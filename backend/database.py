from sqlmodel import SQLModel, create_engine, Session
from config import settings

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # 设置为 True 可以看到 SQL 语句
    connect_args={"check_same_thread": False}  # SQLite 需要
)

def create_db_and_tables():
    """创建数据库表"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """获取数据库会话"""
    with Session(engine) as session:
        yield session
