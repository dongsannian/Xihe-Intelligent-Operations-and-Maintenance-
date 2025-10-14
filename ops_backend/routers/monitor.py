from fastapi import APIRouter
from utils.prometheus_client import query_prometheus
from utils.elasticsearch_client import query_logs

router = APIRouter(prefix="/api/monitor", tags=["Monitor"])

# 查询 CPU 使用率
@router.get("/cpu")
def cpu_usage():
    query = '100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)'
    return {"metric": "cpu_usage", "data": query_prometheus(query)}

# 查询内存使用率
@router.get("/memory")
def memory_usage():
    query = '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100'
    return {"metric": "memory_usage", "data": query_prometheus(query)}

# 查询磁盘使用率
@router.get("/disk")
def disk_usage():
    query = '100 * (1 - (node_filesystem_avail_bytes{fstype!~"tmpfs|overlay"} / node_filesystem_size_bytes{fstype!~"tmpfs|overlay"}))'
    return {"metric": "disk_usage", "data": query_prometheus(query)}

# 查询日志数据
@router.get("/logs")
def get_logs(log_type: str):
    return {"logs": query_logs(log_type)}  # 依据日志类型查询

# 根因分析接口：结合 Prometheus 数据和日志数据进行分析
@router.get("/rootcause")
def root_cause_analysis():
    cpu_data = query_prometheus('cpu_usage')
    error_logs = query_logs('error|fail')
    # 根因分析：可以根据 CPU 使用率和错误日志返回分析结果
    return {"cpu": cpu_data, "logs": error_logs}

# AI 问答接口：根据问题返回智能分析
@router.get("/ai-query")
def ai_query(query: str):
    if "系统状态" in query:
        cpu_data = query_prometheus('cpu_usage')
        memory_data = query_prometheus('memory_usage')
        return {"answer": f"CPU使用率: {cpu_data}, 内存使用: {memory_data}"}
    return {"answer": "无法理解问题"}

