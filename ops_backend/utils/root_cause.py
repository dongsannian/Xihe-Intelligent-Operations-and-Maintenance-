
# 静态依赖关系，可以将来替换成数据库/CMDB
dependencies = {
    "node01": ["nginx", "mysql"],
    "nginx": ["frontend"],
    "frontend": [],
    "mysql": []
}

def analyze_root_cause(service: str):
    """
    返回服务依赖链，用于根因分析
    """
    if service not in dependencies:
        return {"root_cause": f"未知服务: {service}"}
    dependents = dependencies.get(service, [])
    return {
        "root_cause": f"{service} 异常导致下游服务异常",
        "impact_chain": dependents
    }
    affected = []

    def dfs(svc):
        affected.append(svc)
        for dep in dependencies.get(svc, []):
            dfs(dep)

    dfs(service)
    return {"root_cause": service, "affected_chain": affected}

