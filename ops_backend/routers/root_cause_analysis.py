from typing import Dict, List
from fastapi import APIRouter, HTTPException
from utils.root_cause import analyze_root_cause

router = APIRouter(prefix="/api", tags=["Root Cause Analysis"])

@router.get("/root-cause/{service}", response_model=Dict)
async def get_root_cause(service: str):
    """
    分析指定服务的根因和影响链
    
    参数:
        service: 要分析的服务名称
    
    返回:
        包含根因和影响链的字典
    """
    try:
        result = analyze_root_cause(service)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"根因分析失败: {str(e)}")

@router.get("/root-cause/dependencies", response_model=Dict[str, List[str]])
async def get_dependencies():
    """
    获取所有已知的服务依赖关系
    
    返回:
        服务依赖关系字典
    """
    from utils.root_cause import dependencies
    return dependencies

@router.post("/root-cause/analyze-multiple")
async def analyze_multiple_services(services: List[str]):
    """
    批量分析多个服务的根因
    
    参数:
        services: 服务名称列表
    
    返回:
        每个服务的根因分析结果
    """
    results = {}
    for service in services:
        try:
            results[service] = analyze_root_cause(service)
        except Exception as e:
            results[service] = {"error": str(e)}
    return results
