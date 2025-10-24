# routers/status.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models import StatusSnapshot, GpuDetails

router = APIRouter()

@router.get("/status")
def get_status(db: Session = Depends(get_db)):
    snap = db.execute(select(StatusSnapshot).order_by(StatusSnapshot.create_time.desc())).scalar_one_or_none()
    if not snap:
        # 没数据时，给前端兜底，避免空白
        return {
            "status": {"gpu": "20%", "cpu": "35%", "memory": "60%", "disk": "80%", "network": "良好", "temp": "45℃"},
            "gpuDetails": {"total": 8, "used": 2, "free": 6}
        }
    gpu = db.execute(select(GpuDetails).where(GpuDetails.snapshot_id == snap.id)).scalars().first()
    status_payload = {
        "gpu": snap.gpu_usage,
        "cpu": snap.cpu_usage,
        "memory": snap.memory_usage,
        "disk": snap.disk_usage,
        "network": snap.network_status,
        "temp": snap.temperature,
    }
    gpu_payload = {
        "total": None, "used": None, "free": None,  # 你的表没有这些计数
        "utilization": getattr(gpu, "utilization", None),
        "memory_usage": getattr(gpu, "memory_usage", None),
        "memory_used": getattr(gpu, "memory_used", None),
        "memory_free": getattr(gpu, "memory_free", None),
        "encode_utilization": getattr(gpu, "encode_utilization", None),
        "decode_utilization": getattr(gpu, "decode_utilization", None),
    }
    return {"status": status_payload, "gpuDetails": gpu_payload}

