"""饮食相关路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import date
from typing import List, Dict
from pydantic import BaseModel
from database import get_session
from models import MealRecord
from services.diet import analyze_meal_health
import json

router = APIRouter(prefix="/api/meals", tags=["meals"])


class FoodItem(BaseModel):
    """食物条目"""
    name: str
    amount: str


class AddMealRequest(BaseModel):
    """添加饮食记录请求"""
    user_id: int
    meal_type: str  # breakfast/lunch/dinner/snack
    food_items: List[FoodItem]
    date: str  # YYYY-MM-DD


@router.post("/add")
async def add_meal_record(
    request: AddMealRequest,
    session: Session = Depends(get_session)
):
    """
    添加饮食记录并分析
    
    Args:
        request: 饮食记录请求
        session: 数据库会话
    
    Returns:
        分析结果
    """
    # 验证餐次类型
    if request.meal_type not in ["breakfast", "lunch", "dinner", "snack"]:
        raise HTTPException(status_code=422, detail="meal_type 不合法")
    
    # 验证食物列表
    if not request.food_items:
        raise HTTPException(status_code=400, detail="食物列表为空")
    
    try:
        # 解析日期
        meal_date = date.fromisoformat(request.date)
        
        # 转换食物列表为字典格式
        food_items_list = [item.dict() for item in request.food_items]
        
        # 调用AI分析服务
        analysis_result = await analyze_meal_health(food_items_list)
        
        # 保存到数据库
        meal_record = MealRecord(
            user_id=request.user_id,
            meal_type=request.meal_type,
            food_items=json.dumps(food_items_list, ensure_ascii=False),
            total_calories=analysis_result["total_calories"],
            health_score=analysis_result["health_score"],
            analysis=analysis_result["analysis"],
            date=meal_date
        )
        
        session.add(meal_record)
        session.commit()
        session.refresh(meal_record)
        
        return {
            "success": True,
            "data": {
                "id": meal_record.id,
                "meal_type": meal_record.meal_type,
                "health_score": meal_record.health_score,
                "total_calories": meal_record.total_calories,
                "analysis": meal_record.analysis
            },
            "message": "饮食记录成功"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"日期格式错误: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 分析失败: {str(e)}")


@router.get("/today")
def get_today_meals(
    user_id: int,
    session: Session = Depends(get_session)
):
    """
    获取今日饮食记录
    
    Args:
        user_id: 用户ID
        session: 数据库会话
    
    Returns:
        今日饮食记录列表
    """
    today = date.today()
    
    statement = select(MealRecord).where(
        MealRecord.user_id == user_id,
        MealRecord.date == today
    )
    
    meals = session.exec(statement).all()
    
    # 计算统计数据
    total_calories = sum(meal.total_calories or 0 for meal in meals)
    avg_score = int(sum(meal.health_score for meal in meals) / len(meals)) if meals else 0
    
    # 格式化返回数据
    meals_data = []
    for meal in meals:
        meals_data.append({
            "id": meal.id,
            "meal_type": meal.meal_type,
            "food_items": json.loads(meal.food_items),
            "health_score": meal.health_score,
            "total_calories": meal.total_calories,
            "analysis": meal.analysis
        })
    
    return {
        "success": True,
        "data": {
            "date": str(today),
            "meals": meals_data,
            "total_calories": total_calories,
            "avg_health_score": avg_score,
            "meal_count": len(meals)
        }
    }
