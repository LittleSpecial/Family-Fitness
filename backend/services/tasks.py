"""每日任务生成服务"""
import random
from datetime import date
from typing import List
from sqlmodel import Session, select
from models import DailyTask


# 任务池
TASK_POOL = [
    {"task_name": "喝 8 杯水", "task_type": "water", "reward_points": 10},
    {"task_name": "早起一杯温水", "task_type": "water", "reward_points": 5},
    {"task_name": "拉伸 10 分钟", "task_type": "stretch", "reward_points": 10},
    {"task_name": "颈部放松 5 分钟", "task_type": "stretch", "reward_points": 5},
    {"task_name": "散步 30 分钟", "task_type": "walk", "reward_points": 15},
    {"task_name": "饭后走 100 步", "task_type": "walk", "reward_points": 5},
    {"task_name": "少油饮食", "task_type": "diet", "reward_points": 10},
    {"task_name": "多吃蔬菜", "task_type": "diet", "reward_points": 10},
    {"task_name": "今日无糖饮料", "task_type": "no_sugar", "reward_points": 15},
    {"task_name": "减少甜食摄入", "task_type": "no_sugar", "reward_points": 10},
    {"task_name": "23:00 前入睡", "task_type": "sleep", "reward_points": 15},
    {"task_name": "完成一次运动", "task_type": "exercise", "reward_points": 20},
]


def generate_daily_tasks(session: Session, user_id: int, task_date: date) -> List[DailyTask]:
    """
    为用户生成每日任务
    
    Args:
        session: 数据库会话
        user_id: 用户ID
        task_date: 任务日期
    
    Returns:
        生成的任务列表
    """
    # 检查是否已生成任务
    statement = select(DailyTask).where(
        DailyTask.user_id == user_id,
        DailyTask.date == task_date
    )
    existing_tasks = session.exec(statement).all()
    
    if existing_tasks:
        return existing_tasks
    
    # 从任务池中随机选择 5 个任务,确保任务类型不重复
    selected_tasks = []
    used_types = set()
    
    # 随机打乱任务池
    shuffled_pool = random.sample(TASK_POOL, len(TASK_POOL))
    
    for task_template in shuffled_pool:
        task_type = task_template["task_type"]
        
        # 确保每种类型只出现一次
        if task_type not in used_types:
            task = DailyTask(
                user_id=user_id,
                task_name=task_template["task_name"],
                task_type=task_type,
                reward_points=task_template["reward_points"],
                date=task_date,
                done=False
            )
            selected_tasks.append(task)
            used_types.add(task_type)
        
        # 选够 5 个任务就停止
        if len(selected_tasks) >= 5:
            break
    
    # 批量插入数据库
    for task in selected_tasks:
        session.add(task)
    session.commit()
    
    # 刷新对象以获取生成的 ID
    for task in selected_tasks:
        session.refresh(task)
    
    return selected_tasks
