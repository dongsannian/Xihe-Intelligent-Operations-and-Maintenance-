from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import models

# 导入已有路由
from routers import auth, poll, status, overview, metrics, root_cause_analysis

# 创建应用
app = FastAPI(title="OPS Backend API", version="1.0.0")

# 数据库初始化
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许跨域
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册已有路由
app.include_router(auth.router)
app.include_router(poll.router)
app.include_router(status.router)
app.include_router(overview.router, prefix="/overview")

# 注册新路由
app.include_router(metrics.router, prefix="/api", tags=["Metrics"])
app.include_router(root_cause_analysis.router)

# 健康检查接口
@app.get("/ping")
def ping():
    return {"ok": True}

@app.get("/")
def root():
    return {"message": "OPS backend is running", "docs": "/docs"}

