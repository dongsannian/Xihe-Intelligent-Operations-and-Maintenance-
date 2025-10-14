# routers/poll.py
from fastapi import APIRouter, Query
from typing import List, Optional
import random
import datetime as dt

router = APIRouter(prefix="/poll", tags=["poll"])

# ---- KPI 汇总（卡片用） ----
@router.get("/summary")
def poll_summary():
    def card(pct):
        # 迷你火柴图 8 段
        spark = [random.randint(40, 100) for _ in range(8)]
        return {"percent": pct, "spark": spark}

    return {
        "cpu": card(round(random.uniform(50, 90), 1)),
        "gpu": card(round(random.uniform(70, 98), 1)),
        "disk": card(round(random.uniform(60, 85), 1)),
        "memory": card(round(random.uniform(70, 90), 1)),
    }

# ---- 任务记录表（筛选+分页）----
@router.get("/records")
def poll_records(
    time_range: str = Query("7d", description="时间范围 7d/30d/custom"),
    hw_type: str = Query("全部"),
    zone: str = Query("全部"),
    status: str = Query("全部"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    # mock 50 条
    hardware_types = ["CPU", "GPU", "硬盘", "内存"]
    statuses = ["已完成", "运行中", "已停止"]
    rows = []
    base = dt.datetime.now()

    for i in range(50):
        ht = random.choice(hardware_types)
        st = random.choice(statuses)
        start = base - dt.timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))
        end = None if st == "运行中" else start + dt.timedelta(hours=random.randint(1, 3))
        rows.append({
            "code": f"PT{base:%Y%m%d}{i:04d}",
            "task_name": f"{ht} 指标监控",
            "hw_type": ht,
            "device": random.choice(["CPU", "GPU", "硬盘", "内存"]),
            "metric": random.choice(["温度", "利用率", "吞吐", "占用率"]),
            "start_time": start.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end.strftime("%Y-%m-%d %H:%M:%S") if end else "-",
            "status": st,
        })

    # 过滤（简单示意）
    if hw_type != "全部":
        rows = [r for r in rows if r["hw_type"] == hw_type]
    if status != "全部":
        rows = [r for r in rows if r["status"] == status]

    total = len(rows)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    return {"list": rows[start_idx:end_idx], "total": total}

# ---- 趋势折线（页面底部小图）----
@router.get("/trend")
def poll_trend(
    range_days: int = Query(7, ge=1, le=30),
):
    xs = []
    base = dt.date.today()
    for i in range(range_days):
        day = base - dt.timedelta(days=range_days - 1 - i)
        xs.append(day.strftime("%m-%d"))

    def series(lo, hi):
        return [round(random.uniform(lo, hi), 1) for _ in xs]

    return {
        "x": xs,
        "cpu": series(60, 90),
        "gpu": series(70, 95),
        "memory": series(60, 90),
        "disk": series(50, 85),
    }

# ---- 兼容你 api.js 的旧方法（表格数据）----
@router.get("/task")  # 你 api.js 里是 '/poll-task'，下面这个路由等价
def poll_task_alias(page: int = 1, page_size: int = 10):
    data = poll_records(page=page, page_size=page_size)
    return data

