<template>
  <div class="main-content">
    <div class="back-btn" @click="goBack">
      ← 返回首页
    </div>
    
    <div v-if="loading" class="loading">
      加载中...
    </div>
    
    <div v-else class="day-content">
      <h2>Day {{ dayId }}: {{ dayTitle }}</h2>
      
      <div class="section" v-html="content"></div>
      
      <div class="exercises" v-if="exercises.length > 0">
        <h3>🎯 练习题</h3>
        <div 
          v-for="(exercise, index) in exercises" 
          :key="index"
          class="exercise-item"
        >
          <p><strong>问题 {{ index + 1 }}：</strong>{{ exercise.question }}</p>
          <textarea 
            v-model="answers[index]" 
            placeholder="请输入你的答案..."
          ></textarea>
          
          <div v-if="savedAnswersData[index]" class="score-result">
            <div class="score-display" :class="getScoreClass(savedAnswersData[index].score)">
              <span class="score-label">得分：</span>
              <span class="score-value">{{ savedAnswersData[index].score }} / 10</span>
            </div>
            <p class="feedback">{{ savedAnswersData[index].feedback }}</p>
            <div v-if="savedAnswersData[index].reference" class="reference">
              <p><strong>参考答案：</strong></p>
              <p>{{ savedAnswersData[index].reference }}</p>
            </div>
          </div>
        </div>
        <button class="btn btn-primary" @click="submitAnswers" style="margin-top: 15px;">
          提交答案
        </button>
      </div>
      
      <div style="margin-top: 30px; display: flex; gap: 15px;">
        <button 
          v-if="!progress.completed" 
          class="btn btn-success"
          @click="markComplete"
        >
          ✓ 标记为已完成
        </button>
        <span 
          v-else 
          style="color: #10b981; font-weight: 600;"
        >
          ✓ 已完成
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getDayProgress, updateProgress, getAnswers, submitAnswer } from '../api'

const route = useRoute()
const router = useRouter()
const dayId = computed(() => parseInt(route.params.id))
const loading = ref(true)
const progress = ref({ completed: false })
const answers = ref([])
const savedAnswers = ref([])
const savedAnswersData = ref([])

