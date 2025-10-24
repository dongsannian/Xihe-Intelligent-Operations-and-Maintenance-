from fastapi import APIRouter
from utils.metrics_collector import get_system_metrics
from utils.log_collector import get_recent_logs
from utils.service_checker import check_service
from utils.root_cause import analyze_root_cause

router = APIRouter()

@router.get("/metrics")
async def get_metrics():
    return get_system_metrics()

@router.get("/logs")
async def get_logs(lines: int = 50):
    return {"logs": get_recent_logs(lines)}

@router.get("/service/{name}")
async def service_status(name: str):
    return check_service(name)

@router.get("/rootcause/{service}")
async def root_cause(service: str):
    return analyze_root_cause(service)
