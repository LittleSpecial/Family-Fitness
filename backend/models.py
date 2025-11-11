from datetime import datetime, date
from typing import Optional
from sqlmodel import Field, SQLModel, JSON, Column
from sqlalchemy import Index


class User(SQLModel, table=True):
    """用户表"""
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True, index=True)  # 登录用户名
    password_hash: str = Field(max_length=255)  # 密码哈希
    name: str = Field(max_length=50)  # 显示名称
    total_score: int = Field(default=0, ge=0)  # 总积分
    created_at: datetime = Field(default_factory=datetime.now)


class ExerciseRecord(SQLModel, table=True):
    """运动记录表"""
    __tablename__ = "exercise_records"
    __table_args__ = (
        Index('idx_user_date', 'user_id', 'date'),
        Index('idx_user_created', 'user_id', 'created_at'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    exercise_type: str = Field(max_length=50)
    duration_min: int = Field(ge=0)
    calories: int = Field(ge=0)
    steps: Optional[int] = Field(default=None, ge=0)
    avg_heart_rate: Optional[int] = Field(default=None, ge=0)
    max_heart_rate: Optional[int] = Field(default=None, ge=0)
    source_device: str = Field(max_length=20)  # apple/huawei/unknown
    date: date
    score: int = Field(ge=0, le=100)
    created_at: datetime = Field(default_factory=datetime.now)


class MealRecord(SQLModel, table=True):
    """饮食记录表"""
    __tablename__ = "meal_records"
    __table_args__ = (
        Index('idx_meal_user_date', 'user_id', 'date'),
        Index('idx_meal_user_date_type', 'user_id', 'date', 'meal_type'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    meal_type: str = Field(max_length=20)  # breakfast/lunch/dinner/snack
    food_items: str = Field(sa_column=Column(JSON))  # JSON 格式存储食物列表
    total_calories: Optional[int] = Field(default=None, ge=0)
    health_score: int = Field(ge=0, le=100)
    analysis: Optional[str] = Field(default=None)
    date: date
    created_at: datetime = Field(default_factory=datetime.now)


class DailyTask(SQLModel, table=True):
    """每日任务表"""
    __tablename__ = "daily_tasks"
    __table_args__ = (
        Index('idx_task_user_date', 'user_id', 'date'),
        Index('idx_task_user_date_done', 'user_id', 'date', 'done'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    task_name: str = Field(max_length=100)
    task_type: str = Field(max_length=20)  # water/stretch/walk/diet/no_sugar/sleep/exercise
    done: bool = Field(default=False)
    date: date
    reward_points: int = Field(default=10, ge=0)
    created_at: datetime = Field(default_factory=datetime.now)
