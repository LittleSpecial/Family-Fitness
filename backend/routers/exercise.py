"""运动相关路由"""
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlmodel import Session
from datetime import date
from database import get_session
from models import ExerciseRecord
from services.vision import parse_exercise_screenshot
from services.score import calculate_score

router = APIRouter(prefix="/api", tags=["exercise"])


@router.post("/parse_report")
async def parse_exercise_report(
    file: UploadFile = File(...),
    user_id: int = Form(...),
    session: Session = Depends(get_session)
):
    """
    上传运动截图并识别数据
    
    Args:
        file: 运动截图文件
        user_id: 用户ID
        session: 数据库会话
    
    Returns:
        识别结果和得分
    """
    # 验证文件类型
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="文件格式不支持,仅支持 jpg/png")
    
    # 读取文件内容
    try:
        image_bytes = await file.read()
        
        # 验证文件大小 (10MB)
        if len(image_bytes) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="文件大小超过限制(最大10MB)")
        
        # 调用 Vision 识别服务
        recognized_data = await parse_exercise_screenshot(image_bytes)
        
        # 计算得分
        score = calculate_score(recognized_data)
        recognized_data["score"] = score
        
        # 保存到数据库
        exercise_record = ExerciseRecord(
            user_id=user_id,
            exercise_type=recognized_data["exercise_type"],
            duration_min=recognized_data["duration_min"],
            calories=recognized_data["calories"],
            steps=recognized_data.get("steps"),
            avg_heart_rate=recognized_data.get("avg_heart_rate"),
            max_heart_rate=recognized_data.get("max_heart_rate"),
            source_device=recognized_data["source_device"],
            date=recognized_data["date"],
            score=score
        )
        
        session.add(exercise_record)
        session.commit()
        session.refresh(exercise_record)
        
        return {
            "success": True,
            "data": {
                "exercise_type": recognized_data["exercise_type"],
                "duration_min": recognized_data["duration_min"],
                "calories": recognized_data["calories"],
                "steps": recognized_data.get("steps"),
                "avg_heart_rate": recognized_data.get("avg_heart_rate"),
                "max_heart_rate": recognized_data.get("max_heart_rate"),
                "score": score,
                "source_device": recognized_data["source_device"],
                "date": str(recognized_data["date"])
            },
            "message": "识别成功"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"识别失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")
