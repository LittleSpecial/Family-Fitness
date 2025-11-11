"""饮食健康分析服务"""
import json
import httpx
from typing import Dict, List
from config import settings


# 饮食分析提示词
DIET_ANALYSIS_PROMPT = """你是一位营养专家,请分析以下这餐的营养健康度。

用户吃了:
{food_items}

请从以下维度评估并返回 JSON 格式:

{{
  "health_score": 健康得分(0-100,整数),
  "total_calories": 估算总卡路里(整数),
  "analysis": "简短的健康分析和建议(50字以内)",
  "nutrition_balance": {{
    "protein": "蛋白质充足/适中/不足",
    "carbs": "碳水化合物充足/适中/不足",
    "vegetables": "蔬菜充足/适中/不足",
    "oil": "油脂过多/适中/较少",
    "sugar": "糖分过多/适中/较少"
  }}
}}

评分标准:
- 营养均衡(蛋白质+碳水+蔬菜): 基础分 60
- 蔬菜丰富: +10 分
- 高蛋白: +5 分
- 少油少盐: +10 分
- 无糖饮料/甜食: +10 分
- 全谷物主食: +5 分
- 油炸食品: -15 分
- 高糖饮料/甜食: -10 分
- 加工肉类过多: -10 分"""


async def analyze_meal_health(food_items: List[Dict]) -> Dict:
    """
    分析饮食健康度
    
    Args:
        food_items: 食物列表,格式: [{"name": "食物名", "amount": "份量"}, ...]
    
    Returns:
        包含健康得分、卡路里、分析等信息的字典
    
    Raises:
        Exception: 分析失败时抛出异常
    """
    # 格式化食物列表为文本
    food_text = "\n".join([f"- {item['name']} {item['amount']}" for item in food_items])
    prompt = DIET_ANALYSIS_PROMPT.format(food_items=food_text)
    
    # 构建 API 请求
    headers = {
        "Authorization": f"Bearer {settings.QWEN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": settings.DIET_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": settings.DIET_TEMPERATURE,
        "max_tokens": settings.DIET_MAX_TOKENS
    }
    
    try:
        # 调用千问 API
        async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
            response = await client.post(
                f"{settings.QWEN_API_URL}/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                raise Exception(f"API 调用失败: {response.status_code}")
            
            result = response.json()
        
        # 解析返回的 JSON
        content = result["choices"][0]["message"]["content"]
        
        # 提取 JSON 部分
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        if json_start != -1 and json_end != 0:
            json_str = content[json_start:json_end]
            data = json.loads(json_str)
        else:
            raise ValueError("无法从响应中提取 JSON 数据")
        
        # 验证数据
        validated_data = validate_meal_analysis(data)
        return validated_data
        
    except Exception as e:
        # 返回默认值
        return {
            "health_score": 50,
            "total_calories": 0,
            "analysis": "分析失败,请稍后重试",
            "nutrition_balance": {
                "protein": "未知",
                "carbs": "未知",
                "vegetables": "未知",
                "oil": "未知",
                "sugar": "未知"
            }
        }


def validate_meal_analysis(data: Dict) -> Dict:
    """
    验证饮食分析数据
    
    Args:
        data: 原始分析数据
    
    Returns:
        验证后的数据
    """
    # 健康得分验证
    health_score = data.get("health_score", 50)
    if not isinstance(health_score, int) or health_score < 0 or health_score > 100:
        health_score = 50
    
    # 卡路里验证
    total_calories = data.get("total_calories", 0)
    if not isinstance(total_calories, int) or total_calories < 0:
        total_calories = 0
    
    # 分析文本验证
    analysis = data.get("analysis", "")
    if not isinstance(analysis, str):
        analysis = ""
    
    # 营养平衡验证
    nutrition_balance = data.get("nutrition_balance", {})
    if not isinstance(nutrition_balance, dict):
        nutrition_balance = {
            "protein": "适中",
            "carbs": "适中",
            "vegetables": "适中",
            "oil": "适中",
            "sugar": "适中"
        }
    
    return {
        "health_score": health_score,
        "total_calories": total_calories,
        "analysis": analysis,
        "nutrition_balance": nutrition_balance
    }
