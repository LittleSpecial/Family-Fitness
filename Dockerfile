# FamilyFit 健康助手 - Docker 镜像

FROM python:3.11-slim

WORKDIR /app

# 配置阿里云镜像源加速
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制后端代码
COPY backend/ ./backend/
COPY requirements.txt .
COPY .env .

# 安装 Python 依赖（使用阿里云 PyPI 镜像）
RUN pip3 install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# 创建必要的目录
RUN mkdir -p data uploads

# 暴露端口
EXPOSE 8000

# 启动后端
CMD ["python3", "backend/main.py"]
