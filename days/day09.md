# Day 9：部署与运维

> **学习目标：** 掌握版本升级、数据备份恢复、数据库配置
> **预计时间：** 1.5 小时
> **难度：** 🔴 重点

---

## 📖 学习内容

### 1. 版本升级

#### 升级前准备

1. **备份数据**（重要！）
2. 查看更新日志
3. 确认兼容性

#### Docker 升级步骤

```bash
# 1. 停止服务
docker compose down

# 2. 备份数据
cp -r storage storage_backup_$(date +%Y%m%d)

# 3. 拉取最新镜像
docker compose pull

# 4. 启动服务
docker compose up -d

# 5. 查看日志
docker compose logs -f app
```

#### 版本选择

| 版本 | 说明 | 适用场景 |
|------|------|----------|
| latest | 稳定版 | 生产环境 |
| beta | 测试版 | 测试环境 |
| alpha | 开发版 | 开发体验 |

---

### 2. 数据备份与恢复

#### 备份方式

**方式 1：文件备份**
```bash
# 备份整个 storage 目录
tar -czvf nocobase_backup_$(date +%Y%m%d).tar.gz storage/
```

**方式 2：数据库备份**
```bash
# PostgreSQL
docker compose exec db pg_dump -U nocobase nocobase > backup.sql

# MySQL
docker compose exec db mysqldump -u nocobase -p nocobase > backup.sql
```

#### 恢复数据

**恢复文件：**
```bash
tar -xzvf nocobase_backup_20260501.tar.gz
```

**恢复数据库：**
```bash
# PostgreSQL
docker compose exec -T db psql -U nocobase nocobase < backup.sql

# MySQL
docker compose exec -T db mysql -u nocobase -p nocobase < backup.sql
```

---

### 3. 数据库配置

#### PostgreSQL 配置

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: nocobase
      POSTGRES_USER: nocobase
      POSTGRES_PASSWORD: your_password
    volumes:
      - ./storage/db:/var/lib/postgresql/data
```

#### MySQL 配置

```yaml
services:
  db:
    image: mysql:8
    environment:
      MYSQL_DATABASE: nocobase
      MYSQL_USER: nocobase
      MYSQL_PASSWORD: your_password
      MYSQL_ROOT_PASSWORD: root_password
    volumes:
      - ./storage/db:/var/lib/mysql
```

---

### 4. 环境变量

#### 常用环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| NODE_ENV | 运行环境 | production |
| APP_PORT | 应用端口 | 13000 |
| DB_DATABASE | 数据库名 | nocobase |
| DB_USER | 数据库用户 | nocobase |
| DB_PASSWORD | 数据库密码 | - |
| SECRET_KEY | 加密密钥 | 自动生成 |

#### 配置示例

```yaml
environment:
  - NODE_ENV=production
  - APP_PORT=13000
  - DB_DATABASE=nocobase
  - DB_USER=nocobase
  - DB_PASSWORD=your_secure_password
  - SECRET_KEY=your_secret_key_here
```

---

### 5. 性能优化

#### 数据库优化

- 配置连接池
- 添加索引
- 定期清理日志

#### 应用优化

- 启用缓存
- 配置 CDN
- 负载均衡

---

### 6. 日志管理

#### 查看日志

```bash
# 查看应用日志
docker compose logs -f app

# 查看数据库日志
docker compose logs -f db

# 查看最近 100 行
docker compose logs --tail 100 app
```

#### 日志位置

```
storage/logs/
├── app.log      # 应用日志
├── access.log   # 访问日志
└── error.log    # 错误日志
```

---

## 🎯 练习题

### 问题 1：升级前为什么要备份数据？

### 问题 2：如何备份和恢复 PostgreSQL 数据库？

### 问题 3：常用的环境变量有哪些？

### 问题 4：动手练习 - 执行一次完整的数据备份

---

## 📚 扩展阅读

- [安装升级文档](https://docs.nocobase.com/cn/get-started/installation/docker)
- [环境变量](https://docs.nocobase.com/cn/get-started/environment-variables)

---

## ✅ 今日任务

- [ ] 了解版本升级流程
- [ ] 掌握数据备份方法
- [ ] 掌握数据恢复方法
- [ ] 了解数据库配置
- [ ] 了解常用环境变量

---

*完成学习后，请回答练习题，我会帮你更新进度！*
