from elasticsearch import Elasticsearch
import os

# 初始化 Elasticsearch 客户端
ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
es = Elasticsearch([ES_HOST])

def query_logs(log_pattern: str, index: str="log-*"):
    """根据日志模式查询 Elasticsearch"""
    body = {
        "query": {
            "regexp": {
                "message": f".*{log_pattern}.*"
            }
        }
    }
    response = es.search(index=index, body=body)
    return response['hits']['hits']

