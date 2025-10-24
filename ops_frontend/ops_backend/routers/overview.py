from fastapi import APIRouter
from datetime import datetime
import psutil
import requests  # ✅ 顶格导入
# ==================================================
# 系统状态监控接口
# ==================================================
router = APIRouter()

@router.get("/ping")
def ping():
    return {"ok": True}

@router.get("/status")
async def get_system_status():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    total_mem = round(memory.total / (1024 ** 3), 1)
    used_mem = round(memory.used / (1024 ** 3), 1)
    free_mem = round(memory.available / (1024 ** 3), 1)

    gpu = 0.0
    try:
        import pynvml
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        gpu = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        pynvml.nvmlShutdown()
    except Exception:
        pass

    return {
        "cpu": {
            "total_usage": cpu,
            "per_core": psutil.cpu_percent(percpu=True),
            "user": psutil.cpu_times_percent().user,
            "system": psutil.cpu_times_percent().system,
            "iowait": psutil.cpu_times_percent().iowait
        },
        "memory": {
            "total": f"{total_mem} GB",
            "used": f"{used_mem} GB",
            "free": f"{free_mem} GB",
            "cached": "2.3 GB",
            "swap_used": "1.1 GB",
            "swap_total": "2 GB"
        },
        "disk": {
            "read_speed": "150 MB/s",
            "write_speed": "120 MB/s",
            "io_wait": "12 ms",
            "usage_percent": 72.5,
            "free_space": "120 GB"
        },
        "network": {
            "upload": "20 Mbps",
            "download": "55 Mbps",
            "packet_loss": 0.1,
            "latency": "18 ms"
        },
        "gpu": gpu
    }

# ==================================================
# Prometheus 告警接口
# ==================================================
PROMETHEUS_URL = "http://127.0.0.1:9090"  # 修改为实际 Prometheus 地址

@router.get("/alerts")
async def get_prometheus_alerts():
    """
    获取 Prometheus 当前告警（含状态 + 模块分类）
    """
    try:
        resp = requests.get(f"{PROMETHEUS_URL}/api/v1/alerts", timeout=5)
        data = resp.json()

        alerts = []
        for i, alert in enumerate(data["data"]["alerts"], start=1):
            labels = alert.get("labels", {})
            annotations = alert.get("annotations", {})
            status = alert.get("state", "").upper() or labels.get("state", "UNKNOWN").upper()

            message = (
                annotations.get("description")
                or annotations.get("summary")
                or labels.get("alertname", "未命名告警")
            )
            module = classify_module(message)

            alerts.append({
                "id": i,
                "alertname": labels.get("alertname", "Unknown"),
                "message": message,
                "level": labels.get("severity", "info").upper(),
                "module": module,
                "status": status,  # FIRING / RESOLVED
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        return alerts

    except Exception as e:
        return {"error": str(e)}

def classify_module(text: str) -> str:
    text = text.lower()
    if any(k in text for k in ["cpu", "processor", "load"]):
        return "CPU"
    if any(k in text for k in ["memory", "ram", "swap"]):
        return "内存"
    if any(k in text for k in ["disk", "io", "filesystem"]):
        return "磁盘"
    if any(k in text for k in ["network", "bandwidth", "ping"]):
        return "网络"
    if any(k in text for k in ["service", "nginx", "mysql", "backend", "api"]):
        return "服务"
    return "其他"

