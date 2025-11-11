"""任务相关路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from datetime import date, timedelta
from typing import Dict
from pydantic import BaseModel
from database import get_session
from models import DailyTask, ExerciseRecord, MealRecord
from services.tasks import generate_daily_tasks
import json

router = APIRouter(prefix="/api", tags=["tasks"])


class TaskDoneRequest(BaseModel):
    """任务完成请求"""
    task_id: int
    user_id: int


@router.get("/tasks/today")
def get_today_tasks(
    user_id: int,
    session: Session = Depends(get_session)
):
    """
    获取今日任务
    
    Args:
        user_id: 用户ID
        session: 数据库会话
    
    Returns:
        今日任务列表
    """
    today = date.today()
    
    # 生成或获取今日任务
    tasks = generate_daily_tasks(session, user_id, today)
    
    # 统计数据
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.done)
    total_points = sum(task.reward_points for task in tasks if task.done)
    
    # 格式化任务数据
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            "id": task.id,
            "task_name": task.task_name,
            "task_type": task.task_type,
            "done": task.done,
            "reward_points": task.reward_points
        })
    
    return {
        "success": True,
        "data": {
            "date": str(today),
            "tasks": tasks_data,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "total_points": total_points
        }
    }


@router.post("/tasks/done")
def mark_task_done(
    request: TaskDoneRequest,
    session: Session = Depends(get_session)
):
    """
    标记任务为已完成
    
    Args:
        request: 任务完成请求
        session: 数据库会话
    
    Returns:
        更新后的任务状态
    """
    # 查询任务
    task = session.get(DailyTask, request.task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    if task.user_id != request.user_id:
        raise HTTPException(status_code=403, detail="无权操作该任务")
    
    # 标记为已完成
    task.done = True
    session.add(task)
    session.commit()
    session.refresh(task)
    
    # 计算今日总积分
    today = date.today()
    statement = select(DailyTask).where(
        DailyTask.user_id == request.user_id,
        DailyTask.date == today,
        DailyTask.done == True
    )
    completed_tasks = session.exec(statement).all()
    total_points_today = sum(t.reward_points for t in completed_tasks)
    
    return {
        "success": True,
        "data": {
            "task_id": task.id,
            "done": task.done,
            "reward_points": task.reward_points,
            "total_points_today": total_points_today
        },
        "message": f"任务完成,获得 {task.reward_points} 积分"
    }


@router.get("/trends")
def get_health_trends(
    user_id: int,
    days: int = 7,
    session: Session = Depends(get_session)
):
    """
    获取健康趋势数据
    
    Args:
        user_id: 用户ID
        days: 查询天数(7或30)
        session: 数据库会话
    
    Returns:
        趋势数据
    """
    # 计算日期范围
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)
    
    # 查询运动数据
    exercise_statement = select(ExerciseRecord).where(
        ExerciseRecord.user_id == user_id,
        ExerciseRecord.date >= start_date,
        ExerciseRecord.date <= end_date
    )
    exercises = session.exec(exercise_statement).all()
    
    # 查询饮食数据
    meal_statement = select(MealRecord).where(
        MealRecord.user_id == user_id,
        MealRecord.date >= start_date,
        MealRecord.date <= end_date
    )
    meals = session.exec(meal_statement).all()
    
    # 查询任务数据
    task_statement = select(DailyTask).where(
        DailyTask.user_id == user_id,
        DailyTask.date >= start_date,
        DailyTask.date <= end_date
    )
    tasks = session.exec(task_statement).all()
    
    # 按日期组织数据
    date_range = [start_date + timedelta(days=i) for i in range(days)]
    
    daily_scores = []
    exercise_calories = []
    exercise_durations = []
    exercise_steps = []
    diet_scores = []
    diet_calories = []
    task_rates = []
    
    for d in date_range:
        # 运动数据
        day_exercises = [e for e in exercises if e.date == d]
        total_calories = sum(e.calories for e in day_exercises)
        total_duration = sum(e.duration_min for e in day_exercises)
        total_steps = sum(e.steps or 0 for e in day_exercises)
        exercise_score = min(sum(e.score for e in day_exercises), 100)
        
        exercise_calories.append(total_calories)
        exercise_durations.append(total_duration)
        exercise_steps.append(total_steps)
        
        # 饮食数据
        day_meals = [m for m in meals if m.date == d]
        meal_calories = sum(m.total_calories or 0 for m in day_meals)
        avg_meal_score = int(sum(m.health_score for m in day_meals) / len(day_meals)) if day_meals else 0
        
        diet_calories.append(meal_calories)
        diet_scores.append(avg_meal_score)
        
        # 任务数据
        day_tasks = [t for t in tasks if t.date == d]
        task_total = len(day_tasks)
        task_done = sum(1 for t in day_tasks if t.done)
        task_rate = int((task_done / task_total * 100)) if task_total > 0 else 0
        task_points = sum(t.reward_points for t in day_tasks if t.done)
        
        task_rates.append({"date": str(d), "rate": task_rate})
        
        # 综合得分计算
        # 如果三项都有数据: (运动得分 × 0.4 + 饮食得分 × 0.4 + 任务积分 × 0.2)
        total_score = 0
        weight_sum = 0
        
        if exercise_score > 0:
            total_score += exercise_score * 0.4
            weight_sum += 0.4
        
        if avg_meal_score > 0:
            total_score += avg_meal_score * 0.4
            weight_sum += 0.4
        
        if task_points > 0:
            # 任务积分归一化到 0-100
            normalized_task_score = min(task_points, 100)
            total_score += normalized_task_score * 0.2
            weight_sum += 0.2
        
        # 按权重归一化
        final_score = int(total_score / weight_sum) if weight_sum > 0 else 0
        
        daily_scores.append({"date": str(d), "score": final_score})
    
    return {
        "success": True,
        "data": {
            "daily_scores": daily_scores,
            "exercise_trends": {
                "calories": exercise_calories,
                "duration": exercise_durations,
                "steps": exercise_steps
            },
            "task_completion_rate": task_rates,
            "diet_trends": {
                "avg_health_scores": diet_scores,
                "daily_calories": diet_calories
            }
        }
    }
