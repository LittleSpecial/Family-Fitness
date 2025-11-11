# FamilyFit 健康助手 - 部署指南

## 🚀 快速部署（推荐：使用 Docker）

### 前提条件
- 安装 Docker 和 Docker Compose
- 准备一台云服务器（如阿里云、腾讯云）或使用本地电脑

### 1. 部署步骤

```bash
# 1. 克隆或上传代码到服务器
git clone <你的仓库地址>
cd health

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 QWEN_API_KEY

# 3. 构建前端
cd frontend
npm install
npm run build
cd ..

# 4. 启动服务（Docker）
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 2. 访问应用
- 在浏览器打开：`http://你的服务器IP`
- 后端 API 文档：`http://你的服务器IP/docs`

---

## 📱 方式一：局域网部署（适合家庭使用）

适合：家人都在同一 WiFi 下使用

```bash
# 1. 在你的电脑上启动
./deploy.sh

# 2. 启动后端
source venv/bin/activate
cd backend && python3 main.py &

# 3. 安装并启动前端服务器
npm install -g serve
cd frontend && serve -s dist -l 80

# 4. 查看你的电脑 IP
ifconfig | grep "inet " | grep -v 127.0.0.1

# 5. 家人访问：http://你的电脑IP
```

---

## ☁️ 方式二：云服务器部署（推荐）

适合：随时随地访问

### 购买云服务器
推荐配置：
- **最低配置**：1核2G（约 ¥70/月）
- **推荐配置**：2核4G（约 ¥150/月）
- **系统**：Ubuntu 22.04 或 CentOS 8

### 部署到阿里云/腾讯云

```bash
# 1. SSH 登录服务器
ssh root@你的服务器IP

# 2. 安装 Docker
curl -fsSL https://get.docker.com | bash
systemctl start docker
systemctl enable docker

# 3. 安装 Docker Compose
apt install docker-compose -y  # Ubuntu
# 或
yum install docker-compose -y  # CentOS

# 4. 上传代码（使用 git 或 scp）
git clone <你的仓库>
cd health

# 5. 配置并启动
cp .env.example .env
vim .env  # 填入 API Key

# 构建前端
cd frontend
npm install
npm run build
cd ..

# 启动服务
docker-compose up -d

# 6. 配置防火墙
ufw allow 80  # Ubuntu
# 或
firewall-cmd --add-port=80/tcp --permanent  # CentOS
firewall-cmd --reload
```

### 绑定域名（可选）
1. 购买域名（如 `family-health.com`）
2. 在域名控制台添加 A 记录指向服务器 IP
3. 修改 `nginx.conf` 中的 `server_name`
4. 重启服务：`docker-compose restart`

---

## 🔐 安全建议

### 1. 设置访问密码（推荐）
在 nginx.conf 中添加基本认证：

```nginx
location / {
    auth_basic "FamilyFit 健康助手";
    auth_basic_user_file /etc/nginx/.htpasswd;
    # ...
}
```

生成密码文件：
```bash
apt install apache2-utils -y
htpasswd -c .htpasswd family
# 输入密码
```

### 2. 启用 HTTPS（强烈推荐）
```bash
# 安装 certbot
apt install certbot python3-certbot-nginx -y

# 获取免费 SSL 证书
certbot --nginx -d 你的域名
```

---

## 📊 性能优化

### 1. 启用 Gzip 压缩
在 nginx.conf 添加：
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

### 2. 设置缓存
```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 7d;
}
```

---

## 🛠️ 维护命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 更新代码后重新部署
git pull
cd frontend && npm run build && cd ..
docker-compose up -d --build

# 备份数据库
cp data/health.db backup/health_$(date +%Y%m%d).db
```

---

## 🎯 最简单的方案（零配置）

如果觉得复杂，可以使用 **Vercel + Railway** 免费部署：

1. **前端部署到 Vercel**
   - 登录 https://vercel.com
   - 导入 GitHub 仓库
   - 设置 Build Command: `cd frontend && npm run build`
   - 设置 Output Directory: `frontend/dist`

2. **后端部署到 Railway**
   - 登录 https://railway.app
   - 新建项目，选择 GitHub 仓库
   - 添加环境变量 `QWEN_API_KEY`
   - 自动部署

免费额度：
- Vercel: 100GB 带宽/月
- Railway: $5 免费额度/月

---

## ❓ 常见问题

**Q: 家人无法访问？**
A: 检查防火墙是否开放 80 端口，确保设备在同一网络

**Q: API 调用失败？**
A: 检查 .env 文件中的 API Key 是否正确

**Q: 前端显示空白？**
A: 检查前端是否正确构建：`cd frontend && npm run build`

**Q: 数据会丢失吗？**
A: 数据存储在 `data/health.db`，定期备份即可

---

## 📞 技术支持

如有问题，检查日志：
```bash
docker-compose logs -f
```
