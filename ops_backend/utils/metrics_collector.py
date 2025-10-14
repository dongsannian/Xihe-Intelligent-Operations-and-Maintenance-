
import psutil

def get_system_metrics():
    """
    采集基础系统指标
    返回 CPU、内存、磁盘占用率
    """
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
    }

