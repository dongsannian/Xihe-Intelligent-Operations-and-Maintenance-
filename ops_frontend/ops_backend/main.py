from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import models

# 导入已有路由
from routers import auth, poll, status, overview, metrics, rootcause

# 可选导入 subsystem（如果存在）
try:
    from routers import subsystem
except ImportError:
    subsystem = None

# 创建应用
app = FastAPI(title="OPS Backend API", version="1.0.0")

# 数据库初始化
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 允许跨域
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由（统一使用 /api 前缀）
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(poll.router, prefix="/api/poll", tags=["Poll"])
app.include_router(status.router, prefix="/api/status", tags=["Status"])
app.include_router(overview.router, prefix="/api/overview", tags=["Overview"])
# Metrics 模块
app.include_router(metrics.router, prefix="/api/metrics", tags=["Metrics"])

# Root Cause 模块
app.include_router(rootcause.router, prefix="/api", tags=["RootCause"])


# 如果 subsystem 模块存在，则注册
if subsystem:
    app.include_router(subsystem.router, prefix="/api/subsystem", tags=["Subsystem"])

# 健康检查接口
@app.get("/ping")
def ping():
    return {"ok": True}

@app.get("/")
def root():
    return {"message": "OPS backend is running", "docs": "/docs"}

