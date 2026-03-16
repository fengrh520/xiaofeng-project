# 🚀 从零打造 AI 提示词优化助手：Vue3 + Django 全栈开发实战复盘

> **摘要**：在 AI 时代，Prompt（提示词）的质量直接决定了生成内容的上限。本文将详细复盘如何使用 Vue 3 和 Django 5 打造一款全栈“AI 提示词优化助手”。我们将深入探讨 Prompt 工程的重要性，剖析前后端分离架构的设计思路，还原从环境搭建到功能实现的完整过程，并分享开发过程中遇到的“坑”与解决方案。无论你是全栈新手还是 AI 爱好者，这篇 3000 字实战指南都能给你带来启发。

---

## 📖 一、为什么我们需要“优化 Prompt”？

### 1.1 AI 的“听不懂”困境
你是否遇到过这种情况：让 AI 写一篇文章，结果它生成的废话连篇；或者让它写一段代码，结果漏洞百出。这往往不是 AI 不够聪明，而是我们的**指令（Prompt）不够清晰**。

### 1.2 什么是结构化 Prompt？
一个高质量的 Prompt 通常包含以下核心要素：
- **角色设定 (Role)**：你希望 AI 扮演什么角色（如“资深 Python 工程师”）。
- **任务目标 (Task)**：具体要做什么（如“解释这段代码的内存泄漏原因”）。
- **约束条件 (Constraints)**：字数限制、格式要求、禁止事项。
- **输出格式 (Format)**：Markdown 表格、JSON、代码块等。

### 1.3 本项目的作用
“小封机器人”旨在解决普通用户不会写复杂 Prompt 的痛点。用户只需输入一句简单的话（如“帮我写个周报”），系统会自动调用大模型（Moonshot AI），将其扩充为结构清晰、逻辑严密的**专家级 Prompt**，从而让 AI 的回答质量提升 10 倍以上。

---

## 🛠️ 二、技术栈选型与架构设计

本项目采用经典的前后端分离架构，兼顾了开发的灵活性与系统的扩展性。

### 2.1 前端：现代化的交互体验 (Vue 3 生态)
- **核心框架**：**Vue 3 (Composition API)** —— 相比 Vue 2，逻辑复用更强，代码组织更清晰。
- **构建工具**：**Vite** —— 秒级启动，热更新极快，极大提升开发效率。
- **UI 组件库**：**Element Plus** —— 提供成熟的 Layout、Form、Table 组件，快速搭建高颜值界面。
- **状态管理**：**Pinia** —— Vuex 的继任者，API 更简洁，完美支持 TypeScript（本项目虽用 JS 但也享受到自动补全）。
- **路由管理**：**Vue Router 4** —— 管理单页应用（SPA）的页面跳转与权限控制。
- **HTTP 客户端**：**Axios** —— 处理 API 请求，配置拦截器实现 JWT Token 的自动携带与刷新。

### 2.2 后端：稳健的数据接口 (Django 生态)
- **Web 框架**：**Django 5** —— Python 界最强大的 Web 框架，内置 Admin 后台、ORM 系统，开箱即用。
- **API 框架**：**Django REST Framework (DRF)** —— 快速构建符合 RESTful 规范的 API 接口，提供序列化器（Serializer）和视图集（ViewSet）。
- **身份认证**：**SimpleJWT** —— 基于 JSON Web Token 的无状态认证机制，完美适配前后端分离场景。
- **AI 接入**：**Moonshot AI SDK (OpenAI 兼容)** —— 调用 Kimi 大模型进行 Prompt 优化。
- **数据增强**：**django-filter** —— 实现复杂的搜索、筛选（Star/Pin）和排序功能。
- **跨域处理**：**django-cors-headers** —— 解决浏览器同源策略限制，允许前端（5173 端口）访问后端（8000 端口）。

### 2.3 数据库与版本控制
- **数据库**：**SQLite** (开发阶段) —— 轻量级，无需配置，文件型数据库。
- **版本控制**：**Git** —— 分支管理（feature/bugfix），`.gitignore` 敏感文件过滤。

---

## 💻 三、制作过程全复盘

### 第一阶段：环境搭建与“Hello World”

#### 1. 后端初始化
我们首先创建了 Django 项目 `backend`。为了保持环境纯净，使用了 `venv` 虚拟环境。
```bash
# 创建虚拟环境
python -m venv venv
# 激活环境 (Windows)
.\venv\Scripts\activate
# 安装依赖
pip install django djangorestframework django-cors-headers
# 创建项目
django-admin startproject config .
```
**关键点**：配置 `settings.py`，注册 `rest_framework` 和 `corsheaders` 应用，并设置 `CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]`，这是前后端联调的第一道关卡。

