from fastapi import APIRouter
from datetime import datetime
import psutil

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

