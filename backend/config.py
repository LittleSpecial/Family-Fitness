import os
from typing import List
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

class Settings:
    """应用配置类"""
    
    # 阿里云百炼平台 API 配置
    QWEN_API_KEY: str = os.getenv("QWEN_API_KEY", "")
    QWEN_API_URL: str = os.getenv("QWEN_API_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/health.db")
    
    # 文件上传配置
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    
    # CORS 配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]
    
    # API 超时配置
    API_TIMEOUT: int = 30
    
    # Vision API 参数
    VISION_MODEL: str = "qwen-vl-max-latest"  # 千问 VL 多模态模型
    VISION_TEMPERATURE: float = 0.1
    VISION_MAX_TOKENS: int = 1000
    
    # 饮食分析 API 参数
    DIET_MODEL: str = "qwen-plus-latest"  # 千问文本模型
    DIET_TEMPERATURE: float = 0.3
    DIET_MAX_TOKENS: int = 1500

settings = Settings()

# 确保上传目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs("./data", exist_ok=True)