#### 2. 前端初始化
使用 Vite 快速生成 Vue 3 项目 `frontend`。
```bash
npm create vite@latest frontend -- --template vue
cd frontend
npm install axios element-plus pinia vue-router
npm run dev
```
此时，前端运行在 5173，后端运行在 8000，虽然还没连通，但地基已打好。

---

### 第二阶段：AI 核心功能实现

这是项目的灵魂。我们在后端创建了一个 `api` 应用，定义了核心逻辑。

#### 1. 调用 Moonshot AI
我们没有把 API Key 暴露给前端，而是通过后端代理转发。这不仅安全，还能在后端做流控和日志。
```python
# backend/api/utils.py (简化版)
from openai import OpenAI

def optimize_prompt(user_input):
    client = OpenAI(api_key="sk-...", base_url="https://api.moonshot.cn/v1")
    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system", "content": "你是一个 Prompt 优化专家..."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content
```

#### 2. 前端流式体验
虽然目前后端是同步返回，但在前端我们设计了“加载中”状态（Loading Spinner），让用户感知到 AI 正在思考。未来计划升级为 SSE（Server-Sent Events）流式输出，像 ChatGPT 那样打字机效果。

---

### 第三阶段：用户认证与数据隔离 (难点攻克)

为了让每个用户只能看到自己的 Prompt，我们引入了 JWT 认证。

#### 1. 认证流程
1. 用户在前端输入账号密码 -> POST `/api/token/`。
2. 后端验证成功，返回 `access` 和 `refresh` 两个 Token。
3. 前端将 Token 存入 `localStorage`。
4. **Pinia Store** 更新登录状态 `isAuthenticated = true`。
5. **Axios 拦截器** 自动在后续请求头中带上 `Authorization: Bearer <token>`。

#### 2. 数据隔离 (Data Isolation)
这是后端最关键的一行代码。通过重写 `get_queryset` 方法，确保用户只能操作自己的数据。
```python
# backend/api/views.py
class PromptViewSet(viewsets.ModelViewSet):
    # ...
    def get_queryset(self):
        # 👑 核心逻辑：只返回当前登录用户的数据
        return Prompt.objects.filter(user=self.request.user).order_by('-created_at')
```

---

### 第四阶段：功能增强与体验优化

#### 1. 搜索与筛选
利用 `django-filter`，我们轻松实现了复杂的查询功能。前端只需在 URL 参数中传递 `?search=周报&is_starred=true`，后端自动处理过滤逻辑，无需手写大量 `if-else`。

#### 2. 交互细节
- **侧边栏历史记录**：我们重构了 `Home.vue`，加入了侧边栏，用户可以点击历史记录回溯之前的优化结果。
- **置顶与星标**：实现了类似微信聊天置顶的功能，重要 Prompt 永不沉底。
- **防白屏处理**：在路由守卫（Router Guard）中增加了容错逻辑，防止用户访问不存在的路由导致页面崩溃。

---

## 🐛 四、踩坑记录与避坑指南

### 4.1 CORS 跨域噩梦
**现象**：前端报错 `Access to XMLHttpRequest ... has been blocked by CORS policy`。
**原因**：Vite 在端口被占用时会自动切换到 5174，而 Django 配置死板地只允许 5173。
**解决**：
1. 修改 Django `settings.py`，添加 `http://localhost:5174`。
2. 同时也教会了我们：开发环境要关注终端输出的实际端口号。

### 4.2 数据库迁移冲突
**现象**：给 `Prompt` 模型添加 `user` 字段时，报错 `IntegrityError`。
**原因**：旧数据没有 `user`，而新字段规定 `null=False`。
**解决**：在开发阶段，最暴力的解法是“删库跑路”——删除 `db.sqlite3` 和 `migrations` 文件夹（保留 `__init__.py`），重新 `makemigrations`。生产环境则需要提供 `default` 值或分步迁移。

### 4.3 Git 身份验证
**现象**：`git commit` 报错 `Author identity unknown`。
**原因**：新电脑未配置 Git 全局用户。
**解决**：使用 `git config user.name "..."` 配置当前仓库身份。

---

## 🔮 五、未来展望

目前项目已发布 v1.0 版本，实现了核心闭环。接下来的 v1.1 版本，我们计划：
1. **数据可视化**：引入 ECharts，统计用户的 Prompt 优化频率和高频词云。
2. **社区分享**：允许用户将优质 Prompt 公开到“模板广场”。
3. **多模型切换**：支持 GPT-4、Claude 3 等更多模型。

---

> **结语**：全栈开发不仅是技术的堆砌，更是对产品逻辑的深度理解。通过这个项目，我们不仅掌握了 Vue3 + Django 的最佳实践，更深刻体会到了 AI 如何赋能传统开发。希望这篇文章能为你提供参考，欢迎在评论区交流你的想法！

*(本文配图建议：架构图、前端界面截图、Postman 接口测试图、Git 分支管理图)*
