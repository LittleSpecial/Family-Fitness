# FamilyFit 健康助手

一款简单易用的健康管理应用,支持运动截图识别、饮食健康分析、每日任务打卡和健康趋势可视化。

## 功能特点

✅ **运动记录识别**: 上传华为/Apple设备运动截图,AI自动识别运动数据并评分
✅ **饮食健康分析**: 记录每日饮食,AI分析营养健康度并提供改进建议  
✅ **每日健康任务**: 系统自动生成5个健康任务,完成后获得积分奖励
✅ **健康趋势展示**: 可视化展示运动、饮食、任务完成趋势数据

## 技术栈

### 后端
- FastAPI
- SQLModel (ORM)
- SQLite (数据库)
- DeepSeek API (AI识别)

### 前端
- Vue 3 + Composition API
- Vite
- Chart.js (图表)
- Axios (HTTP客户端)

## 快速开始

### 1. 环境要求

- Python 3.10+
- Node.js 16+
- DeepSeek API Key

### 2. 配置环境变量

创建 `.env` 文件(可选,也可直接设置环境变量):

```bash
export DEEPSEEK_API_KEY=your_api_key_here
```

### 3. 启动后端

```bash
# 安装依赖
pip install -r requirements.txt

# 启动后端服务
cd backend
python main.py
```

后端服务将在 http://localhost:8000 启动

### 4. 启动前端

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将在 http://localhost:5173 启动

## API 文档

启动后端后,访问 http://localhost:8000/docs 查看完整API文档

### 主要接口

- `POST /api/parse_report` - 上传运动截图识别
- `POST /api/meals/add` - 添加饮食记录
- `GET /api/tasks/today` - 获取今日任务
- `POST /api/tasks/done` - 完成任务
- `GET /api/trends` - 获取健康趋势数据

## 项目结构

```
health/
├─ backend/              # 后端代码
│   ├─ main.py          # FastAPI应用入口
│   ├─ models.py        # 数据模型
│   ├─ database.py      # 数据库配置
│   ├─ config.py        # 配置文件
│   ├─ routers/         # API路由
│   └─ services/        # 业务服务层
├─ frontend/            # 前端代码
│   ├─ src/
│   │   ├─ pages/       # 页面组件
│   │   ├─ components/  # 通用组件
│   │   ├─ api/         # API封装
│   │   └─ router/      # 路由配置
│   └─ package.json
├─ data/                # SQLite数据库文件
└─ requirements.txt     # Python依赖
```

## 使用说明

### 运动记录

1. 进入"运动上传"页面
2. 点击上传运动截图(支持华为/Apple设备截图)
3. 等待AI识别(约5-10秒)
4. 查看识别结果和运动得分

### 饮食记录

1. 进入"饮食记录"页面
2. 选择餐次(早餐/午餐/晚餐/加餐)
3. 添加食物名称和份量
4. 点击"分析健康度"
5. 查看健康得分和改进建议

### 每日任务

1. 进入"今日任务"页面
2. 查看系统生成的5个健康任务
3. 完成后点击任务打卡
4. 获得积分奖励

### 健康趋势

1. 进入"健康趋势"页面
2. 选择查看近7天或近30天数据
3. 查看各项健康指标趋势图表

## 注意事项

⚠️ 需要配置有效的 DeepSeek API Key
⚠️ 首次运行会自动创建数据库表
⚠️ 默认创建测试用户(ID=1)
⚠️ 上传图片大小限制10MB

## 许可证

MIT License
