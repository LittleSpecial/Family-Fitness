"""运动得分计算服务"""

def calculate_score(record: dict) -> int:
    """
    计算运动得分
    
    Args:
        record: 运动记录字典,包含 duration_min, calories, avg_heart_rate, exercise_type, steps
    
    Returns:
        整数得分 (0-100)
    """
    score = 0.0
    
    # 1. 时长得分: duration_min / 3 (运动 30 分钟 = 10 分)
    duration_min = record.get("duration_min", 0)
    score += duration_min / 3
    
    # 2. 卡路里得分: calories / 25 (消耗 250 卡路里 = 10 分)
    calories = record.get("calories", 0)
    score += calories / 25
    
    # 3. 心率得分: avg_heart_rate / 20 (平均心率 120 = 6 分)
    avg_heart_rate = record.get("avg_heart_rate")
    if avg_heart_rate:
        score += avg_heart_rate / 20
    
    # 4. 运动类型加分
    exercise_type = record.get("exercise_type", "").lower()
    type_bonus = {
        "羽毛球": 5,
        "篮球": 5,
        "游泳": 8,
        "跑步": 3,
        "骑行": 3,
    }
    for key, bonus in type_bonus.items():
        if key in exercise_type:
            score += bonus
            break
    
    # 5. 步数加分
    steps = record.get("steps")
    if steps:
        if steps > 10000:
            score += 5
        elif steps > 5000:
            score += 3
    
    # 确保得分在 0-100 范围内
    final_score = min(int(round(score)), 100)
    return max(final_score, 0)
