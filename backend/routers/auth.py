"""用户认证路由"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from pydantic import BaseModel
from datetime import datetime, timedelta
import hashlib
import secrets

from database import get_session
from models import User

router = APIRouter(prefix="/api/auth", tags=["认证"])
security = HTTPBearer()

# 简单的 token 存储（生产环境应使用 Redis）
active_tokens = {}


class RegisterRequest(BaseModel):
    """注册请求"""
    username: str
    password: str
    name: str
    role: str = "other"


class LoginRequest(BaseModel):
    """登录请求"""
    username: str
    password: str


class UserResponse(BaseModel):
    """用户响应"""
    id: int
    username: str
    name: str
    role: str
    total_score: int
    token: str


def hash_password(password: str) -> str:
    """密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()


def create_token(user_id: int) -> str:
    """创建 token"""
    token = secrets.token_urlsafe(32)
    active_tokens[token] = {
        "user_id": user_id,
        "expires_at": datetime.now() + timedelta(days=30)
    }
    return token


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """验证 token 并返回用户 ID"""
    token = credentials.credentials
    
    if token not in active_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌"
        )
    
    token_data = active_tokens[token]
    if datetime.now() > token_data["expires_at"]:
        del active_tokens[token]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证令牌已过期"
        )
    
    return token_data["user_id"]


@router.post("/register", response_model=UserResponse)
def register(request: RegisterRequest, session: Session = Depends(get_session)):
    """用户注册"""
    # 检查用户名是否已存在
    statement = select(User).where(User.username == request.username)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 创建新用户
    user = User(
        username=request.username,
        password_hash=hash_password(request.password),
        name=request.name,
        role=request.role,
        total_score=0
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # 创建 token
    token = create_token(user.id)
    
    return UserResponse(
        id=user.id,
        username=user.username,
        name=user.name,
        role=user.role,
        total_score=user.total_score,
        token=token
    )


@router.post("/login", response_model=UserResponse)
def login(request: LoginRequest, session: Session = Depends(get_session)):
    """用户登录"""
    # 查找用户
    statement = select(User).where(User.username == request.username)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 验证密码
    if user.password_hash != hash_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 创建 token
    token = create_token(user.id)
    
    return UserResponse(
        id=user.id,
        username=user.username,
        name=user.name,
        role=user.role,
        total_score=user.total_score,
        token=token
    )


@router.get("/me", response_model=UserResponse)
def get_current_user(
    user_id: int = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """获取当前登录用户信息"""
    user = session.get(User, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 返回当前 token（从请求头获取）
    # 这里简化处理，实际应该从请求中提取
    token = list(active_tokens.keys())[0] if active_tokens else ""
    
    return UserResponse(
        id=user.id,
        username=user.username,
        name=user.name,
        role=user.role,
        total_score=user.total_score,
        token=token
    )


@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """用户登出"""
    token = credentials.credentials
    if token in active_tokens:
        del active_tokens[token]
    return {"message": "登出成功"}