const dayData = {
  1: {
    title: '认识 NocoBase',
    content: `
      <div class="section">
        <h3>学习目标</h3>
        <p>理解 NocoBase 产品定位、核心理念和技术栈</p>
        
        <h3>NocoBase 是什么？</h3>
        <p><strong>NocoBase</strong> 是一个开源的、极易扩展的 AI 无代码开发平台，通过配置和拖拽来搭建业务系统。</p>
        <p>📚 官方资源：</p>
        <ul>
          <li><a href="https://www.nocobase.com/" target="_blank">NocoBase 官网</a></li>
          <li><a href="https://github.com/nocobase/nocobase" target="_blank">GitHub 仓库</a></li>
          <li><a href="https://docs.nocobase.com/cn/" target="_blank">中文文档</a></li>
          <li><a href="https://docs.nocobase.com/cn/tutorials/v2/" target="_blank">官方教程</a></li>
        </ul>
        
        <h3>五个核心理念</h3>
        <ol>
          <li><strong>数据模型驱动</strong>：先定义数据结构，再展示数据，最后处理数据</li>
          <li><strong>所见即所得</strong>：页面就是画布，像搭 Notion 一样直观</li>
          <li><strong>一切皆插件</strong>：所有功能都是插件，类似 WordPress</li>
          <li><strong>AI 融入业务</strong>：内置 AI 员工，执行分析、翻译等任务</li>
          <li><strong>开源 + 私有部署</strong>：核心代码开源，数据在自己服务器上</li>
        </ol>
        
        <h3>技术栈</h3>
        <table>
          <tr><th>层级</th><th>技术</th></tr>
          <tr><td>前端</td><td>React + Ant Design 5.0</td></tr>
          <tr><td>后端</td><td>Node.js + Koa</td></tr>
          <tr><td>数据库</td><td>PostgreSQL / MySQL / MariaDB</td></tr>
          <tr><td>部署</td><td>Docker / Kubernetes</td></tr>
        </table>
        
        <h3>两种核心模式</h3>
        <ul>
          <li><strong>使用模式</strong>：普通用户日常使用的界面</li>
          <li><strong>配置模式</strong>：搭建和调整界面的设计模式</li>
        </ul>

        <h3>三个核心概念：数据源、区块、操作</h3>
        <p>这三个概念是 NocoBase 的基础，理解它们的关系至关重要：</p>
        <p>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/core-concepts" target="_blank">核心概念</a></p>
        
        <h4>1. 数据源（Data Source）</h4>
        <ul>
          <li><strong>定义</strong>：数据源是存放数据的地方，可以是数据库、区块链、API等</li>
          <li><strong>作用</strong>：定义数据结构和存储位置</li>
          <li><strong>默认数据源</strong>：安装后自动创建的内置 PostgreSQL 数据库</li>
          <li><strong>配置路径</strong>：设置 → 数据源配置</li>
          <li>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/data-source" target="_blank">数据源</a></li>
        </ul>

        <h4>2. 区块（Block）</h4>
        <ul>
          <li><strong>定义</strong>：区块是页面上展示数据的方式</li>
          <li><strong>作用</strong>：将数据以表格、表单、图表等形式展示给用户</li>
          <li><strong>常见类型</strong>：
            <ul>
              <li>表格区块：像 Excel 一样展示数据列表</li>
              <li>表单区块：让用户输入和编辑数据</li>
              <li>详情区块：展示单条记录的详细信息</li>
              <li>看板区块：用看板形式展示任务进度</li>
              <li>图表区块：用图表展示数据分析结果</li>
            </ul>
          </li>
          <li><strong>操作方式</strong>：在配置模式下，从左侧拖拽到页面即可</li>
          <li>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/blocks" target="_blank">区块</a></li>
        </ul>

        <h4>3. 操作（Action）</h4>
        <ul>
          <li><strong>定义</strong>：操作是对数据进行处理的动作</li>
          <li><strong>作用</strong>：让用户能够增删改查数据</li>
          <li><strong>常见操作</strong>：
            <ul>
              <li>新增（Create）：添加新数据</li>
              <li>查看（View）：查看数据详情</li>
              <li>编辑（Edit）：修改现有数据</li>
              <li>删除（Delete）：删除数据</li>
              <li>批量操作：批量删除、导出等</li>
            </ul>
          </li>
          <li><strong>配置方式</strong>：点击区块右上角的配置按钮添加操作</li>
          <li>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/actions" target="_blank">操作</a></li>
        </ul>

        <h4>三者关系图</h4>
        <pre>
数据源（定义存什么） → 区块（定义怎么展示） → 操作（定义怎么用）
      ↓                        ↓                        ↓
   创建数据表              将数据表拖到页面            给区块添加按钮
        </pre>

        <h4>实际使用流程</h4>
        <ol>
          <li><strong>第一步：创建数据源和表</strong> - 在数据源中创建 Collection（数据表），定义字段</li>
          <li><strong>第二步：添加区块</strong> - 在配置模式下，将对应的区块拖到页面</li>
          <li><strong>第三步：配置操作</strong> - 给区块添加新增、编辑、删除等操作按钮</li>
          <li><strong>第四步：切换使用模式</strong> - 普通用户就可以使用了</li>
        </ol>

        <h4>举例说明</h4>
        <p><strong>场景：创建一个客户管理系统</strong></p>
        <ol>
          <li><strong>数据源</strong>：创建一个名为"客户"的 Collection，包含字段：姓名、手机号、邮箱、地址</li>
          <li><strong>区块</strong>：在页面上添加一个表格区块，关联到"客户"这个 Collection</li>
          <li><strong>操作</strong>：给表格添加"新增客户"、"编辑客户"、"删除客户"按钮</li>
          <li><strong>使用</strong>：用户就可以在表格中添加、编辑、删除客户信息了</li>
        </ol>
      </div>
    `,
    exercises: [
      { question: "NocoBase 的五个核心理念是什么？" },
      { question: "配置模式和使用模式有什么区别？" },
      { question: "请详细说明数据源、区块、操作三者的关系是什么？" }
    ]
  },
  2: {
    title: 'Docker 安装部署',
    content: `
      <div class="section">
        <h3>学习目标</h3>
        <p>掌握 NocoBase 的 Docker 安装和基本运维</p>
        
        <h3>快速安装步骤</h3>
        <pre>
# 创建项目目录
mkdir my-nocobase && cd my-nocobase

# 下载配置文件
curl -fsSL https://static-docs.nocobase.com/docker-compose/cn/latest-postgres.yml -o docker-compose.yml

# 启动服务
docker compose up -d

# 查看日志
docker compose logs -f app
        </pre>
        
        <h3>默认登录信息</h3>
        <ul>
          <li>访问地址：http://localhost:13000</li>
          <li>账号：admin@nocobase.com</li>
          <li>密码：admin123</li>
        </ul>
        
        <h3>常用命令</h3>
        <pre>
docker compose ps        # 查看容器状态
docker compose logs -f   # 查看日志
docker compose down      # 停止服务
docker compose restart   # 重启服务
        </pre>
        <p>📚 参考文档：</p>
        <ul>
          <li><a href="https://docs.nocobase.com/cn/getting-started/deployment/docker" target="_blank">Docker 部署</a></li>
          <li><a href="https://docs.nocobase.com/cn/getting-started/deployment/docker-compose" target="_blank">Docker Compose 配置</a></li>
        </ul>
      </div>
    `,
    exercises: [
      { question: "如何查看 NocoBase 的运行日志？" },
      { question: "默认的登录账号密码是什么？" },
      { question: "如何解决端口被占用的问题？" }
    ]
  },
  3: {
    title: '基础功能概览',
    content: `
      <div class="section">
        <h3>学习目标</h3>
        <p>熟悉 NocoBase 的主要功能模块和操作方式</p>
        
        <h3>Collection 和 Field</h3>
        <p>在 NocoBase 中，数据存储的核心概念是 Collection 和 Field：</p>
        
        <h4>Collection（数据表）</h4>
        <ul>
          <li><strong>定义</strong>：Collection 是数据表的抽象概念，类似 Excel 中的工作表或数据库中的 Table</li>
          <li><strong>作用</strong>：存储一类相关的数据，如"用户"、"订单"、"产品"等</li>
          <li><strong>特点</strong>：每个 Collection 可以包含多个 Field（字段）</li>
          <li><strong>类比</strong>：相当于数据库中的表（Table）</li>
        </ul>

        <h4>Field（字段）</h4>
        <ul>
          <li><strong>定义</strong>：Field 是 Collection 中的列，定义数据的具体属性</li>
          <li><strong>作用</strong>：描述 Collection 中每条记录的特征</li>
          <li><strong>类比</strong>：相当于数据库中的列（Column）</li>
        </ul>

        <h4>举例说明</h4>
        <p><strong>创建一个"员工" Collection：</strong></p>
        <table>
          <tr><th>字段名</th><th>字段类型</th><th>说明</th></tr>
          <tr><td>姓名</td><td>单行文本</td><td>员工姓名</td></tr>
          <tr><td>工号</td><td>单行文本</td><td>唯一工号标识</td></tr>
          <tr><td>部门</td><td>单选</td><td>所属部门</td></tr>
          <tr><td>入职日期</td><td>日期</td><td>入职时间</td></tr>
          <tr><td>薪资</td><td>数字</td><td>工资数额</td></tr>
        </table>
        <p>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/collections" target="_blank">Collections</a></p>

        <h3>常用字段类型</h3>
        <table>
          <tr><th>类型</th><th>说明</th><th>示例</th></tr>
          <tr><td>单行文本</td><td>短文本</td><td>姓名、标题、编号</td></tr>
          <tr><td>多行文本</td><td>长文本</td><td>描述、备注、地址</td></tr>
          <tr><td>数字</td><td>整数或小数</td><td>价格、数量、年龄</td></tr>
          <tr><td>日期</td><td>日期时间</td><td>生日、订单日期</td></tr>
          <tr><td>单选</td><td>固定选项</td><td>性别、状态、部门</td></tr>
          <tr><td>多选</td><td>多个选项</td><td>爱好、技能</td></tr>
          <tr><td>开关</td><td>是/否</td><td>是否启用、是否 VIP</td></tr>
          <tr><td>关联</td><td>关联其他表</td><td>用户-订单、产品-分类</td></tr>
          <tr><td>附件</td><td>上传文件</td><td>头像、合同、文档</td></tr>
          <tr><td>公式</td><td>计算字段</td><td>总价=单价×数量</td></tr>
        </table>
        <p>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/fields" target="_blank">Fields</a></p>

        <h3>常用区块类型</h3>
        <p>区块是 NocoBase 中展示数据的基本单元：</p>
        
        <h4>1. 表格区块（Table）</h4>
        <ul>
          <li><strong>用途</strong>：列表展示多条数据</li>
          <li><strong>特点</strong>：可排序、可筛选、可分页</li>
          <li><strong>类比</strong>：像 Excel 表格一样</li>
        </ul>

        <h4>2. 表单区块（Form）</h4>
        <ul>
          <li><strong>用途</strong>：让用户输入和编辑数据</li>
          <li><strong>特点</strong>：可添加字段、可设置必填、可验证</li>
          <li><strong>类比</strong>：像在线表单一样</li>
        </ul>

        <h4>3. 详情区块（Details）</h4>
        <ul>
          <li><strong>用途</strong>：展示单条记录的完整信息</li>
          <li><strong>特点</strong>：可以展示关联数据</li>
          <li><strong>类比</strong>：像个人资料页一样</li>
        </ul>

        <h4>4. 看板区块（Kanban）</h4>
        <ul>
          <li><strong>用途</strong>：以看板形式展示数据</li>
          <li><strong>特点</strong>：按状态分组、支持拖拽</li>
          <li><strong>类比</strong>：像 Trello 看板一样</li>
        </ul>

        <h4>5. 图表区块（Chart）</h4>
        <ul>
          <li><strong>用途</strong>：以图表形式展示数据</li>
          <li><strong>特点</strong>：支持折线图、柱状图、饼图等</li>
          <li><strong>类比</strong>：像数据分析仪表盘一样</li>
        </ul>

        <h3>如何给表格区块添加操作</h3>
        <p>操作让用户能够与数据进行交互，以下是添加"新增"操作的步骤：</p>
        <ol>
          <li><strong>第一步：进入配置模式</strong> - 点击右上角的荧光笔图标</li>
          <li><strong>第二步：选择表格区块</strong> - 点击页面上的表格区块</li>
          <li><strong>第三步：打开配置面板</strong> - 点击区块右上角的"齿轮"图标</li>
          <li><strong>第四步：添加操作</strong> - 在左侧找到"操作"选项，勾选"新增"</li>
          <li><strong>第五步：保存配置</strong> - 点击保存，切换到使用模式即可</li>
        </ol>

        <h3>常用操作类型</h3>
        <table>
          <tr><th>操作</th><th>功能</th><th>说明</th></tr>
          <tr><td>新增</td><td>Create</td><td>添加新记录</td></tr>
          <tr><td>查看</td><td>View</td><td>查看详情</td></tr>
          <tr><td>编辑</td><td>Edit</td><td>修改数据</td></tr>
          <tr><td>删除</td><td>Delete</td><td>删除记录</td></tr>
          <tr><td>批量删除</td><td>Bulk Delete</td><td>批量删除</td></tr>
          <tr><td>导出</td><td>Export</td><td>导出数据</td></tr>
        </table>
        <p>📚 参考文档：</p>
        <ul>
          <li><a href="https://docs.nocobase.com/cn/tutorials/v2/actions" target="_blank">Actions</a></li>
          <li><a href="https://docs.nocobase.com/cn/tutorials/v2/quick-start" target="_blank">快速开始</a></li>
        </ul>
      </div>
    `,
    exercises: [
      { question: "Collection 和 Field 分别是什么？有什么区别？" },
      { question: "常用的区块类型有哪些？它们各自的用途是什么？" },
      { question: "如何给表格区块添加「新增」操作？请描述具体步骤。" }
    ]
  },
  4: {
    title: '数据建模基础',
    content: `
      <div class="section">
        <h3>学习目标</h3>
        <p>掌握 NocoBase 数据建模的基本方法，学会创建 Collection 和 Field</p>
        
        <h3>什么是数据建模？</h3>
        <p>数据建模就是确定业务需要哪些数据、数据如何组织、数据之间的关系是什么的过程。</p>
        <p>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/collections" target="_blank">Collections</a></p>

        <h3>数据建模步骤</h3>
        <ol>
          <li><strong>分析业务需求</strong> - 明确需要管理哪些业务对象</li>
          <li><strong>识别实体</strong> - 确定有哪些独立的数据对象</li>
          <li><strong>定义属性</strong> - 为每个实体添加字段</li>
          <li><strong>建立关系</strong> - 确定实体之间的关联关系</li>
        </ol>

        <h3>创建 Collection 的步骤</h3>
        <ol>
          <li>进入"数据管理" → "数据表管理"</li>
          <li>点击"新建表"</li>
          <li>填写表名称、描述</li>
          <li>添加字段（Field）</li>
          <li>配置字段类型、选项</li>
          <li>保存</li>
        </ol>

        <h3>实例：创建产品管理模块</h3>
        <p><strong>实体识别：</strong>产品、分类、供应商</p>
        <p><strong>产品表（Products）字段：</strong></p>
        <ul>
          <li>产品名称（单行文本）</li>
          <li>SKU 编码（单行文本）</li>
          <li>价格（数字）</li>
          <li>库存数量（数字）</li>
          <li>产品描述（多行文本）</li>
          <li>分类（关联字段）</li>
          <li>供应商（关联字段）</li>
          <li>上架状态（开关）</li>
          <li>创建时间（日期）</li>
        </ul>

        <h3>字段配置要点</h3>
        <ul>
          <li><strong>必填字段</strong>：设置为必填，保证数据完整性</li>
          <li><strong>默认值</strong>：为常用字段设置默认值</li>
          <li><strong>唯一约束</strong>：确保编码类字段不重复</li>
          <li><strong>验证规则</strong>：设置格式验证（邮箱、手机号等）</li>
        </ul>
        <p>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/fields" target="_blank">字段配置</a></p>
      </div>
    `,
    exercises: [
      { question: "请简述数据建模的基本步骤有哪些？" },
      { question: "创建 Collection 时需要考虑哪些字段配置要点？" },
      { question: "假设你要创建一个客户管理系统，你会设计哪些 Collection 和字段？" }
    ]
  },
  5: {
    title: '数据建模进阶',
    content: `
      <div class="section">
        <h3>学习目标</h3>
        <p>掌握数据关联、公式字段、索引、视图等高级特性</p>
        
        <h3>数据关联（Relationships）</h3>
        <p>数据关联定义不同 Collection 之间的关系：</p>
        <ul>
          <li><strong>一对一（1:1）</strong>：如用户和用户档案</li>
          <li><strong>一对多（1:N）</strong>：如部门和员工</li>
          <li><strong>多对多（N:M）</strong>：如学生和课程</li>
        </ul>
        <p>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/relationships" target="_blank">关联关系</a></p>

        <h3>公式字段（Formula）</h3>
        <p>公式字段可以根据其他字段自动计算值：</p>
        <ul>
          <li><strong>数学运算</strong>：总价 = 单价 × 数量</li>
          <li><strong>日期计算</strong>：年龄 = 当前年份 - 出生年份</li>
          <li><strong>字符串拼接</strong>：完整地址 = 省份 + 城市 + 街道</li>
        </ul>

        <h3>索引（Index）</h3>
        <p>索引可以加速查询：</p>
        <ul>
          <li>为经常搜索的字段添加索引</li>
          <li>为唯一字段添加唯一索引</li>
          <li>复合索引用于多字段组合查询</li>
        </ul>

        <h3>实例：电商订单系统</h3>
        <p><strong>Collection 设计：</strong></p>
        <ul>
          <li><strong>订单表</strong>：订单号、用户ID、状态、总金额、创建时间</li>
          <li><strong>订单明细表</strong>：订单ID、产品ID、数量、单价</li>
          <li><strong>用户表</strong>：用户名、电话、邮箱、地址</li>
          <li><strong>产品表</strong>：产品名、SKU、价格、库存</li>
        </ul>

        <h3>关联设置</h3>
        <ol>
          <li>订单表 → 用户表（多对一）</li>
          <li>订单表 → 订单明细表（一对多）</li>
          <li>订单明细表 → 产品表（多对一）</li>
        </ol>
      </div>
    `,
    exercises: [
      { question: "请列举并说明三种数据关联类型，各举一个业务场景例子。" },
      { question: "公式字段有什么用途？请举3个具体应用场景。" },
      { question: "设计一个简单的学校管理系统，包括学生、课程、成绩，说明它们的关联关系。" }
    ]
  },
  6: {
    title: '界面搭建',
    content: `
      <div class="section">
        <h3>学习目标</h3>
        <p>掌握 NocoBase 页面和菜单配置，学会搭建实用的管理界面</p>
        
        <h3>页面管理</h3>
        <ul>
          <li><strong>创建页面</strong>：新建页面或从模板创建</li>
          <li><strong>页面类型</strong>：表单页、列表页、详情页等</li>
          <li><strong>页面权限</strong>：控制哪些角色可以访问</li>
        </ul>
        <p>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/pages" target="_blank">页面管理</a></p>

        <h3>菜单配置</h3>
        <ol>
          <li>进入"系统管理" → "菜单管理"</li>
          <li>点击"新建菜单"</li>
          <li>配置菜单名称、图标、路由</li>
          <li>设置菜单排序和层级</li>
          <li>关联到具体页面</li>
        </ol>

        <h3>界面布局原则</h3>
        <ul>
          <li><strong>逻辑清晰</strong>：按功能模块分组页面</li>
          <li><strong>使用便捷</strong>：常用功能放在首位</li>
          <li><strong>视觉舒适</strong>：合理使用图标和颜色</li>
          <li><strong>权限分明</strong>：不同角色看到不同菜单</li>
        </ul>

        <h3>实例：客户关系管理系统界面</h3>
        <p><strong>菜单结构：</strong></p>
        <ul>
          <li>
            客户管理
            <ul>
              <li>客户列表（表格区块）</li>
              <li>新增客户（表单区块）</li>
              <li>客户跟进记录</li>
            </ul>
          </li>
          <li>
            销售机会
            <ul>
              <li>机会看板（看板区块）</li>
              <li>销售报表（图表区块）</li>
            </ul>
          </li>
          <li>
            系统设置
            <ul>
              <li>用户管理</li>
              <li>角色配置</li>
            </ul>
          </li>
        </ul>
      </div>
    `,
    exercises: [
      { question: "配置菜单的基本步骤有哪些？" },
      { question: "设计界面布局时需要考虑哪些原则？" },
      { question: "为你所在的业务场景（或你熟悉的业务）设计一套菜单结构。" }
    ]
  },
  7: {
    title: '用户与权限',
    content: `
      <div class="section">
        <h3>学习目标</h3>
        <p>掌握用户管理、角色管理和权限配置，保证系统安全</p>
        
        <h3>用户管理</h3>
        <ul>
          <li><strong>用户信息</strong>：姓名、邮箱、电话、部门</li>
          <li><strong>账号状态</strong>：启用/禁用</li>
          <li><strong>重置密码</strong>：管理员可以重置用户密码</li>
        </ul>
        <p>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/users" target="_blank">用户管理</a></p>

        <h3>角色管理</h3>
        <p>角色是一组权限的集合，可以批量分配给用户：</p>
        <ul>
          <li><strong>内置角色</strong>：超级管理员、管理员、普通用户</li>
          <li><strong>自定义角色</strong>：可以根据业务需求创建</li>
          <li><strong>角色继承</strong>：角色可以继承其他角色的权限</li>
        </ul>
        <p>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/roles" target="_blank">角色管理</a></p>

        <h3>权限控制</h3>
        <p>权限可以细分为：</p>
        <ul>
          <li><strong>菜单权限</strong>：控制能看到哪些菜单</li>
          <li><strong>数据权限</strong>：控制能访问哪些数据</li>
          <li><strong>操作权限</strong>：控制能做哪些操作（查看/新增/编辑/删除）</li>
          <li><strong>字段权限</strong>：控制能看到哪些字段</li>
        </ul>
        <p>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/permissions" target="_blank">权限管理</a></p>

        <h3>权限配置建议</h3>
        <ul>
          <li><strong>最小权限原则</strong>：只给必要的权限</li>
          <li><strong>角色细分</strong>：不同岗位创建不同角色</li>
          <li><strong>定期审计</strong>：检查权限是否合理</li>
          <li><strong>操作日志</strong>：记录关键操作</li>
        </ul>
      </div>
    `,
    exercises: [
      { question: "NocoBase 的权限控制分为哪几个维度？" },
      { question: "为什么要使用角色而不是直接给用户分配权限？" },
      { question: "请为一个典型的企业设计角色体系（至少5个角色）。" }
    ]
  },
  8: {
    title: '工作流',
    content: `
      <div class="section">
        <h3>学习目标</h3>
        <p>了解 NocoBase 工作流功能，学会设计和配置业务流程</p>
        
        <h3>什么是工作流？</h3>
        <p>工作流是一系列有逻辑顺序的任务自动化，用于实现业务流程自动化。</p>
        <p>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/workflow" target="_blank">工作流</a></p>

        <h3>常见应用场景</h3>
        <ul>
          <li><strong>审批流程</strong>：请假审批、报销审批</li>
          <li><strong>数据同步</strong>：新建数据时同步到其他系统</li>
          <li><strong>自动通知</strong>：订单变化时通知相关人员</li>
          <li><strong>数据计算</strong>：自动更新关联数据</li>
        </ul>

        <h3>工作流设计步骤</h3>
        <ol>
          <li><strong>定义触发条件</strong>：什么情况下启动工作流</li>
          <li><strong>设计流程节点</strong>：按顺序配置处理步骤</li>
          <li><strong>配置分支条件</strong>：不同情况走不同分支</li>
          <li><strong>设置权限控制</strong>：每个节点由谁处理</li>
          <li><strong>测试和发布</strong>：先测试再上线</li>
        </ol>

        <h3>实例：请假审批流程</h3>
        <ul>
          <li><strong>触发条件</strong>：员工提交请假申请</li>
          <li><strong>节点1</strong>：自动验证请假天数是否在可用天数内</li>
          <li><strong>节点2</strong>：发送给部门主管审批</li>
          <li><strong>节点3</strong>：如3天以上，需要HR二次审批</li>
          <li><strong>节点4</strong>：审批通过后，发送通知给员工和行政</li>
        </ul>
      </div>
    `,
    exercises: [
      { question: "工作流可以应用在哪些业务场景？请举3个例子。" },
      { question: "设计一个完整的采购审批流程。" },
      { question: "工作流与权限系统如何配合使用？" }
    ]
  },
  9: {
    title: '部署与运维',
    content: `
      <div class="section">
        <h3>学习目标</h3>
        <p>掌握 NocoBase 的生产环境部署、备份和监控</p>
        
        <h3>生产环境部署</h3>
        <ul>
          <li><strong>服务器配置</strong>：CPU、内存、硬盘建议</li>
          <li><strong>数据库配置</strong>：PostgreSQL 最佳实践</li>
          <li><strong>反向代理</strong>：使用 Nginx 配置 SSL</li>
          <li><strong>域名配置</strong>：配置正式域名访问</li>
        </ul>
        <p>📚 参考文档：<a href="https://docs.nocobase.com/cn/getting-started/deployment" target="_blank">部署指南</a></p>

        <h3>数据备份</h3>
        <ul>
          <li><strong>定期备份</strong>：每日自动备份数据库</li>
          <li><strong>文件备份</strong>：备份上传的文件</li>
          <li><strong>备份验证</strong>：定期测试备份恢复</li>
          <li><strong>异地容灾</strong>：重要数据异地存储</li>
        </ul>

        <h3>系统监控</h3>
        <ul>
          <li><strong>资源监控</strong>：CPU、内存、磁盘使用率</li>
          <li><strong>日志管理</strong>：定期清理日志，保留重要记录</li>
          <li><strong>性能监控</strong>：监控系统响应时间</li>
        </ul>

        <h3>常见运维命令</h3>
        <pre>
docker compose ps        # 查看服务状态
docker compose stop      # 停止服务
docker compose restart   # 重启服务
docker compose down      # 彻底停止并删除容器
docker compose pull      # 拉取最新镜像
docker compose up -d     # 更新并启动服务
        </pre>
      </div>
    `,
    exercises: [
      { question: "生产环境部署需要考虑哪些方面？" },
      { question: "数据备份策略应该包括哪些内容？" },
      { question: "请写一个简单的 NocoBase 运维检查清单。" }
    ]
  },
  10: {
    title: '常见问题排查（一）',
    content: `
      <div class="section">
        <h3>学习目标</h3>
        <p>掌握常见问题的排查方法，能够独立解决用户反馈的问题</p>
        
        <h3>问题分类</h3>
        <ul>
          <li><strong>安装部署问题</strong>：无法启动、端口冲突</li>
          <li><strong>数据问题</strong>：数据丢失、查询慢</li>
          <li><strong>权限问题</strong>：无法访问、操作无权限</li>
          <li><strong>界面问题</strong>：页面白屏、样式错乱</li>
        </ul>

        <h3>日志查看</h3>
        <ul>
          <li><strong>应用日志</strong>：docker compose logs app</li>
          <li><strong>数据库日志</strong>：查看数据库操作日志</li>
          <li><strong>浏览器控制台</strong>：F12 打开开发者工具</li>
        </ul>

        <h3>常见问题案例</h3>
        <h4>1. 无法登录系统</h4>
        <p>排查步骤：检查账号密码、检查用户状态、查看日志</p>
        
        <h4>2. 表格数据不显示</h4>
        <p>排查步骤：检查数据源连接、检查权限、检查筛选条件</p>
        
        <h4>3. 上传文件失败</h4>
        <p>排查步骤：检查存储空间、检查文件类型限制、检查文件大小限制</p>

        <h3>排查技巧</h3>
        <ol>
          <li><strong>复现问题</strong>：先确认能稳定复现问题</li>
          <li><strong>简化场景</strong>：排除复杂配置，用最小用例测试</li>
          <li><strong>查看日志</strong>：日志是排查的第一手资料</li>
          <li><strong>对比正常</strong>：与正常情况对比找差异</li>
        </ol>
      </div>
    `,
    exercises: [
      { question: "排查问题时，为什么日志很重要？" },
      { question: "用户反馈无法访问某个功能页面，你怎么排查？" },
      { question: "如果表格查询很慢，可能是什么原因？怎么优化？" }
    ]
  },
  11: {
    title: '常见问题排查（二）',
    content: `
      <div class="section">
        <h3>学习目标</h3>
        <p>继续学习更多复杂问题的排查，掌握性能优化方法</p>
        
        <h3>性能优化</h3>
        <h4>数据库优化</h4>
        <ul>
          <li>为经常查询的字段添加索引</li>
          <li>优化复杂 SQL 查询</li>
          <li>定期清理历史数据</li>
        </ul>

        <h4>前端优化</h4>
        <ul>
          <li>合理分页，避免一次性加载大量数据</li>
          <li>使用懒加载，按需加载组件</li>
          <li>图片和资源压缩</li>
        </ul>

        <h3>数据问题案例</h3>
        <h4>1. 数据重复</h4>
        <p>排查步骤：检查唯一约束、检查并发操作</p>
        
        <h4>2. 数据不一致</h4>
        <p>排查步骤：检查事务、检查关联更新逻辑</p>
        
        <h4>3. 数据丢失</h4>
        <p>排查步骤：检查删除操作日志、检查备份</p>

        <h3>升级和迁移</h3>
        <ul>
          <li><strong>升级前备份</strong>：一定要先备份再升级</li>
          <li><strong>阅读更新日志</strong>：了解有哪些变更</li>
          <li><strong>测试环境验证</strong>：先在测试环境测试</li>
        </ul>

        <h3>寻求帮助</h3>
        <ul>
          <li>先看文档：<a href="https://docs.nocobase.com/cn/" target="_blank">官方文档</a></li>
          <li>GitHub 提 issue：<a href="https://github.com/nocobase/nocobase/issues" target="_blank">Issues</a></li>
          <li>社区论坛交流</li>
        </ul>
      </div>
    `,
    exercises: [
      { question: "NocoBase 升级需要注意什么？" },
      { question: "如何提高系统查询性能？" },
      { question: "发现数据不一致时，你会怎么排查和修复？" }
    ]
  },
  12: {
    title: '高级功能了解',
    content: `
      <div class="section">
        <h3>学习目标</h3>
        <p>了解 NocoBase 的高级功能，知道哪些问题可以用这些功能解决</p>
        
        <h3>AI 功能</h3>
        <ul>
          <li>智能数据分析</li>
          <li>自动生成报表</li>
          <li>对话式查询</li>
          <li>文本翻译和总结</li>
        </ul>
        <p>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/ai" target="_blank">AI 功能</a></p>

        <h3>API 接口</h3>
        <p>NocoBase 自动生成 RESTful API：</p>
        <ul>
          <li>自动生成 API 文档</li>
          <li>支持自定义 API</li>
          <li>Webhook 回调</li>
        </ul>

        <h3>多语言支持</h3>
        <ul>
          <li>内置多语言框架</li>
          <li>自定义语言包</li>
          <li>用户界面语言切换</li>
        </ul>

        <h3>其他功能</h3>
        <ul>
          <li><strong>定时任务</strong>：按计划执行自动任务</li>
          <li><strong>数据导入导出</strong>：Excel、CSV 等格式</li>
          <li><strong>审计日志</strong>：记录所有关键操作</li>
          <li><strong>消息通知</strong>：系统通知、邮件通知</li>
        </ul>
      </div>
    `,
    exercises: [
      { question: "NocoBase 的 AI 功能有什么用途？" },
      { question: "API 接口在什么场景下会用到？" },
      { question: "你最感兴趣的高级功能是什么？为什么？" }
    ]
  },
  13: {
    title: '插件开发基础',
    content: `
      <div class="section">
        <h3>学习目标</h3>
        <p>了解 NocoBase 插件开发机制，知道如何扩展功能</p>
        
        <h3>什么是插件？</h3>
        <p>NocoBase 采用插件化架构，所有功能都是独立插件，可以灵活扩展。</p>
        <p>📚 参考文档：<a href="https://docs.nocobase.com/cn/tutorials/v2/plugin" target="_blank">插件开发</a></p>

        <h3>插件类型</h3>
        <ul>
          <li><strong>字段插件</strong>：自定义字段类型</li>
          <li><strong>区块插件</strong>：自定义区块</li>
          <li><strong>操作插件</strong>：自定义操作</li>
          <li><strong>完整业务插件</strong>：完整的业务模块</li>
        </ul>

        <h3>开发环境</h3>
        <ul>
          <li>Node.js 开发环境</li>
          <li>TypeScript 语言</li>
          <li>React + Ant Design 前端框架</li>
          <li>开发文档和示例</li>
        </ul>

        <h3>何时需要插件开发？</h3>
        <ul>
          <li>现有功能无法满足需求</li>
          <li>需要集成外部系统</li>
          <li>需要自定义特殊交互</li>
          <li>需要行业特定功能</li>
        </ul>
      </div>
    `,
    exercises: [
      { question: "NocoBase 的插件架构有什么优势？" },
      { question: "什么情况下建议使用插件开发？" },
      { question: "你会考虑开发什么插件？为什么？" }
    ]
  },
  14: {
    title: '售后实战模拟',
    content: `
      <div class="section">
        <h3>学习目标</h3>
        <p>通过真实案例模拟，综合应用所学知识解决问题</p>
        
        <h3>场景 1：新功能上线</h3>
        <p><strong>需求</strong>：用户需要一个新的"合同管理"模块</p>
        <p><strong>任务</strong>：设计数据结构、配置界面、设置权限</p>

        <h3>场景 2：问题排查</h3>
        <p><strong>问题描述</strong>：用户反馈"打开订单列表非常慢"</p>
        <p><strong>任务</strong>：分析原因、优化查询、验证效果</p>

        <h3>场景 3：权限调整</h3>
        <p><strong>需求</strong>：销售人员只能看到自己负责的客户</p>
        <p><strong>任务</strong>：配置数据权限、测试验证</p>

        <h3>场景 4：系统迁移</h3>
        <p><strong>需求</strong>：将旧系统数据迁移到 NocoBase</p>
        <p><strong>任务</strong>：设计迁移方案、编写导入脚本、验证数据</p>

        <h3>售后沟通技巧</h3>
        <ul>
          <li>先理解问题，不要急于解决</li>
          <li>多问问题，引导用户详细描述</li>
          <li>及时反馈进度</li>
          <li>问题解决后，做记录总结</li>
        </ul>
      </div>
    `,
    exercises: [
      { question: "面对用户问题时，你应该先做什么？" },
      { question: "如何让用户满意地解决问题？" },
      { question: "记录和总结售后问题有什么好处？" }
    ]
  },
  15: {
    title: '毕业考核',
    content: `
      <div class="section">
        <h3>考核目标</h3>
        <p>综合检查 15 天学习成果，确保你已具备成为 NocoBase 售后支持的能力</p>
        
        <h3>考核内容</h3>
        <ol>
          <li><strong>产品知识</strong>：核心理念、基础概念、功能模块</li>
          <li><strong>操作技能</strong>：能独立完成系统配置和数据建模</li>
          <li><strong>问题排查</strong>：能独立排查和解决常见问题</li>
          <li><strong>最佳实践</strong>：知道什么是好的做法</li>
        </ol>

        <h3>综合实践项目</h3>
        <p><strong>项目目标</strong>：使用 NocoBase 搭建一个简单的项目管理系统</p>
        <p><strong>功能要求</strong>：</p>
        <ul>
          <li>项目管理：创建、编辑、查看项目</li>
          <li>任务管理：添加任务、分配负责人、更新状态</li>
          <li>成员管理：团队成员管理</li>
          <li>进度看板：用看板展示任务进度</li>
          <li>权限控制：不同角色看到不同内容</li>
        </ul>

        <h3>学习回顾</h3>
        <p>回顾一下这 15 天学到的内容：</p>
        <ul>
          <li>Day 1-3：认识 NocoBase、安装部署、基础功能</li>
          <li>Day 4-6：数据建模、界面搭建</li>
          <li>Day 7-9：权限、工作流、部署运维</li>
          <li>Day 10-12：问题排查、高级功能</li>
          <li>Day 13-15：插件开发、实战模拟、考核</li>
        </ul>

        <h3>恭喜毕业！</h3>
        <p>🎉 恭喜完成 NocoBase 15 天学习计划！</p>
        <p>现在你已具备 NocoBase 售后技术支持的基本能力，继续实践和学习，你会越来越熟练！</p>
        <p>💡 继续关注官方文档和社区，保持学习！</p>
      </div>
    `,
    exercises: [
      { question: "请总结这 15 天你学到的最重要的 5 个知识点。" },
      { question: "设计一个项目管理系统的 Collection 结构。" },
      { question: "你后续打算如何继续学习和提升 NocoBase 技能？" }
    ]
  }
}

