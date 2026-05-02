# NocoBase 学习平台 - 部署指南

## 🎯 推荐部署方案：Render 免费部署

这是最简单且功能最全的免费方案！

---

## 🚀 方案一：Render 部署（推荐）

### 1. 准备 GitHub 仓库
- 将你的代码推送到 GitHub 仓库
- 确保 `render.yaml` 在仓库根目录

### 2. 注册 Render
访问：https://render.com
- 用 GitHub 账号注册（免费）

### 3. 一键部署
1. 点击 "New +" → "Blueprint"
2. 连接你的 GitHub 仓库
3. 选择你的仓库
4. 自动识别 `render.yaml` 配置
5. 点击 "Apply"

### 4. 等待部署
- 首次部署可能需要 5-10 分钟
- 部署完成后会给你两个 URL：
  - 前端：`https://nocobase-learning-frontend.onrender.com`
  - 后端：`https://nocobase-learning-backend.onrender.com`

---

## 🎨 方案二：Vercel + Render 部署

### 前端部署到 Vercel
1. 访问 https://vercel.com
2. 用 GitHub 登录
3. 导入仓库
4. 配置环境变量：
   - `VITE_API_URL` = `https://your-backend.onrender.com`
5. 部署！

### 后端部署到 Render
参考方案一部署后端部分。

---

## 🐳 方案三：本地 Docker 部署

### 1. 确保已安装 Docker 和 Docker Compose

### 2. 创建 docker-compose.yml（如果没有的话）
在项目根目录创建：
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
    depends_on:
      - backend
    restart: unless-stopped
```

### 3. 启动
```bash
docker-compose up -d
```

---

## 📊 免费方案对比

| 平台 | 前端 | 后端 | 免费额度 | 优点 | 缺点 |
|------|------|------|---------|------|------|
| **Render** | ✅ | ✅ | 750小时/月 | 一键部署，前后端一起 | 冷启动较慢 |
| **Vercel** | ✅ | ❌ | 无限 | 极速，CDN全球分布 | 无后端 |
| **Netlify** | ✅ | ❌ | 无限 | 类似Vercel | 无后端 |
| **Railway** | ✅ | ✅ | $5/月 | 简单易用 | 额度有限 |
| **Fly.io** | ✅ | ✅ | 3个应用 | 全球节点 | 需要信用卡 |

---

## ⚙️ 环境变量配置

### 前端 .env 配置
在 `frontend/` 目录创建 `.env`：
```env
VITE_API_URL=https://your-backend.onrender.com
```

### 后端不需要特别配置

---

## 🔧 部署后验证

1. 访问前端 URL，确保页面正常
2. 尝试提交一个问题，确保 API 连通
3. 检查是否能正常获取数据

---

## 💡 小提示

### Render 免费额度
- 每月 750 小时（持续运行）
- 免费 500MB 存储空间
- 每月 100GB 带宽
- 支持自动 CI/CD

### 数据持久化
⚠️ **注意：** 
- Render 免费层**不会持久化 SQLite 数据库文件**
- 如果需要数据持久化，建议：
  1. 使用 Render 提供的 PostgreSQL 数据库
  2. 或者使用付费层
  3. 或者定期手动备份数据库文件

---

## ❓ 遇到问题？

1. 查看 Render 日志：Dashboard → 你的服务 → Logs
2. 检查 GitHub 仓库是否正确配置
3. 确保 render.yaml 在根目录
4. 尝试重新部署

---

## 🎊 恭喜！

部署成功后，你就有了自己的 NocoBase 学习平台！