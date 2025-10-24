# routers/rootcause.py
from fastapi import APIRouter
import requests
import json

router = APIRouter()

PROM_URL = "http://127.0.0.1:9090"  # Prometheus 服务地址

@router.get("/rootcause/graph")
def get_root_cause_graph():
    """从 Prometheus 获取多节点状态并生成依赖图"""
    query_cpu = 'node_cpu_seconds_total{mode="system"}'
    query_mem = 'node_memory_MemAvailable_bytes'
    query_up = 'up'

    # 从 Prometheus 获取状态
    cpu_data = requests.get(f"{PROM_URL}/api/v1/query", params={"query": query_cpu}).json()
    mem_data = requests.get(f"{PROM_URL}/api/v1/query", params={"query": query_mem}).json()
    up_data = requests.get(f"{PROM_URL}/api/v1/query", params={"query": query_up}).json()

    nodes = []
    links = []

    # 模拟生成多服务拓扑（可改成数据库或配置）
    services = ["prometheus", "node_exporter", "backend", "frontend", "database"]

    for s in services:
        node = {"name": s, "status": "normal"}
        if "backend" in s and len(cpu_data["data"]["result"]) == 0:
            node["status"] = "abnormal"
        nodes.append(node)

    # 假设依赖关系
    links = [
        {"source": "database", "target": "backend"},
        {"source": "backend", "target": "frontend"},
        {"source": "frontend", "target": "prometheus"},
    ]

    root_cause = next((n["name"] for n in nodes if n["status"] == "abnormal"), "normal")

    return {
        "nodes": nodes,
        "links": links,
        "root_cause": root_cause
    }

