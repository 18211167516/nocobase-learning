# Day 10：常见问题排查（一）

> **学习目标：** 掌握启动失败、端口占用、数据库连接问题的排查方法
> **预计时间：** 1.5 小时
> **难度：** 🔴 重点

---

## 📖 学习内容

### 1. 问题排查思路

#### 排查流程

```
1. 查看错误信息
↓
2. 查看日志
↓
3. 定位问题原因
↓
4. 查找解决方案
↓
5. 验证修复
```

#### 常用排查命令

```bash
# 查看容器状态
docker compose ps

# 查看容器日志
docker compose logs -f app

# 进入容器
docker compose exec app sh

# 检查端口占用
netstat -tlnp | grep 13000

# 检查磁盘空间
df -h

# 检查内存使用
free -m
```

---

### 2. 启动失败问题

#### 问题 1：容器无法启动

**症状：**
```bash
docker compose ps
# 显示容器状态为 Exited
```

**排查步骤：**
```bash
# 1. 查看容器日志
docker compose logs app

# 2. 查看退出原因
docker inspect <container_id> | grep -A 5 "State"
```

**常见原因：**
- 配置文件错误
- 环境变量缺失
- 数据库连接失败

---

#### 问题 2：启动超时

**症状：**
```
Error: startup timeout
```

**可能原因：**
- 服务器资源不足
- 数据库初始化慢
- 网络问题

**解决方案：**
```yaml
# 增加启动超时时间
environment:
  - STARTUP_TIMEOUT=300000
```

---

### 3. 端口占用问题

#### 症状

```
Error: listen EADDRINUSE: address already in use :::13000
```

#### 排查步骤

```bash
# 查看端口占用
lsof -i :13000        # Mac/Linux
netstat -ano | findstr :13000  # Windows

# 查看占用进程
ps aux | grep <pid>
```

#### 解决方案

**方案 1：停止占用进程**
```bash
kill -9 <pid>
```

**方案 2：更换端口**
```yaml
environment:
  - APP_PORT=13001
ports:
  - "13001:13001"
```

---

### 4. 数据库连接问题

#### 问题 1：数据库连接失败

**症状：**
```
Error: connect ECONNREFUSED 127.0.0.1:5432
```

**排查步骤：**
```bash
# 1. 检查数据库容器是否启动
docker compose ps db

# 2. 检查数据库日志
docker compose logs db

# 3. 测试数据库连接
docker compose exec db psql -U nocobase -d nocobase
```

**常见原因：**
- 数据库容器未启动
- 数据库用户名/密码错误
- 数据库名称错误
- 网络不通

---

#### 问题 2：数据库权限错误

**症状：**
```
Error: permission denied for table xxx
```

**解决方案：**
```sql
-- 授予所有权限
GRANT ALL PRIVILEGES ON DATABASE nocobase TO nocobase;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nocobase;
```

---

### 5. 内存不足问题

#### 症状

```
Error: JavaScript heap out of memory
```

#### 解决方案

```yaml
environment:
  - NODE_OPTIONS=--max-old-space-size=4096
```

---

### 6. 常见错误代码

| 错误代码 | 说明 | 解决方案 |
|----------|------|----------|
| ECONNREFUSED | 连接被拒绝 | 检查服务是否启动 |
| EADDRINUSE | 端口被占用 | 更换端口或停止占用进程 |
| ENOENT | 文件不存在 | 检查文件路径 |
| EACCES | 权限不足 | 检查文件权限 |
| ETIMEDOUT | 连接超时 | 检查网络连接 |

---

## 🎯 练习题

### 问题 1：如何查看 NocoBase 的错误日志？

### 问题 2：端口被占用时如何处理？

### 问题 3：数据库连接失败时如何排查？

### 问题 4：模拟排查一个启动失败的问题

---

## 📚 扩展阅读

- [常见问题](https://docs.nocobase.com/cn/faq)
- [故障排查](https://docs.nocobase.com/cn/troubleshooting)

---

## ✅ 今日任务

- [ ] 掌握问题排查流程
- [ ] 掌握日志查看方法
- [ ] 掌握端口占用问题排查
- [ ] 掌握数据库连接问题排查
- [ ] 整理常见问题清单

---

*完成学习后，请回答练习题，我会帮你更新进度！*
