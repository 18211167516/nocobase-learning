from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import sqlite3
import json
import os
import random

app = FastAPI(title="NocoBase Learning API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE = "nocobase_learning.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day INTEGER UNIQUE NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            completed_at TEXT,
            notes TEXT
        )
    """)
    
    for day in range(1, 16):
        cursor.execute(
            "INSERT OR IGNORE INTO progress (day, completed) VALUES (?, ?)",
            (day, False)
        )
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day INTEGER NOT NULL,
            question INTEGER NOT NULL,
            answer TEXT NOT NULL,
            score INTEGER,
            feedback TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day INTEGER NOT NULL,
            type TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            icon TEXT,
            earned_at TEXT DEFAULT CURRENT_TIMESTAMP,
            type TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE NOT NULL,
            learning_time INTEGER DEFAULT 0,
            questions_answered INTEGER DEFAULT 0,
            notes_created INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def get_reference_answer(day: int, question: int):
    reference_answers = {
        1: {
            1: "NocoBase 的五个核心理念是：1）数据模型驱动 - 先定义数据结构，再展示数据，最后处理数据；2）所见即所得 - 页面就是画布，像搭 Notion 一样直观；3）一切皆插件 - 所有功能都是插件，类似 WordPress；4）AI 融入业务 - 内置 AI 员工，执行分析、翻译等任务；5）开源 + 私有部署 - 核心代码开源，数据在自己服务器上。",
            2: "配置模式是用于搭建和调整界面的设计模式，用户可以拖拽区块、配置功能；使用模式是普通用户日常使用的界面，普通用户只能进行数据操作。通过右上角的荧光笔图标切换两种模式。",
            3: "数据源、区块、操作三者的关系：数据源定义存什么数据（创建 Collection 和 Field）；区块定义怎么展示数据（将数据表拖到页面，配置为表格、表单等）；操作定义怎么使用数据（添加新增、编辑、删除等按钮）。使用流程：1）创建数据源和表；2）添加区块；3）配置操作；4）切换到使用模式。"
        },
        2: {
            1: "使用 docker compose logs -f app 查看 NocoBase 的运行日志。-f 参数表示实时跟踪日志。也可以使用 docker compose logs 查看所有日志，或 docker compose logs --tail 100 查看最后100行。",
            2: "默认账号：admin@nocobase.com；默认密码：admin123。首次登录后系统会要求修改密码，建议设置一个强密码。",
            3: "解决端口被占用问题的步骤：1）使用 netstat -tuln | grep 端口号或 lsof -i :端口号检查哪个进程占用了端口；2）修改 docker-compose.yml 中的端口映射，使用其他端口；3）或停止占用端口的进程：kill -9 进程ID。"
        },
        3: {
            1: "Collection 是数据表，类似 Excel 中的工作表或数据库中的 Table，用于存储一类相关的数据；Field 是字段，是 Collection 中的列，定义数据的具体属性。一个 Collection 可以包含多个 Field。",
            2: "常用的区块类型有：1）表格区块 - 像 Excel 一样展示数据列表，可排序筛选；2）表单区块 - 让用户输入和编辑数据；3）详情区块 - 展示单条记录的完整信息；4）看板区块 - 按状态分组展示，支持拖拽；5）图表区块 - 以图表形式展示数据分析结果。",
            3: "给表格区块添加「新增」操作的步骤：1）点击右上角荧光笔图标进入配置模式；2）点击页面上的表格区块选中它；3）点击区块右上角的齿轮图标打开配置面板；4）在左侧找到操作选项，勾选「新增」；5）保存配置后切换到使用模式即可。"
        },
        4: {
            1: "数据建模的基本步骤：1）分析业务需求 - 明确需要管理哪些业务对象；2）识别实体 - 确定有哪些独立的数据对象；3）定义属性 - 为每个实体添加字段；4）建立关系 - 确定实体之间的关联关系。",
            2: "创建 Collection 时需要考虑的字段配置要点：1）必填字段 - 设置为必填，保证数据完整性；2）默认值 - 为常用字段设置默认值；3）唯一约束 - 确保编码类字段不重复；4）验证规则 - 设置格式验证（邮箱、手机号等）。",
            3: "客户管理系统的 Collection 设计：1）客户表 - 姓名、电话、邮箱、公司、行业、来源、状态等；2）联系人表 - 客户ID、姓名、职位、电话、邮箱；3）跟进记录表 - 客户ID、跟进时间、跟进方式、跟进内容、下次跟进时间；4）商机表 - 客户ID、商机名称、金额、阶段、预计成交时间。"
        },
        5: {
            1: "三种数据关联类型：1）一对一（1:1）：如用户和用户档案；2）一对多（1:N）：如部门和员工；3）多对多（N:M）：如学生和课程。业务场景例子：一个部门有多个员工，每个员工属于一个部门（一对多）。",
            2: "公式字段用途：1）数学运算 - 总价 = 单价 × 数量；2）日期计算 - 年龄 = 当前年份 - 出生年份；3）字符串拼接 - 完整地址 = 省份 + 城市 + 街道；4）状态计算 - 根据数值自动设置状态。",
            3: "学校管理系统设计：1）学生表 - 学号、姓名、性别、出生日期、入学日期、班级；2）课程表 - 课程号、课程名、学分、授课教师；3）成绩表 - 学生ID、课程ID、成绩、学期、学年。关联关系：学生和课程是多对多（N:M），通过成绩表关联。"
        },
        6: {
            1: "配置菜单的基本步骤：1）进入系统管理 → 菜单管理；2）点击新建菜单；3）配置菜单名称、图标、路由；4）设置菜单排序和层级；5）关联到具体页面。",
            2: "设计界面布局时需要考虑的原则：1）逻辑清晰 - 按功能模块分组页面；2）使用便捷 - 常用功能放在首位；3）视觉舒适 - 合理使用图标和颜色；4）权限分明 - 不同角色看到不同菜单。",
            3: "菜单结构设计示例：销售部 - 客户管理、销售机会、销售报表；行政部 - 员工管理、请假申请、会议安排；采购部 - 供应商管理、采购订单、入库记录；财务部 - 收支记录、报销审批、财务报表。"
        },
        7: {
            1: "NocoBase 的权限控制分为四个维度：1）菜单权限 - 控制能看到哪些菜单；2）数据权限 - 控制能访问哪些数据；3）操作权限 - 控制能做哪些操作（查看/新增/编辑/删除）；4）字段权限 - 控制能看到哪些字段。",
            2: "使用角色的好处：1）批量分配 - 可以一次性给多个人分配相同权限；2）便于管理 - 权限变更只需要修改角色即可；3）职责清晰 - 不同岗位对应不同角色；4）便于审计 - 可以清楚知道谁有哪些权限。",
            3: "企业角色体系设计：1）超级管理员 - 拥有全部权限；2）系统管理员 - 系统设置、用户管理；3）部门经理 - 查看本部门数据，审批申请；4）普通员工 - 填写数据，查看自己权限范围内的数据；5）访客 - 只读权限，不能修改。"
        },
        8: {
            1: "工作流应用场景：1）审批流程 - 请假审批、报销审批、采购审批；2）数据同步 - 新建数据时同步到其他系统；3）自动通知 - 订单变化时通知相关人员；4）数据计算 - 自动更新关联数据；5）定时任务 - 定期生成报表。",
            2: "采购审批流程设计：1）触发条件 - 采购申请提交；2）节点1 - 自动检查金额，不同金额走不同流程；3）节点2 - 部门主管审批（≤1万）；4）节点3 - 财务审核（≤5万）；5）节点4 - 总经理审批（>5万）；6）节点5 - 通知申请人结果，通过后通知采购执行。",
            3: "工作流与权限配合：1）节点处理人 - 按角色分配处理权限；2）数据可见性 - 流程中控制数据字段可见；3）操作按钮 - 只在特定节点显示特定操作；4）流程访问 - 控制谁能发起流程。"
        },
        9: {
            1: "生产环境部署需要考虑：1）服务器配置 - CPU、内存、硬盘建议；2）数据库配置 - PostgreSQL 最佳实践；3）反向代理 - 使用 Nginx 配置 SSL；4）域名配置 - 配置正式域名访问；5）数据备份 - 定期自动备份；6）监控告警 - 资源和应用监控。",
            2: "数据备份策略包括：1）定期备份 - 每日自动备份数据库；2）文件备份 - 备份上传的文件；3）备份验证 - 定期测试备份恢复；4）异地容灾 - 重要数据异地存储；5）备份保留 - 保留多份历史备份。",
            3: "运维检查清单：日常检查 - 服务运行状态、资源使用率、错误日志；周检查 - 备份状态、磁盘空间；月检查 - 安全更新、性能优化、数据归档；季度检查 - 灾难恢复演练、容量评估。"
        },
        10: {
            1: "日志的重要性：1）了解问题发生原因 - 日志记录错误详情；2）还原操作步骤 - 可以看到用户做了什么；3）分析性能问题 - 慢查询日志帮助优化；4）安全审计 - 记录敏感操作；5）问题追踪 - 与问题时间点对应。",
            2: "无法访问功能页面的排查步骤：1）检查是否登录 - Cookie 是否有效；2）检查权限 - 当前用户是否有该页面权限；3）检查网络 - 浏览器控制台是否有网络错误；4）检查服务器 - 后端服务是否正常；5）查看日志 - 服务端是否有异常。",
            3: "表格查询慢的原因和优化：1）没有索引 - 为查询字段添加索引；2）数据量太大 - 合理分页，只查需要的；3）查询条件复杂 - 优化 SQL 或考虑归档历史数据；4）关联查询 - 减少不必要的关联；5）服务器资源 - 增加服务器配置。"
        },
        11: {
            1: "NocoBase 升级注意事项：1）升级前备份 - 一定要先备份数据库和文件；2）阅读更新日志 - 了解有哪些变更，是否有破坏性更新；3）测试环境验证 - 先在测试环境测试升级；4）选择合适时间 - 避开业务高峰期；5）准备回滚方案 - 万一有问题可以回退。",
            2: "提高查询性能的方法：1）为经常查询的字段添加索引；2）优化复杂 SQL 查询；3）定期清理历史数据；4）合理分页，避免一次性加载大量数据；5）使用懒加载，按需加载组件；6）考虑读写分离，查询走从库。",
            3: "数据不一致的排查和修复：1）检查日志 - 看最后一次正常操作是什么；2）找最近备份 - 对比看看哪些数据不一致；3）分析关联 - 检查关联更新是否遗漏；4）小范围修复 - 先修复少量数据验证；5）确认原因 - 避免同样问题再次发生。"
        },
        12: {
            1: "NocoBase AI 功能用途：1）智能数据分析 - 自动发现数据趋势；2）自动生成报表 - 自然语言生成报表；3）对话式查询 - 用自然语言查数据；4）文本翻译和总结 - 多语言支持；5）智能推荐 - 基于数据的智能建议。",
            2: "API 接口应用场景：1）与其他系统集成 - 与企业现有系统对接；2）移动端开发 - 给 App 提供数据；3）自动化脚本 - 定时任务、数据同步；4）第三方平台 - 与第三方 SaaS 集成；5）数据导出 - 定制化数据导出。",
            3: "最感兴趣的功能因人而异，可能是 AI 功能、工作流、插件开发等。理由通常是这些功能能解决业务中的具体痛点，提高效率，增加价值。"
        },
        13: {
            1: "NocoBase 插件架构优势：1）灵活扩展 - 需要什么功能加什么插件；2）独立升级 - 插件可以独立更新；3）生态建设 - 社区可以贡献插件；4）按需使用 - 不用的插件可以不加载；5）降低复杂度 - 核心保持简洁。",
            2: "建议使用插件开发的情况：1）现有功能无法满足需求；2）需要集成外部系统；3）需要自定义特殊交互；4）需要行业特定功能；5）已有功能不足以解决问题时。",
            3: "插件开发想法因人而异，常见的有：微信集成、钉钉集成、行业特定字段、特殊报表等。通常基于实际业务需求产生。"
        },
        14: {
            1: "面对用户问题时，应该先：1）理解问题 - 不要急于解决，先搞清楚问题是什么；2）收集信息 - 了解问题背景、影响范围、复现步骤；3）评估优先级 - 判断紧急程度和影响；4）确认理解 - 与用户确认你理解的是否正确。",
            2: "让用户满意的解决问题方法：1）及时响应 - 即使不能马上解决也要有反馈；2）态度友好 - 理解用户遇到问题的心情；3）及时同步 - 定期告诉用户进展；4）超出期望 - 不仅解决问题，还给出建议；5）跟进回访 - 确认问题是否真的解决。",
            3: "记录和总结问题的好处：1）形成知识库 - 以后遇到类似问题可以参考；2）持续改进 - 分析常见问题，改进产品或文档；3）知识沉淀 - 新同事可以快速学习；4）统计分析 - 了解哪些问题最多，重点优化；5）责任追溯 - 明确问题原因和责任人。"
        },
        15: {
            1: "15天学习最重要的5个知识点（因人而异，建议参考）：1）三个核心概念 - 数据源、区块、操作；2）数据建模 - Collection 和 Field 设计；3）权限管理 - 用户角色权限体系；4）问题排查 - 日志分析和常见问题；5）系统思维 - 从需求到上线的完整流程。",
            2: "项目管理系统 Collection 结构：1）项目表 - 项目名、负责人、开始/结束时间、状态、描述；2）任务表 - 项目ID、任务标题、负责人、状态、优先级、截止日期、描述；3）成员表 - 姓名、角色、联系方式、加入时间；4）评论表 - 任务ID、评论人、评论时间、评论内容。",
            3: "继续学习提升的计划：1）多实践 - 多做项目，在实践中成长；2）深入文档 - 精读官方文档，了解细节；3）关注社区 - 参与社区，学习别人的经验；4）分析问题 - 把遇到的问题都记录并总结；5）尝试插件 - 试着写简单插件，深入理解系统。"
        }
    }
    
    day_ref = reference_answers.get(day, {})
    return day_ref.get(question, None)

def score_answer(user_answer: str, day: int, question: int):
    reference = get_reference_answer(day, question)
    if not reference:
        return {
            "score": 5,
            "feedback": "答案已保存（无标准答案）",
            "reference": None
        }
    
    user_words = set(user_answer.lower().replace(',', ' ').replace('.', ' ').split())
    ref_words = set(reference.lower().replace(',', ' ').replace('.', ' ').split())
    
    intersection = user_words & ref_words
    coverage = len(intersection) / len(ref_words) if ref_words else 0
    
    if len(user_answer) < 20:
        score = 3
        feedback = "答案太简短了，建议详细一些。"
    elif coverage > 0.8:
        score = 10
        feedback = "非常好！回答完整准确。"
    elif coverage > 0.5:
        score = 7
        feedback = "不错！回答基本正确，可以再完整一些。"
    elif coverage > 0.2:
        score = 5
        feedback = "可以再改进，查看参考答案对比一下。"
    else:
        score = 3
        feedback = "建议重新学习相关内容后再回答。"
    
    return {
        "score": score,
        "feedback": feedback,
        "reference": reference
    }

init_db()

class ProgressUpdate(BaseModel):
    day: int
    completed: bool
    notes: Optional[str] = None

class AnswerSubmit(BaseModel):
    day: int
    question: int
    answer: str

class NoteCreate(BaseModel):
    day: int
    content: str

class NoteUpdate(BaseModel):
    id: int
    content: str

class FavoriteCreate(BaseModel):
    day: int
    type: str
    content: str

class ChatMessage(BaseModel):
    message: str
    context: Optional[List[dict]] = None

class ProgressResponse(BaseModel):
    day: int
    completed: bool
    completed_at: Optional[str]
    notes: Optional[str]

@app.get("/")
def read_root():
    return {"message": "NocoBase Learning API", "version": "1.0.0"}

@app.get("/progress", response_model=List[ProgressResponse])
def get_progress():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM progress ORDER BY day")
    rows = cursor.fetchall()
    conn.close()
    
    return [
        ProgressResponse(
            day=row["day"],
            completed=bool(row["completed"]),
            completed_at=row["completed_at"],
            notes=row["notes"]
        )
        for row in rows
    ]

@app.get("/progress/{day}", response_model=ProgressResponse)
def get_day_progress(day: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM progress WHERE day = ?", (day,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Day not found")
    
    return ProgressResponse(
        day=row["day"],
        completed=bool(row["completed"]),
        completed_at=row["completed_at"],
        notes=row["notes"]
    )

@app.post("/progress")
def update_progress(progress: ProgressUpdate):
    conn = get_db()
    cursor = conn.cursor()
    
    completed_at = datetime.now().isoformat() if progress.completed else None
    
    cursor.execute(
        """UPDATE progress 
           SET completed = ?, completed_at = ?, notes = ? 
           WHERE day = ?""",
        (progress.completed, completed_at, progress.notes, progress.day)
    )
    
    conn.commit()
    conn.close()
    
    check_and_award_badges()
    
    return {"message": "Progress updated", "day": progress.day}

@app.post("/answers")
def submit_answer(answer: AnswerSubmit):
    conn = get_db()
    cursor = conn.cursor()
    
    result = score_answer(answer.answer, answer.day, answer.question)
    
    cursor.execute(
        """INSERT INTO answers (day, question, answer, score, feedback, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (answer.day, answer.question, answer.answer, result["score"], result["feedback"], datetime.now().isoformat())
    )
    
    conn.commit()
    conn.close()
    
    check_and_award_badges()
    
    return {
        "message": "Answer submitted",
        "day": answer.day,
        "question": answer.question,
        "score": result["score"],
        "feedback": result["feedback"],
        "reference": result["reference"]
    }

