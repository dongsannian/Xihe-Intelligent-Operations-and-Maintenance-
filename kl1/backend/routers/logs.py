# -*- coding: utf-8 -*-
"""
文件：kl1/backend/routers/logs.py
说明：
- 日志 CRUD、AI 日志分析（元器）、AI 问答（整合 route_intent + Prometheus + 最近错误日志）
- 仅对 /api/ask 做了增强；其余接口逻辑保留你的原实现
"""

from fastapi import APIRouter, Depends, Query, Path, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, root_validator
from database import get_db
from models import LogEntry, LogLevel
from sqlalchemy import and_
import os
import requests
import logging
import uuid
from dotenv import load_dotenv
import bcrypt

# ==== 兼容导入：route_intent 可能在 ops_backend 或 kl1 路径 ====
try:
    from ops_backend.utils.intent_router import route_intent
except Exception:
    try:
        from kl1.backend.utils.intent_router import route_intent  # 如果在 kl1 项目内
    except Exception:
        route_intent = None  # 没有就置空，下面会做判空处理
# ============================================================

# 测试用户用
from models import User, UserRole  # 你原文件里的导入

router = APIRouter()

# ---------------- 通用配置 ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 加载 .env
try:
    load_dotenv()
    logger.info("成功加载 .env 环境变量")
except Exception as e:
    logger.warning(f"加载 .env 失败: {e}，将使用系统环境变量")

# 常量（沿用你原来的）
DEFAULT_ASSISTANT_ID = "OLFdKirfJdaS"
YUANQI_API_URL = "https://open.hunyuan.tencent.com/openapi/v1/agent/chat/completions"
API_TIMEOUT = 120
RATE_LIMIT_WINDOW = 60
RATE_LIMIT_MAX_REQUESTS = 10
DEFAULT_USER_ID = "system_user"
rate_limit_store: Dict[str, list] = {}

# ============== 内联：Prometheus 简易查询（无需新文件） ==============
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090").rstrip("/")

def prom_query(expr: str) -> str:
    """查询 Prometheus /api/v1/query，返回首个数值字符串或错误说明（不抛异常）。"""
    try:
        r = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": expr}, timeout=10)
        r.raise_for_status()
        data = r.json().get("data", {}).get("result", [])
        if not data:
            return "暂无数据"
        val = data[0].get("value", [None, ""])[1]
        try:
            return f"{float(val):.2f}"
        except Exception:
            return str(val)
    except Exception as e:
        return f"查询失败:{e}"
# ===================================================================

# ===================== 你原来的模型与请求体 =====================
class YuanqiMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1, max_length=2000)

class AnalyzeRequest(BaseModel):
    user_id: Optional[str] = Field(None, max_length=50)
    assistant_id: str = Field(DEFAULT_ASSISTANT_ID)
    log_id: Optional[int] = Field(None, ge=1)
    log_content: Optional[str] = Field(None, max_length=5000)

    @root_validator(skip_on_failure=True)
    def check_log_source(cls, values):
        if not values.get("log_id") and not values.get("log_content"):
            raise ValueError("必须提供log_id（数据库日志ID）或log_content（日志内容）")
        return values

class AnalysisMessage(BaseModel):
    role: str
    content: str
    timestamp: str

class AnalysisResponse(BaseModel):
    analysis: str
    request_id: Optional[str]
    log_id: Optional[int]
    timestamp: str
    user_id: str
    messages: List[AnalysisMessage]
# ===============================================================

# ===================== 你原来的元器调用 =====================
def call_yuanqi_api(assistant_id: str, user_id: str, messages: List[YuanqiMessage]) -> Dict[str, Any]:
    """调用腾讯元器智能体 API"""
    try:
        token = os.getenv("YUANQI_TOKEN", "")
        if not token:
            raise HTTPException(status_code=500, detail="未配置元器API令牌，请设置 YUANQI_TOKEN")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "X-Source": "openapi",
        }
        # 适配你在原文件中对 content 的结构化要求
        payload = {
            "assistant_id": assistant_id,
            "user_id": user_id,
            "stream": False,
            "messages": [{
                "role": "user",
                "content": [{"type": "text", "text": messages[0].content}]
            }]
        }

        logger.info(f"调用元器API: assistant_id={assistant_id}, user_id={user_id}")
        response = requests.post(YUANQI_API_URL, json=payload, headers=headers, timeout=API_TIMEOUT)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"调用元器失败: {response.status_code} {response.text[:500]}")

        result = response.json()
        if not result.get("choices") or "message" not in result["choices"][0]:
            raise HTTPException(status_code=500, detail="元器返回结构异常，缺少 choices/message")
        return result

    except HTTPException:
        raise
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail=f"调用元器API超时（>{API_TIMEOUT}s）")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="无法连接到元器API服务")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"调用元器API异常: {e}")
# ===========================================================

