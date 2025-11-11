#!/bin/bash

# FamilyFit 健康助手 - 生产环境部署脚本

echo "======================================"
echo "   FamilyFit 生产环境部署"
echo "======================================"
echo ""

# 检查环境变量
if [ ! -f ".env" ]; then
    echo "❌ 错误: .env 文件不存在"
    echo "请先复制 .env.example 为 .env 并配置"
    exit 1
fi

# 安装后端依赖
echo "📦 安装后端依赖..."
pip3 install -r requirements.txt

# 构建前端
echo ""
echo "🏗️  构建前端..."
cd frontend
npm install
npm run build
cd ..

echo ""
echo "✅ 部署准备完成!"
echo ""
echo "启动方式："
echo "1. 后端: python3 backend/main.py"
echo "2. 前端: 使用 nginx 或其他 Web 服务器托管 frontend/dist 目录"
echo ""
echo "建议使用 supervisor 或 systemd 管理后端进程"
echo "======================================"