@app.get("/answers/{day}")
def get_answers(day: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM answers WHERE day = ? ORDER BY question",
        (day,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": row["id"],
            "day": row["day"],
            "question": row["question"],
            "answer": row["answer"],
            "score": row["score"],
            "feedback": row["feedback"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]

@app.get("/wrong-answers")
def get_wrong_answers():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM answers WHERE score < 5 ORDER BY score ASC, created_at DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": row["id"],
            "day": row["day"],
            "question": row["question"],
            "answer": row["answer"],
            "score": row["score"],
            "feedback": row["feedback"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]

@app.get("/stats")
def get_stats():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM progress WHERE completed = 1")
    completed_days = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(*) as total FROM answers")
    total_answers = cursor.fetchone()["total"]
    
    cursor.execute("SELECT AVG(score) as avg_score FROM answers WHERE score IS NOT NULL")
    avg_score = cursor.fetchone()["avg_score"]
    avg_score = round(avg_score, 1) if avg_score else 0
    
    cursor.execute("SELECT day FROM progress WHERE completed = 1 ORDER BY day DESC LIMIT 1")
    last_row = cursor.fetchone()
    current_day = last_row["day"] + 1 if last_row else 1
    
    cursor.execute("SELECT COUNT(*) as total FROM notes")
    total_notes = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(*) as total FROM favorites")
    total_favorites = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(*) as total FROM badges")
    total_badges = cursor.fetchone()["total"]
    
    conn.close()
    
    return {
        "total_days": 15,
        "completed_days": completed_days,
        "remaining_days": 15 - completed_days,
        "progress_percent": round(completed_days / 15 * 100, 1),
        "total_answers": total_answers,
        "average_score": avg_score,
        "current_day": min(current_day, 15),
        "total_notes": total_notes,
        "total_favorites": total_favorites,
        "total_badges": total_badges
    }

@app.get("/learning-stats")
def get_learning_stats():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT day, AVG(score) as avg_score, COUNT(*) as attempts
        FROM answers
        GROUP BY day
        ORDER BY day
    """)
    daily_stats = cursor.fetchall()
    
    cursor.execute("""
        SELECT strftime('%Y-%m-%d', created_at) as date, COUNT(*) as count
        FROM answers
        GROUP BY date
        ORDER BY date DESC
        LIMIT 7
    """)
    recent_activity = cursor.fetchall()
    
    conn.close()
    
    return {
        "daily_stats": [
            {
                "day": row["day"],
                "avg_score": round(row["avg_score"], 1),
                "attempts": row["attempts"]
            }
            for row in daily_stats
        ],
        "recent_activity": [
            {
                "date": row["date"],
                "count": row["count"]
            }
            for row in recent_activity
        ]
    }

@app.post("/notes")
def create_note(note: NoteCreate):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO notes (day, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (note.day, note.content, datetime.now().isoformat(), datetime.now().isoformat())
    )
    
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    
    return {"message": "Note created", "id": note_id}

@app.get("/notes")
def get_notes(day: Optional[int] = None):
    conn = get_db()
    cursor = conn.cursor()
    
    if day:
        cursor.execute("SELECT * FROM notes WHERE day = ? ORDER BY updated_at DESC", (day,))
    else:
        cursor.execute("SELECT * FROM notes ORDER BY updated_at DESC")
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": row["id"],
            "day": row["day"],
            "content": row["content"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
        for row in rows
    ]

@app.put("/notes")
def update_note(note: NoteUpdate):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE notes SET content = ?, updated_at = ? WHERE id = ?",
        (note.content, datetime.now().isoformat(), note.id)
    )
    
    conn.commit()
    conn.close()
    
    return {"message": "Note updated"}

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    
    conn.commit()
    conn.close()
    
    return {"message": "Note deleted"}

@app.post("/favorites")
def create_favorite(favorite: FavoriteCreate):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO favorites (day, type, content, created_at) VALUES (?, ?, ?, ?)",
        (favorite.day, favorite.type, favorite.content, datetime.now().isoformat())
    )
    
    conn.commit()
    fav_id = cursor.lastrowid
    conn.close()
    
    return {"message": "Favorite created", "id": fav_id}

@app.get("/favorites")
def get_favorites(day: Optional[int] = None, type: Optional[str] = None):
    conn = get_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM favorites WHERE 1=1"
    params = []
    
    if day:
        query += " AND day = ?"
        params.append(day)
    if type:
        query += " AND type = ?"
        params.append(type)
    
    query += " ORDER BY created_at DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": row["id"],
            "day": row["day"],
            "type": row["type"],
            "content": row["content"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]

@app.delete("/favorites/{fav_id}")
def delete_favorite(fav_id: int):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM favorites WHERE id = ?", (fav_id,))
    
    conn.commit()
    conn.close()
    
    return {"message": "Favorite deleted"}

@app.get("/badges")
def get_badges():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM badges ORDER BY earned_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    all_badges = get_all_badges()
    earned = [row["name"] for row in rows]
    
    return [
        {
            "name": badge["name"],
            "description": badge["description"],
            "icon": badge["icon"],
            "earned": badge["name"] in earned,
            "earned_at": next((row["earned_at"] for row in rows if row["name"] == badge["name"]), None)
        }
        for badge in all_badges
    ]

def get_all_badges():
    return [
        {"name": "初学者", "description": "完成第一天的学习", "icon": "🌱"},
        {"name": "坚持不懈", "description": "连续学习3天", "icon": "🔥"},
        {"name": "学霸", "description": "完成5天的学习", "icon": "📚"},
        {"name": "知识探索者", "description": "完成10天的学习", "icon": "🔍"},
        {"name": "毕业达人", "description": "完成全部15天的学习", "icon": "🎓"},
        {"name": "答题高手", "description": "回答10道题", "icon": "💯"},
        {"name": "满分达人", "description": "获得第一个10分", "icon": "⭐"},
        {"name": "笔记达人", "description": "创建10条笔记", "icon": "📝"},
        {"name": "收藏家", "description": "收藏5个知识点", "icon": "❤️"},
        {"name": "全能学员", "description": "完成所有徽章任务", "icon": "🏆"}
    ]

def check_and_award_badges():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as count FROM progress WHERE completed = 1")
    completed_days = cursor.fetchone()["count"]
    
    cursor.execute("SELECT COUNT(*) as count FROM answers")
    total_answers = cursor.fetchone()["count"]
    
    cursor.execute("SELECT COUNT(*) as count FROM answers WHERE score = 10")
    perfect_scores = cursor.fetchone()["count"]
    
    cursor.execute("SELECT COUNT(*) as count FROM notes")
    total_notes = cursor.fetchone()["count"]
    
    cursor.execute("SELECT COUNT(*) as count FROM favorites")
    total_favorites = cursor.fetchone()["count"]
    
    badges_to_award = []
    
    if completed_days >= 1:
        badges_to_award.append("初学者")
    if completed_days >= 3:
        badges_to_award.append("坚持不懈")
    if completed_days >= 5:
        badges_to_award.append("学霸")
    if completed_days >= 10:
        badges_to_award.append("知识探索者")
    if completed_days >= 15:
        badges_to_award.append("毕业达人")
    if total_answers >= 10:
        badges_to_award.append("答题高手")
    if perfect_scores >= 1:
        badges_to_award.append("满分达人")
    if total_notes >= 10:
        badges_to_award.append("笔记达人")
    if total_favorites >= 5:
        badges_to_award.append("收藏家")
    if (completed_days >= 15 and total_answers >= 10 and perfect_scores >= 1 and 
        total_notes >= 10 and total_favorites >= 5):
        badges_to_award.append("全能学员")
    
    for badge_name in badges_to_award:
        cursor.execute("SELECT COUNT(*) as count FROM badges WHERE name = ?", (badge_name,))
        exists = cursor.fetchone()["count"]
        
        if not exists:
            badge_info = next((b for b in get_all_badges() if b["name"] == badge_name), None)
            if badge_info:
                cursor.execute(
                    "INSERT INTO badges (name, description, icon, earned_at, type) VALUES (?, ?, ?, ?, ?)",
                    (badge_info["name"], badge_info["description"], badge_info["icon"], 
                     datetime.now().isoformat(), "achievement")
                )
    
    conn.commit()
    conn.close()

@app.get("/recommendations")
def get_recommendations():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM progress ORDER BY day DESC LIMIT 1")
    last_completed = cursor.fetchone()
    
    cursor.execute("""
        SELECT day, AVG(score) as avg_score
        FROM answers
        GROUP BY day
        HAVING avg_score < 6
        ORDER BY avg_score ASC
        LIMIT 3
    """)
    weak_days = cursor.fetchall()
    
    cursor.execute("SELECT * FROM answers WHERE score < 5 ORDER BY score ASC LIMIT 3")
    weak_questions = cursor.fetchall()
    
    conn.close()
    
    recommendations = []
    
    if last_completed:
        next_day = last_completed["day"] + 1 if last_completed["day"] < 15 else 15
        recommendations.append({
            "type": "next_step",
            "priority": "high",
            "message": f"建议继续学习 Day {next_day}",
            "reason": "保持学习进度，继续前进"
        })
    
    if weak_days:
        recommendations.append({
            "type": "review",
            "priority": "high",
            "message": f"建议复习 Day {weak_days[0]['day']}",
            "reason": "这部分知识点需要加强"
        })
    
    if weak_questions:
        recommendations.append({
            "type": "practice",
            "priority": "medium",
            "message": "多做练习题巩固知识",
            "reason": "通过练习加深理解"
        })
    
    recommendations.append({
        "type": "explore",
        "priority": "low",
        "message": "使用 AI 助手解答疑惑",
        "reason": "遇到问题随时提问"
    })
    
    return recommendations

@app.get("/search")
def search(query: str):
    knowledge_base = {
        "NocoBase 核心理念": "数据模型驱动、所见即所得、一切皆插件、AI 融入业务、开源+私有部署",
        "数据源": "数据源是存放数据的地方，定义数据结构和存储位置",
        "区块": "区块是页面上展示数据的方式，包括表格、表单、详情、看板、图表等",
        "操作": "操作是对数据进行处理的动作，包括新增、查看、编辑、删除等",
        "Collection": "Collection 是数据表，类似 Excel 工作表",
        "Field": "Field 是字段，定义数据的具体属性",
        "权限": "权限控制分为菜单权限、数据权限、操作权限、字段权限",
        "工作流": "工作流是业务流程自动化，如审批流程、数据同步等",
        "安装": "使用 Docker 快速安装：mkdir my-nocobase && cd my-nocobase && docker compose up -d",
        "部署": "生产环境部署需要考虑服务器配置、数据库配置、反向代理、数据备份等"
    }
    
    results = []
    query_lower = query.lower()
    
    for keyword, answer in knowledge_base.items():
        if keyword.lower() in query_lower or query_lower in keyword.lower():
            results.append({
                "keyword": keyword,
                "answer": answer
            })
    
    return {"query": query, "results": results}

@app.post("/chat")
def chat(chat_message: ChatMessage):
    knowledge_base = {
        "nocobase": "NocoBase 是一个开源的 AI 无代码开发平台，核心理念包括：数据模型驱动、所见即所得、一切皆插件、AI 融入业务、开源+私有部署。",
        "数据源": "数据源（Data Source）是存放数据的地方，可以定义数据结构和存储位置。默认使用 PostgreSQL 数据库。",
        "区块": "区块（Block）是页面上展示数据的方式，常见类型有：表格区块、表单区块、详情区块、看板区块、图表区块等。",
        "操作": "操作（Action）是对数据进行处理的动作，包括：新增、查看、编辑、删除、批量操作等。",
        "collection": "Collection 是数据表，类似 Excel 中的工作表，用于存储一类相关的数据。",
        "field": "Field 是字段，是 Collection 中的列，定义数据的具体属性。",
        "权限": "NocoBase 的权限控制分为四个维度：菜单权限、数据权限、操作权限、字段权限。",
        "工作流": "工作流是一系列有逻辑顺序的任务自动化，用于实现业务流程自动化，如审批流程、数据同步、自动通知等。",
        "安装": "使用 Docker 快速安装：mkdir my-nocobase && cd my-nocobase，然后下载 docker-compose.yml 并运行 docker compose up -d。",
        "部署": "生产环境部署需要考虑：服务器配置、数据库配置、反向代理、域名配置、数据备份、监控告警等。"
    }
    
    message_lower = chat_message.message.lower()
    
    for keyword, response in knowledge_base.items():
        if keyword in message_lower:
            return {"response": response}
    
    if "出题" in message_lower or "练习题" in message_lower:
        quizzes = [
            "📝 **练习题：** NocoBase 的五个核心理念是什么？\n\n提示：数据模型驱动、所见即所得、一切皆插件...",
            "📝 **练习题：** Collection 和 Field 有什么区别？\n\n提示：Collection 是数据表，Field 是字段...",
            "📝 **练习题：** 如何给表格区块添加「新增」操作？\n\n提示：进入配置模式 → 选择区块 → 配置操作...",
            "📝 **练习题：** 数据源、区块、操作三者的关系是什么？\n\n提示：数据源定义存什么，区块定义怎么展示，操作定义怎么用...",
            "📝 **练习题：** NocoBase 支持哪些数据库？\n\n提示：PostgreSQL、MySQL、MariaDB..."
        ]
        return {"response": random.choice(quizzes)}
    
    if "答案" in message_lower:
        return {"response": "请告诉我你想知道哪道题的答案？或者你可以直接问我具体的知识点问题！"}
    
    default_responses = [
        "这是个好问题！🤔 你可以查看官方文档：https://docs.nocobase.com/cn/ 获取更多信息。",
        "我理解你的问题！建议你：1）查看相关知识点；2）尝试实际操作；3）有疑问随时问我！",
        "关于这个问题，你可以：• 查看官方文档\n• 点击「出一道题」测试知识\n• 或者问我更具体的问题"
    ]
    
    return {"response": random.choice(default_responses)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