# ===================== 频率限制中间件（你原来的） =====================
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = datetime.now().timestamp()

    if client_ip not in rate_limit_store:
        rate_limit_store[client_ip] = []
    rate_limit_store[client_ip] = [t for t in rate_limit_store[client_ip] if now - t < RATE_LIMIT_WINDOW]

    if len(rate_limit_store[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
        return HTTPException(status_code=429, detail="请求过于频繁，请稍后再试")

    rate_limit_store[client_ip].append(now)
    return await call_next(request)
# ======================================================================

# ===================== 【关键】增强版 /api/ask =====================
@router.post("/api/ask")
async def ask_question(payload: dict, db: Session = Depends(get_db)):
    """
    问答接口（增强版）：
    1) 优先走 route_intent（若返回 handled=True，直接返回）
    2) 检测“系统状态/CPU/内存/性能/监控/负载”等关键词：
       - 调 Prometheus：CPU、内存
       - 读最近错误日志（数据库）
       - 将以上信息组合为上下文，交给元器 AI 做综合回答
    3) 其他问题：直接调用元器 AI
    """
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="缺少 question 参数")

    # 1) 意图路由（保持你原有逻辑）
    if route_intent:
        try:
            result = route_intent(question)
            if isinstance(result, dict) and result.get("handled"):
                return {"source": "ops_backend", "answer": result.get("answer", "")}
        except Exception as e:
            logger.warning(f"route_intent 调用异常，跳过：{e}")

    # 2) 系统/性能类问题 → 走 Prometheus + 最近错误日志 + 元器综合分析
    lower_q = question.lower()
    sys_kw = ("系统状态", "cpu", "内存", "性能", "监控", "负载", "资源")
    if any(k in question for k in sys_kw) or any(k in lower_q for k in ("cpu", "memory", "performance", "monitor", "load", "resource")):
        try:
            cpu_expr = '100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)'
            mem_expr = '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100'
            cpu_pct = prom_query(cpu_expr)
            mem_pct = prom_query(mem_expr)

            # 读取数据库最近 5 条 ERROR/CRITICAL 日志
            recent_logs = db.query(LogEntry).filter(
                LogEntry.level.in_([LogLevel.ERROR, LogLevel.CRITICAL])
            ).order_by(LogEntry.timestamp.desc()).limit(5).all()
            logs_text = "\n".join([f"[{l.timestamp.isoformat()}][{l.level}] {l.source}: {l.message}" for l in recent_logs]) or "暂无明显错误日志"

            prompt = f"""你是平台的智能运维助手，请结合“系统监控”和“最近错误日志”给出简洁、可操作的结论与建议。
用户问题：{question}

系统监控（Prometheus 即时）：
- CPU 使用率：{cpu_pct}%
- 内存使用率：{mem_pct}%

最近错误日志（数据库Top5）：
{logs_text}

请输出：
1) 当前状态判断（是否异常，为什么）
2) 可能根因（基于日志线索）
3) 具体建议（操作步骤/阈值/需要关注的指标）
"""

            ai_result = call_yuanqi_api(
                assistant_id=DEFAULT_ASSISTANT_ID,
                user_id=DEFAULT_USER_ID,
                messages=[YuanqiMessage(role="user", content=prompt)]
            )
            ai_content = ai_result["choices"][0]["message"]["content"]
            return {"source": "ops_backend+prometheus+logs", "answer": ai_content, "request_id": ai_result.get("request_id")}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"系统状态综合分析失败：{e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"系统状态分析失败：{e}")

    # 3) 其他问题 → 原样走元器
    ai_result = call_yuanqi_api(
        assistant_id=DEFAULT_ASSISTANT_ID,
        user_id=DEFAULT_USER_ID,
        messages=[YuanqiMessage(role="user", content=question)]
    )
    ai_content = ai_result["choices"][0]["message"]["content"]
    return {"source": "yuanqi", "answer": ai_content, "request_id": ai_result.get("request_id")}
# ======================================================================


# ===================== 你原来的 /login 初始化测试用户 =====================
@router.post("/login")
def init_test_users(db: Session = Depends(get_db)):
    test_users = [
        {"username": "admin001", "email": "admin@example.com", "password": "Admin@123", "full_name": "系统管理员", "role": UserRole.ADMIN},
        {"username": "member001", "email": "member1@example.com", "password": "Member@123", "full_name": "张三", "role": UserRole.MEMBER},
    ]
    for user_data in test_users:
        existing = db.query(User).filter(User.username == user_data["username"]).first()
        if existing:
            continue
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            full_name=user_data["full_name"],
            role=user_data["role"]
        )
        user.set_password(user_data["password"])
        db.add(user)
    db.commit()
    return {"message": "测试用户初始化完成"}
# ======================================================================


