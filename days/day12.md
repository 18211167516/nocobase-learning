# Day 12：高级功能了解

> **学习目标：** 了解 AI 员工、通知渠道、数据可视化、邮件管理
> **预计时间：** 1.5 小时
> **难度：** 🟡 进阶

---

## 📖 学习内容

### 1. AI 员工

#### 什么是 AI 员工？

AI 员工是 NocoBase 内置的 AI 能力，可以在业务流程中执行特定任务。

#### AI 员工类型

| 类型 | 功能 |
|------|------|
| 翻译员 | 翻译文本 |
| 分析员 | 分析数据 |
| 调研员 | 收集信息 |
| 录入员 | 数据录入 |
| 助手 | 通用任务 |

#### 配置 AI 员工

1. 进入配置模式
2. 点击「AI 员工」
3. 添加 AI 员工
4. 配置：
   - 名称和角色
   - 使用的模型（OpenAI / 本地模型）
   - 提示词
   - 可访问的数据

#### 使用场景

- 自动分类工单
- 生成回复建议
- 提取关键信息
- 翻译内容

---

### 2. 通知渠道

#### 支持的通知渠道

| 渠道 | 说明 |
|------|------|
| 站内通知 | NocoBase 内部通知 |
| 邮件 | SMTP 邮件 |
| 钉钉 | 钉钉机器人 |
| 企业微信 | 企业微信机器人 |
| 飞书 | 飞书机器人 |

#### 配置邮件通知

```yaml
# 环境变量配置
environment:
  - MAIL_HOST=smtp.example.com
  - MAIL_PORT=465
  - MAIL_USER=noreply@example.com
  - MAIL_PASSWORD=your_password
  - MAIL_FROM=noreply@example.com
```

#### 配置钉钉通知

1. 创建钉钉机器人
2. 获取 Webhook 地址
3. 在 NocoBase 中配置通知渠道
4. 在工作流中使用通知节点

---

### 3. 数据可视化

#### 图表区块类型

| 类型 | 说明 |
|------|------|
| 柱状图 | 对比数据 |
| 折线图 | 趋势分析 |
| 饼图 | 占比分析 |
| 数字卡片 | 关键指标 |
| 仪表盘 | 综合展示 |

#### 创建图表

1. 添加区块 → 选择「图表区块」
2. 选择数据源
3. 配置维度和指标
4. 选择图表类型
5. 配置样式

#### 仪表盘配置

1. 创建仪表盘页面
2. 添加多个图表区块
3. 配置数据筛选
4. 设置刷新频率

---

### 4. 邮件管理

#### 邮件配置

```yaml
environment:
  - MAIL_HOST=imap.example.com
  - MAIL_PORT=993
  - MAIL_USER=your@email.com
  - MAIL_PASSWORD=your_password
```

#### 邮件功能

- 接收邮件
- 发送邮件
- 邮件模板
- 邮件规则

#### 使用场景

- 工单邮件通知
- 定期报告发送
- 客户沟通记录

---

### 5. 文件管理

#### 文件存储

- 本地存储
- 云存储（S3、OSS 等）

#### 配置云存储

```yaml
environment:
  - STORAGE_TYPE=s3
  - AWS_ACCESS_KEY_ID=your_key
  - AWS_SECRET_ACCESS_KEY=your_secret
  - AWS_S3_BUCKET=your_bucket
  - AWS_S3_REGION=us-east-1
```

---

## 🎯 练习题

### 问题 1：AI 员工可以执行哪些任务？

### 问题 2：如何配置邮件通知？

### 问题 3：如何创建一个数据仪表盘？

### 问题 4：动手练习 - 配置一个通知工作流

---

## 📚 扩展阅读

- [AI 员工](https://docs.nocobase.com/cn/ai-employees/quick-start)
- [通知配置](https://docs.nocobase.com/cn/notification)
- [数据可视化](https://docs.nocobase.com/cn/data-visualization)

---

## ✅ 今日任务

- [ ] 了解 AI 员工功能
- [ ] 配置通知渠道
- [ ] 创建图表区块
- [ ] 了解邮件管理功能

---

*完成学习后，请回答练习题，我会帮你更新进度！*
