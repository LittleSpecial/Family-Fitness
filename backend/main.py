"""FastAPI 应用主程序"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from config import settings
from database import create_db_and_tables
from routers import exercise, meals, tasks
from models import User
from sqlmodel import Session, select
from database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时创建数据库表
    create_db_and_tables()
    
    # 创建默认测试用户(如果不存在)
    with Session(engine) as session:
        statement = select(User).where(User.id == 1)
        existing_user = session.exec(statement).first()
        
        if not existing_user:
            default_user = User(id=1, name="测试用户", role="other")
            session.add(default_user)
            session.commit()
            print("✅ 已创建默认测试用户 (ID=1, name=测试用户)")
    
    print("✅ 数据库初始化完成")
    yield
    print("👋 应用关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title="FamilyFit 健康助手 API",
    description="家庭健康管理应用后端 API",
    version="1.0.0",
    lifespan=lifespan
)

# 配置 CORS - 允许所有来源（生产环境应限制）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Railway/Vercel 部署时允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(exercise.router)
app.include_router(meals.router)
app.include_router(tasks.router)

# 挂载前端静态文件（Railway 一体化部署）
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")


@app.get("/")
def root():
    """首页 - 返回前端应用或 API 信息"""
    frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
    index_file = os.path.join(frontend_dist, "index.html")
    
    if os.path.exists(index_file):
        return FileResponse(index_file)
    
    # 如果前端未构建，返回 API 信息
    return {
        "message": "欢迎使用 FamilyFit 健康助手 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