const dayTitle = computed(() => dayData[dayId.value]?.title || '')
const content = computed(() => dayData[dayId.value]?.content || '')
const exercises = computed(() => dayData[dayId.value]?.exercises || [])

const goBack = () => {
  router.push('/')
}

const markComplete = async () => {
  try {
    await updateProgress({
      day: dayId.value,
      completed: true
    })
    progress.value.completed = true
    alert('恭喜完成今天的学习！')
  } catch (error) {
    console.error('Failed to update progress:', error)
  }
}

const submitAnswers = async () => {
  try {
    for (let i = 0; i < answers.value.length; i++) {
      if (answers.value[i]) {
        const result = await submitAnswer({
          day: dayId.value,
          question: i + 1,
          answer: answers.value[i]
        })
        savedAnswersData.value[i] = {
          score: result.data.score,
          feedback: result.data.feedback,
          reference: result.data.reference
        }
      }
    }
    alert('答案已提交！')
  } catch (error) {
    console.error('Failed to submit answers', error)
  }
}

const getScoreClass = (score) => {
  if (score >= 8) return 'score-good'
  if (score >= 5) return 'score-medium'
  return 'score-bad'
}

onMounted(async () => {
  try {
    const res = await getDayProgress(dayId.value)
    progress.value = res.data
    
    const answersRes = await getAnswers(dayId.value)
    savedAnswers.value = answersRes.data
    answers.value = exercises.value.map((_, i) => {
      const saved = savedAnswers.value.find(a => a.question === i + 1)
      if (saved) {
        savedAnswersData.value[i] = {
          score: saved.score,
          feedback: saved.feedback,
          reference: null
        }
      }
      return saved?.answer || ''
    })
  } catch (error) {
    console.error('Failed to load day data', error)
  } finally {
    loading.value = false
  }
})
</script>
