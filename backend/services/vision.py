"""运动截图 Vision 识别服务"""
import base64
import json
import httpx
from datetime import date, datetime
from typing import Dict, Optional
from config import settings


# Vision 模型提示词
VISION_PROMPT = """你是一个专业的运动数据识别助手。请仔细观察这张运动记录截图，准确读取每个字段。

⚠️ 关键识别步骤：

第一步 - 识别运动类型（最重要）：
1. 仔细查看图片最顶部或中心位置的大字标题
2. 注意查看运动图标（如果有的话）
3. 运动类型通常用较大的字体显示在截图顶部
4. 【重要】必须完全按照图中显示的文字识别，一字不差
5. 如果看到"网球"就返回"网球"，看到"跑步"就返回"跑步"，看到"骑行"就返回"骑行"
6. 绝对不能猜测或推断，必须是图中明确显示的文字

第二步 - 读取时间数据：
1. 查找"时间""时长""用时"等字样
2. 格式可能是：MM:SS或 HH:MM:SS
3. 转换为总分钟数（整数）

第三步 - 读取卡路里：
1. 查找"卡路里""千卡""kcal"等字样
2. 数值可能带千位分隔符

第四步 - 读取可选数据（如果图中有）：
1. 步数：查找"步""步数"字样
2. 平均心率：查找"平均心率""avg""bpm"等，通常在心率区间附近
3. 最大心率：查找"最大心率""max"等
4. 距离、配速等其他数据（暂不需要）

第五步 - 判断设备来源：
1. 华为：绿色主题、华为运动健康 logo、华为字样
2. 苹果：Apple Watch、Apple Fitness 界面风格
3. 其他：标记为 unknown

请严格按此 JSON 格式返回（只返回 JSON，不要其他文字）：

{
  "exercise_type": "运动类型名称（中文，必须是图中显示的原始文字）",
  "duration_min": 运动时长分钟数(整数),
  "calories": 消耗卡路里(整数),
  "steps": 步数(整数或null),
  "avg_heart_rate": 平均心率(整数或null),
  "max_heart_rate": 最大心率(整数或null),
  "date": "YYYY-MM-DD或null",
  "source_device": "huawei/apple/unknown"
}"""


async def parse_exercise_screenshot(image_bytes: bytes) -> Dict:
    """
    解析运动截图,提取运动数据
    
    Args:
        image_bytes: 图片字节流
    
    Returns:
        包含运动数据的字典
    
    Raises:
        Exception: 识别失败时抛出异常
    """
    # 转换为 base64
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # 构建 API 请求
    headers = {
        "Authorization": f"Bearer {settings.QWEN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 千问 VL 模型的消息格式
    payload = {
        "model": settings.VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": VISION_PROMPT},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
            }
        ],
        "temperature": settings.VISION_TEMPERATURE,
        "max_tokens": settings.VISION_MAX_TOKENS
    }
    
    # 调用千问 Vision API
    async with httpx.AsyncClient(timeout=settings.API_TIMEOUT) as client:
        response = await client.post(
            f"{settings.QWEN_API_URL}/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"API 调用失败: {response.status_code} - {response.text}")
        
        result = response.json()
    
    # 解析返回的 JSON
    try:
        # 千问模型的标准响应格式
        message = result["choices"][0]["message"]
        content = message.get("content", "")
        
        # 提取 JSON 部分(可能包含其他文本)
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        if json_start != -1 and json_end != 0:
            json_str = content[json_start:json_end]
            data = json.loads(json_str)
        else:
            raise ValueError("无法从响应中提取 JSON 数据")
    except (KeyError, json.JSONDecodeError, ValueError) as e:
        # 打印完整的响应以便调试
        print(f"解析错误: {str(e)}")
        print(f"完整响应: {result}")
        raise Exception(f"JSON 解析失败: {str(e)}")
    
    # 数据验证和补充
    validated_data = validate_and_fix_data(data)
    
    return validated_data


def validate_and_fix_data(data: Dict) -> Dict:
    """
    验证和修正识别数据
    
    Args:
        data: 原始识别数据
    
    Returns:
        验证后的数据
    
    Raises:
        ValueError: 数据验证失败
    """
    # 必填字段验证
    exercise_type = data.get("exercise_type")
    if not exercise_type or not isinstance(exercise_type, str):
        print(f"运动类型验证失败: {exercise_type}, 类型: {type(exercise_type)}")
        print(f"完整数据: {data}")
        raise ValueError("运动类型缺失或格式错误")
    
    duration_min = data.get("duration_min")
    if not duration_min or not isinstance(duration_min, int) or duration_min < 1 or duration_min > 600:
        raise ValueError("运动时长数据无效")
    
    calories = data.get("calories")
    if calories is None or not isinstance(calories, int) or calories < 0 or calories > 10000:
        raise ValueError("卡路里数据无效")
    
    # 可选字段验证
    steps = data.get("steps")
    if steps is not None and (not isinstance(steps, int) or steps < 0):
        steps = None
    
    avg_heart_rate = data.get("avg_heart_rate")
    if avg_heart_rate is not None:
        if not isinstance(avg_heart_rate, int) or avg_heart_rate < 40 or avg_heart_rate > 220:
            avg_heart_rate = None
    
    max_heart_rate = data.get("max_heart_rate")
    if max_heart_rate is not None:
        if not isinstance(max_heart_rate, int) or max_heart_rate < 50 or max_heart_rate > 250:
            max_heart_rate = None
    
    # 日期处理
    date_str = data.get("date")
    if date_str:
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            # 检查日期范围
            if parsed_date < date(2020, 1, 1) or parsed_date > date.today():
                parsed_date = date.today()
        except ValueError:
            parsed_date = date.today()
    else:
        parsed_date = date.today()
    
    # 设备来源
    source_device = data.get("source_device", "unknown")
    if source_device not in ["apple", "huawei", "unknown"]:
        source_device = "unknown"
    
    return {
        "exercise_type": exercise_type,
        "duration_min": duration_min,
        "calories": calories,
        "steps": steps,
        "avg_heart_rate": avg_heart_rate,
        "max_heart_rate": max_heart_rate,
        "date": parsed_date,
        "source_device": source_device
    }
