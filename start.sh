#!/bin/bash

# FamilyFit 健康助手 - 快速启动脚本

echo "======================================"
echo "   FamilyFit 健康助手 启动向导"
echo "======================================"
echo ""

if [ -f ".env" ]; then
    echo "📝 加载 .env 配置文件..."
    export $(cat .env | grep -v '#' | xargs)
    echo "✅ 配置加载完成"
    echo ""
fi

# 检查 DeepSeek API Key
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo "⚠️  警告: 未设置 DEEPSEEK_API_KEY"
    echo "请创建 .env 文件并设置: DEEPSEEK_API_KEY=your_api_key"
    echo "或者运行: export DEEPSEEK_API_KEY=your_api_key"
    echo ""
    read -p "是否继续? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "📦 安装后端依赖..."
pip3 install -r requirements.txt

echo ""
echo "📦 安装前端依赖..."
cd frontend
npm install
cd ..

echo ""
echo "✅ 依赖安装完成!"
echo ""
echo "🚀 启动说明:"
echo ""
echo "1. 启动后端 (在新终端中运行):"
echo "   cd backend && python3 main.py"
echo ""
echo "2. 启动前端 (在新终端中运行):"
echo "   cd frontend && npm run dev"
echo ""
echo "3. 访问应用:"
echo "   前端: http://localhost:5173"
echo "   后端API文档: http://localhost:8000/docs"
echo ""
echo "======================================"
