#!/bin/bash
# FamilyFit 阿里云一键部署脚本

echo "======================================"
echo "   FamilyFit 健康助手 - 一键部署"
echo "======================================"
echo ""

# 更新系统
echo "📦 更新系统..."
apt update && apt upgrade -y

# 安装 Docker
echo "🐳 安装 Docker..."
curl -fsSL https://get.docker.com | bash

# 配置 Docker 阿里云镜像加速
echo "⚡ 配置 Docker 镜像加速..."
mkdir -p /etc/docker
cat > /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com",
    "https://registry.docker-cn.com"
  ]
}
EOF

systemctl start docker
systemctl enable docker
systemctl daemon-reload
systemctl restart docker

# 安装 Docker Compose
echo "📦 安装 Docker Compose..."
apt install docker-compose -y

# 安装 Git
echo "📦 安装 Git..."
apt install git -y

# 克隆项目
echo "📥 下载项目代码..."
cd /root
git clone https://github.com/LittleSpecial/Family-Fitness.git
cd Family-Fitness

# 配置环境变量
echo "⚙️  配置环境变量..."
cat > .env << EOF
QWEN_API_KEY=sk-cd52e8a0a2724a2586ea6d8d91536770
EOF

# 构建前端
echo "🏗️  构建前端..."
cd frontend
docker run --rm -v $(pwd):/app -w /app node:20-alpine sh -c "npm install && npm run build"
cd ..

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

# 开放防火墙端口
echo "🔥 配置防火墙..."
ufw allow 80
ufw allow 8000
ufw --force enable

echo ""
echo "======================================"
echo "✅ 部署完成！"
echo "======================================"
echo ""
echo "访问地址："
echo "前端：http://$(curl -s ip.sb)"
echo "后端：http://$(curl -s ip.sb):8000"
echo ""
echo "查看日志：docker-compose logs -f"
echo "重启服务：docker-compose restart"
echo "停止服务：docker-compose down"
echo ""
