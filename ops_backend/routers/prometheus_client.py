import requests
import os

PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090").rstrip("/")

def query_prometheus(query: str):
    url = f"{PROMETHEUS_URL}/api/v1/query"
    response = requests.get(url, params={'query': query})
    if response.status_code == 200:
        return response.json().get('data', {}).get('result', [])
    else:
        raise Exception(f"Prometheus query failed: {response.text}")

