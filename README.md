# Agent Workspace

Agent Workspace 是一个面向 AI Agent 工程能力展示的全栈项目。  
当前完成的是 v1 阶段的 Day 1 到 Day 7，已经具备可运行、可演示、可扩展的最小闭环。

## 项目简介

用户输入一个任务后，系统会判断是否需要：

- 直接回答
- 检索知识库
- 调用工具

然后返回：

- 最终回答
- intent 类型
- sources
- tool calls
- trace

## 核心功能

当前版本已完成：

- Chat UI：支持消息输入、消息流展示、loading 和 error 状态
- Intent Classifier：规则版 `direct_answer / knowledge_qa / tool_call`
- Direct Answer：支持真实 LLM 接入，未配置时安全回退
- Tool Calling：已接入 `calculator_tool`
- RAG 占位能力：已接入 `document_lookup_tool` mock 检索
- Trace / Sources / Tool Calls 面板：适合 demo 展示

## 系统架构

```text
[Next.js Web App]
        |
        | HTTP
        v
[FastAPI Backend]
        |
        v
[Agent Orchestrator]
  |- Intent Classifier
  |- Decision Router
  |- LLM Service
  |- Tool Executor
  \- Retrieval Stub
```

## 技术栈

### 前端

- Next.js 15
- TypeScript
- Tailwind CSS
- React Query

### 后端

- FastAPI
- Pydantic v2
- Uvicorn
- Python unittest

## 目录结构

```text
agent-workspace/
  apps/
    api/
      app/
        agents/
        api/
        core/
        schemas/
        services/
        tools/
      tests/
      .env.example
    web/
      app/
      components/
      hooks/
      lib/
      types/
      .env.example
  docs/
    Agent Workspace v1 技术设计文档.md
  .env.example
  package.json
  README.md
```

## 本地启动

### 1. 安装前端依赖

```bash
npm install
```

### 2. 准备后端虚拟环境

如果 `apps/api/.venv` 还不存在：

```bash
cd apps/api
python3 -m venv .venv
./.venv/bin/pip install fastapi httpx pydantic pydantic-settings "uvicorn[standard]"
cd ../..
```

### 3. 配置环境变量

根目录有一份统一参考配置：[.env.example](/Users/alucard/Code/AlucPro/agent-workspace/.env.example)

后端：

- 复制 `apps/api/.env.example` 为 `apps/api/.env`
- 如果要启用真实 LLM，填入 `OPENAI_API_KEY` 和 `OPENAI_MODEL`

前端：

- 复制 `apps/web/.env.example` 为 `apps/web/.env.local`

### 4. 启动服务

后端：

```bash
npm run dev:api
```

前端：

```bash
npm run dev:web
```

访问：

- Web: [http://localhost:3000](http://localhost:3000)
- API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## 可用脚本

```bash
npm run dev:web
npm run dev:api
npm run build:web
npm run test:api
```

## 示例用例

### 1. Direct Answer

输入：

```text
帮我把这段需求整理成开发任务列表
```

预期：

- intent = `direct_answer`
- 走 LLM 或 fallback direct answer

### 2. Knowledge QA

输入：

```text
总结这份 PRD 里的核心目标，并列出风险点
```

预期：

- intent = `knowledge_qa`
- 返回 sources 和 trace

### 3. Tool Call

输入：

```text
帮我计算 2025 年同比增长率，去年收入 120 万，今年 156 万
```

预期：

- intent = `tool_call`
- `calculator_tool` 返回 `30.00%`
- Tool Calls 面板展示表达式、结果和解释

## 后续路线图

- 文档上传和真实 RAG 流程
- `document_lookup_tool` 接入真实向量检索
- 会话持久化
- 多轮上下文
- README 中的架构图和 demo 截图