# ===================== 你原来的 /analyze：AI 日志分析 =====================
@router.post(
    "/analyze",
    description="使用腾讯元器AI分析日志内容",
    response_model=AnalysisResponse
)
def analyze_log(request: AnalyzeRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    try:
        if not request.user_id or not request.user_id.strip():
            request.user_id = f"auto_{uuid.uuid4().hex[:8]}"

        log_content = request.log_content
        if request.log_id:
            log = db.query(LogEntry).filter(LogEntry.id == request.log_id).first()
            if not log:
                raise HTTPException(status_code=404, detail=f"ID为{request.log_id}的日志不存在")
            log_content = log.message

        if not log_content or not log_content.strip():
            raise HTTPException(status_code=400, detail="日志内容不能为空")

        messages = [YuanqiMessage(
            role="user",
            content=f"""请分析以下日志内容，帮我：
1. 识别日志级别和可能的问题类型
2. 解释错误原因（如果能识别）
3. 提供具体的解决方案或建议

日志内容：
{log_content}"""
        )]

        ai_result = call_yuanqi_api(
            assistant_id=request.assistant_id,
            user_id=request.user_id,
            messages=messages
        )

        ai_content = ai_result["choices"][0]["message"]["content"]
        now_str = datetime.now().isoformat()
        return {
            "analysis": ai_content,
            "request_id": ai_result.get("request_id"),
            "log_id": request.log_id,
            "timestamp": now_str,
            "user_id": request.user_id,
            "messages": [
                AnalysisMessage(role="user", content=log_content, timestamp=now_str),
                AnalysisMessage(role="assistant", content=ai_content, timestamp=now_str)
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"日志分析失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"日志分析失败: {e}")
# ======================================================================


# ===================== 你原来的 日志 CRUD =====================
class LogEntryBase(BaseModel):
    source: str = Field(..., min_length=1, max_length=100)
    level: LogLevel = Field(...)
    message: str = Field(..., min_length=1, max_length=10000)
    module: Optional[str] = Field(None, max_length=100)
    line_number: Optional[int] = Field(None, ge=0)  # 允许0值，因为有些日志可能来自没有行号的地方
    extra: Optional[str] = Field(None, max_length=5000)

class LogEntryCreate(LogEntryBase):
    pass

class LogEntryResponse(LogEntryBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True

@router.get("/", response_model=List[LogEntryResponse], description="获取日志列表，支持多条件筛选")
def get_logs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    level: Optional[LogLevel] = Query(None),
    source: Optional[str] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    keyword: Optional[str] = Query(None)
) -> List[LogEntryResponse]:
    try:
        query = db.query(LogEntry)
        if level:
            query = query.filter(LogEntry.level == level)
        if source:
            query = query.filter(LogEntry.source.contains(source))
        if keyword:
            query = query.filter(LogEntry.message.contains(keyword))
        if start_time and end_time:
            if start_time > end_time:
                raise HTTPException(status_code=400, detail="开始时间不能晚于结束时间")
            query = query.filter(and_(LogEntry.timestamp >= start_time, LogEntry.timestamp <= end_time))
        elif start_time:
            query = query.filter(LogEntry.timestamp >= start_time)
        elif end_time:
            query = query.filter(LogEntry.timestamp <= end_time)

        logs = query.order_by(LogEntry.timestamp.desc()).offset(skip).limit(limit).all()
        logger.info(f"查询日志列表: 找到{len(logs)}条记录 (skip={skip}, limit={limit})")
        return logs
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"查询日志列表出错: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"查询日志失败: {e}")

@router.get("/{log_id}", response_model=LogEntryResponse, description="获取指定ID的日志详情")
def get_log(log_id: int = Path(..., ge=1), db: Session = Depends(get_db)) -> LogEntryResponse:
    try:
        log = db.query(LogEntry).filter(LogEntry.id == log_id).first()
        if not log:
            raise HTTPException(status_code=404, detail="日志不存在")
        return log
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"查询日志详情出错: ID={log_id}, 错误={e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"查询日志详情失败: {e}")

@router.post("/", response_model=LogEntryResponse, status_code=201, description="添加新的日志条目")
def create_log(log: LogEntryCreate, db: Session = Depends(get_db)) -> LogEntryResponse:
    try:
        db_log = LogEntry(**log.dict())
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        logger.info(f"创建新日志: ID={db_log.id}, source={log.source}, level={log.level}")
        return db_log
    except Exception as e:
        db.rollback()
        logger.error(f"创建日志出错: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"创建日志失败: {e}")

@router.delete("/{log_id}", status_code=204, description="删除指定ID的日志")
def delete_log(log_id: int = Path(..., ge=1), db: Session = Depends(get_db)) -> None:
    try:
        log = db.query(LogEntry).filter(LogEntry.id == log_id).first()
        if not log:
            raise HTTPException(status_code=404, detail="日志不存在")
        db.delete(log)
        db.commit()
        logger.info(f"删除日志: ID={log_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"删除日志出错: ID={log_id}, 错误={e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"删除日志失败: {e}")
# ======================================================================

