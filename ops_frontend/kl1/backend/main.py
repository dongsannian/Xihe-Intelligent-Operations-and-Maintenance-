from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import logs, alerts  # ✅ 新增 alerts 模块
from database import engine, Base
import uvicorn
from routers import overview

print("✅ alerts 模块加载成功")

# 创建数据库表（如果不存在）
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用
app = FastAPI(
    title="日志管理系统 API",
    description="用于收集、查询和分析系统日志、系统告警的后端 API",
    version="1.1.0"
)

# 配置跨域（开发环境允许所有来源，生产环境需限制来源）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载日志管理模块 - 直接挂载到根路径，因为logs.py中已包含完整路径定义
app.include_router(logs.router, tags=["日志管理"])

# ✅ 新增：挂载告警接收模块
# 告警来自 Prometheus 的 Alertmanager，会通过 webhook 调用此接口
app.include_router(alerts.router, prefix="/api", tags=["系统告警"])
app.include_router(overview.router)

# 根路径接口，用于验证服务状态
@app.get("/")
async def root():
    return {
        "message": "欢迎使用日志与告警管理系统 API",
        "version": "1.1.0",
        "modules": ["logs", "alerts"]
    }

# 允许通过 python3 main.py 启动服务
if __name__ == "__main__":
    uvicorn.run(
        app="main:app",   # 指定应用入口
        host="0.0.0.0",   # 允许所有IP访问
        port=8000,        # 服务端口
        reload=True       # 开发模式：自动热重载
    )

