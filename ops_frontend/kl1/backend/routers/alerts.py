from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import logging
import json
from database import get_db
from models import LogEntry, LogLevel
print("✅ alerts.py 文件被导入执行")

router = APIRouter(tags=["Alerts"])
# 在此打印确认是否进入路由
#logger.info("Loaded /api/alerts route.")
print("✅ alerts 模块已成功注册到 FastAPI")

# 初始化日志
logger = logging.getLogger(__name__)

@router.post("/alerts")
async def receive_alerts(request: Request, db: Session = Depends(get_db)):
    """
    接收来自 Alertmanager 的告警推送。
    这些数据将被存入日志数据库，并可触发 AI 分析。
    """
    try:
        payload = await request.json()
        alerts = payload.get("alerts", [])
        if not alerts:
            logger.warning("收到空告警")
            raise HTTPException(status_code=400, detail="空告警数据")

        records = []
        for alert in alerts:
            labels = alert.get("labels", {})
            annotations = alert.get("annotations", {})
            status = alert.get("status", "firing")
            starts_at = alert.get("startsAt")
            ends_at = alert.get("endsAt")

            # 格式化时间
            start_time = datetime.fromisoformat(starts_at.replace("Z", "+00:00")) if starts_at else datetime.now()
            end_time = datetime.fromisoformat(ends_at.replace("Z", "+00:00")) if ends_at else None

            # 记录内容
            message = annotations.get("description", "未提供描述")
            level = LogLevel.WARNING if status == "firing" else LogLevel.INFO

            log_entry = LogEntry(
                source="PrometheusAlert",
                level=level,
                message=f"[{status.upper()}] {annotations.get('summary', '')} - {message}",
                module=labels.get("alertname", "system_alert"),
                timestamp=start_time
            )

            db.add(log_entry)
            records.append(log_entry)

            logger.info(f"接收到告警: {log_entry.message}")

        db.commit()
        return {"status": "success", "count": len(records)}

    except Exception as e:
        logger.error(f"处理告警失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
