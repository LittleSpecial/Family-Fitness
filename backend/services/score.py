"""运动得分计算服务"""

def calculate_score(record: dict) -> int:
    """
    计算运动得分
    
    Args:
        record: 运动记录字典,包含 duration_min, calories, avg_heart_rate, exercise_type, steps
    
    Returns:
        整数得分 (0-100)
    """
    exercise_type = record.get("exercise_type", "")
    
    # 判断是否为每日步数总结
    if exercise_type == "每日步数":
        return calculate_daily_steps_score(record)
    
    # 单次运动记录的评分逻辑
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
    type_bonus = {
        "羽毛球": 5,
        "篮球": 5,
        "游泳": 8,
        "跑步": 3,
        "骑行": 3,
    }
    exercise_type_lower = exercise_type.lower()
    for key, bonus in type_bonus.items():
        if key in exercise_type_lower:
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


def calculate_daily_steps_score(record: dict) -> int:
    """
    计算每日步数总结的得分
    
    Args:
        record: 包含 steps, calories 等字段的字典
    
    Returns:
        整数得分 (0-100)
    """
    score = 0.0
    
    # 1. 步数得分（主要指标）
    steps = record.get("steps", 0)
    if steps >= 20000:
        score += 50  # 超过2万步，满分
    elif steps >= 15000:
        score += 40  # 1.5万-2万步
    elif steps >= 10000:
        score += 30  # 1万-1.5万步
    elif steps >= 5000:
        score += 20  # 5千-1万步
    else:
        score += steps / 250  # 低于5千步，按比例计算
    
    # 2. 卡路里得分
    calories = record.get("calories", 0)
    if calories >= 1000:
        score += 30
    elif calories >= 600:
        score += 20
    elif calories >= 300:
        score += 10
    else:
        score += calories / 30
    
    # 3. 活跃度加分（步数和卡路里都高）
    if steps >= 15000 and calories >= 600:
        score += 20  # 双高奖励
    
    # 确保得分在 0-100 范围内
    final_score = min(int(round(score)), 100)
    return max(final_score, 0)
