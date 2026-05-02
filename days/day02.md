# Day 2：Docker 安装部署

> **学习目标：** 掌握 NocoBase 的 Docker 安装和基本运维
> **预计时间：** 1.5 小时
> **难度：** 🟢 基础

---

## 📖 学习内容

### 1. 前提条件

在开始之前，确保你的电脑已安装：
- **Docker**：容器运行环境
- **Docker Compose**：容器编排工具

**安装 Docker：**
- Windows/Mac：下载 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Linux：参考 [Docker 官方文档](https://docs.docker.com/engine/install/)

**验证安装：**
```bash
docker --version
docker compose version
```

---

### 2. 快速安装（推荐）

#### 第一步：创建项目目录

```bash
mkdir my-nocobase && cd my-nocobase
```

#### 第二步：下载配置文件

```bash
# PostgreSQL 版本（推荐）
curl -fsSL https://static-docs.nocobase.com/docker-compose/cn/latest-postgres.yml -o docker-compose.yml

# 或 MySQL 版本
curl -fsSL https://static-docs.nocobase.com/docker-compose/cn/latest-mysql.yml -o docker-compose.yml
```

#### 第三步：启动服务

```bash
# 拉取镜像
docker compose pull

# 后台启动
docker compose up -d

# 查看日志
docker compose logs -f app
```

看到以下输出表示启动成功：
```
🚀 NocoBase server running at: http://localhost:13000/
```

#### 第四步：登录

- 访问：`http://localhost:13000`
- 账号：`admin@nocobase.com`
- 密码：`admin123`

**⚠️ 重要：首次登录后请立即修改默认密码！**

---

### 3. 常用 Docker 命令

```bash
# 查看运行中的容器
docker compose ps

# 查看日志
docker compose logs -f app

# 停止服务
docker compose down

# 重启服务
docker compose restart

# 进入容器
docker compose exec app sh

# 查看容器资源使用
docker stats
```

---

### 4. 目录结构

```
my-nocobase/
├── docker-compose.yml    # Docker 配置文件
└── storage/              # 数据存储目录（自动创建）
    ├── db/               # 数据库文件
    ├── uploads/          # 上传文件
    └── logs/             # 日志文件
```

---

### 5. 环境变量配置

在 `docker-compose.yml` 中可以配置：

```yaml
environment:
  - NODE_ENV=production
  - DB_DATABASE=nocobase
  - DB_USER=nocobase
  - DB_PASSWORD=your_password
  - APP_PORT=13000
```

---

### 6. 常见启动问题排查

#### 问题 1：端口被占用

**错误信息：**
```
Error: port 13000 is already in use
```

**解决方案：**
```bash
# 查看端口占用
lsof -i :13000  # Mac/Linux
netstat -ano | findstr :13000  # Windows

# 修改端口（在 docker-compose.yml 中）
APP_PORT=13001
```

#### 问题 2：Docker 未启动

**错误信息：**
```
Cannot connect to the Docker daemon
```

**解决方案：**
- 确保 Docker Desktop 正在运行
- Linux 上执行：`sudo systemctl start docker`

#### 问题 3：镜像拉取失败

**解决方案：**
```bash
# 使用国内镜像源
docker pull registry.cn-hangzhou.aliyuncs.com/nocobase/nocobase:latest
```

---

### 7. 数据持久化

**重要：** 生产环境必须配置数据持久化！

```yaml
volumes:
  - ./storage/db:/app/storage/db
  - ./storage/uploads:/app/storage/uploads
  - ./storage/logs:/app/storage/logs
```

---

## 🎯 练习题

### 问题 1：如何查看 NocoBase 的运行日志？

### 问题 2：默认的登录账号密码是什么？为什么要修改？

### 问题 3：如何解决端口被占用的问题？

### 问题 4：数据持久化为什么重要？

---

## 📚 扩展阅读

- [Docker 安装详解](https://docs.nocobase.com/cn/get-started/installation/docker)
- [系统要求](https://docs.nocobase.com/cn/get-started/system-requirements)

---

## ✅ 今日任务

- [ ] 安装 Docker 和 Docker Compose
- [ ] 使用 Docker 安装 NocoBase
- [ ] 成功登录并修改默认密码
- [ ] 练习常用 Docker 命令
- [ ] 了解数据持久化配置

---

*完成学习后，请回答练习题，我会帮你更新进度！*
