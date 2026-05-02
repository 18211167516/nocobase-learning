# Day 13：插件开发基础

> **学习目标：** 了解插件结构、前端插件、后端插件
> **预计时间：** 2 小时
> **难度：** 🟡 进阶

---

## 📖 学习内容

### 1. 插件概述

#### 什么是插件？

NocoBase 的所有功能都是插件，包括：
- 核心功能
- 区块类型
- 字段类型
- 工作流节点
- 数据源类型

#### 插件类型

| 类型 | 说明 |
|------|------|
| 预置插件 | 官方内置插件 |
| 社区插件 | 社区贡献插件 |
| 自定义插件 | 自行开发插件 |

---

### 2. 插件结构

#### 目录结构

```
my-plugin/
├── package.json       # 插件配置
├── src/
│   ├── client/        # 前端代码
│   │   ├── index.tsx
│   │   └── Plugin.tsx
│   └── server/        # 后端代码
│       ├── index.ts
│       └── plugin.ts
└── locale/            # 国际化
    └── zh-CN.json
```

#### package.json

```json
{
  "name": "@my-org/my-plugin",
  "version": "1.0.0",
  "displayName": "我的插件",
  "description": "插件描述",
  "main": "dist/server/index.js",
  "nocobase": {
    "displayName": "我的插件",
    "type": "plugin"
  }
}
```

---

### 3. 前端插件开发

#### 创建前端插件

```typescript
// src/client/Plugin.tsx
import { Plugin } from '@nocobase/client';

class MyPlugin extends Plugin {
  async load() {
    // 注册区块
    this.app.addBlock({
      type: 'my-block',
      component: MyBlock,
    });

    // 注册路由
    this.app.router.add('my-page', {
      path: '/my-page',
      component: MyPage,
    });
  }
}

export default MyPlugin;
```

#### 自定义区块

```typescript
// src/client/blocks/MyBlock.tsx
import React from 'react';
import { useBlockRequest } from '@nocobase/client';

export function MyBlock() {
  const { data, loading } = useBlockRequest();

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      {data?.map(item => (
        <div key={item.id}>{item.name}</div>
      ))}
    </div>
  );
}
```

---

### 4. 后端插件开发

#### 创建后端插件

```typescript
// src/server/plugin.ts
import { Plugin } from '@nocobase/server';

export class MyPlugin extends Plugin {
  async load() {
    // 注册 API 路由
    this.app.resourcer.define({
      name: 'my-resource',
      actions: {
        list: async (ctx, next) => {
          ctx.body = { data: [] };
          await next();
        },
      },
    });

    // 注册数据库模型
    this.db.collection({
      name: 'my_collection',
      fields: [
        { type: 'string', name: 'name' },
        { type: 'integer', name: 'count' },
      ],
    });
  }
}
```

---

### 5. 插件发布

#### 构建插件

```bash
# 开发模式
yarn dev

# 构建
yarn build

# 打包
yarn pack
```

#### 发布到 NPM

```bash
npm publish
```

---

### 6. 常用扩展点

| 扩展点 | 说明 |
|--------|------|
| 区块 | 自定义区块类型 |
| 字段 | 自定义字段类型 |
| 操作 | 自定义操作按钮 |
| 工作流节点 | 自定义工作流节点 |
| 数据源 | 自定义数据源类型 |

---

## 🎯 练习题

### 问题 1：NocoBase 插件的结构是什么？

### 问题 2：如何注册一个自定义区块？

### 问题 3：前端插件和后端插件有什么区别？

### 问题 4：动手练习 - 创建一个简单的自定义区块

---

## 📚 扩展阅读

- [插件开发指南](https://docs.nocobase.com/cn/development/plugin)
- [前端开发](https://docs.nocobase.com/cn/development/client)
- [后端开发](https://docs.nocobase.com/cn/development/server)

---

## ✅ 今日任务

- [ ] 了解插件结构
- [ ] 了解前端插件开发
- [ ] 了解后端插件开发
- [ ] 了解插件发布流程

---

*完成学习后，请回答练习题，我会帮你更新进度！*
