from fastapi import APIRouter
import psutil

router = APIRouter(prefix="/overview", tags=["系统总览"])

@router.get("/status")
def get_system_status():
    # 获取 CPU 信息
    cpu_total = psutil.cpu_percent(interval=0.5)
    cpu_per_core = psutil.cpu_percent(interval=0.5, percpu=True)

    # 获取内存信息
    memory = psutil.virtual_memory()

    # 获取磁盘信息
    disk = psutil.disk_usage('/')

    # 获取网络信息
    net = psutil.net_io_counters()

    return {
        "cpu": {
            "total_usage": cpu_total,
            "per_core": cpu_per_core
        },
        "memory": {
            "used": f"{memory.used / (1024 ** 3):.1f} GB",
            "total": f"{memory.total / (1024 ** 3):.1f} GB",
            "free": f"{memory.free / (1024 ** 3):.1f} GB",
            "percent": memory.percent
        },
        "disk": {
            "usage_percent": disk.percent,
            "free_space": f"{disk.free / (1024 ** 3):.1f} GB"
        },
        "network": {
            "upload": f"{net.bytes_sent / 1024 / 1024:.1f} MB",
            "download": f"{net.bytes_recv / 1024 / 1024:.1f} MB"
        }
    }

