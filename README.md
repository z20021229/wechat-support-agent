# wechat-support-agent

## 项目简介
wechat-support-agent 是一个“微信/类微信远程技术支持 Agent 分身”的 MVP。项目使用一个静态 Web 页面模拟客户在微信中咨询技术问题，后端通过 FastAPI、关键词分类、Markdown 知识库和规则版工单摘要生成器，完成接待、信息收集、问题分类、排查建议和工单摘要。

当前状态：第 7 阶段：GitHub documentation and demo examples completed。

Release 状态：`v0.1.0` MVP release prepared。

发布材料：
- [CHANGELOG.md](CHANGELOG.md)
- [RELEASE_NOTES.md](RELEASE_NOTES.md)
- [docs/final_acceptance.md](docs/final_acceptance.md)

## 项目背景
远程技术支持经常需要重复询问客户的环境、报错、操作步骤和影响范围。很多问题在进入人工深度排查前，都可以先由 Agent 完成基础接待、分类和信息收集。

本项目对应两个交付任务：
- 任务 1：选择一个场景，搭建 Agent 来进行提效。本项目选择的场景是：微信/类微信远程技术支持 Agent 分身。
- 任务 2：用 AI 开发一个小工具。本项目中的小工具是：技术支持工单摘要生成器。

## 解决的问题
- 降低技术支持一线反复追问基础信息的成本。
- 将客户描述转换为结构化问题分类和下一步追问。
- 基于聊天记录生成工单摘要草稿，方便人工接手。
- 用 Codex + 多 Agent 分工方式演示一个小型 AI 提效项目的完整开发过程。

## 核心功能
- Web 模拟微信客服聊天页面。
- FastAPI 后端 mock API。
- 关键词规则问题分类。
- 6 类 Markdown 技术支持知识库。
- `/chat` 返回分类、知识库引用和下一步追问。
- `/summary` 根据聊天记录生成结构化工单摘要。
- 基础自动化测试覆盖后端接口、分类器、知识库读取和工单摘要。

## 系统架构
```text
frontend/index.html
  -> POST http://127.0.0.1:8000/chat
  -> POST http://127.0.0.1:8000/summary

FastAPI backend
  -> classifier.py       关键词分类
  -> knowledge_base.py   读取 Markdown 知识库
  -> agent.py            生成技术支持追问
  -> ticket_summary.py   生成结构化工单摘要
```

更多说明见 `docs/architecture.md`。

## 多 Agent 开发模式
项目采用 Main Agent 监控 + 子 Agent 分工：
- Main Agent：控制阶段边界、任务拆分、验收和集成。
- Backend Agent：实现 API、分类、知识库读取和摘要生成。
- Frontend Agent：实现静态聊天页面。
- Knowledge Agent：维护知识库和提示词模板。
- Docs Agent：完善 GitHub 展示文档和演示案例。

这种方式避免一个 Agent 一次性吞掉全部上下文，也减少 Prompt 过杂导致实现越界。详细流程见 `AGENTS.md` 和 `docs/development_workflow.md`。

## 技术栈
- 后端：Python FastAPI
- 前端：HTML + CSS + JavaScript
- 知识库：Markdown
- 分类与摘要：轻量规则
- 测试：pytest + FastAPI TestClient
- 第一版不接真实微信
- 第一版不接真实 LLM API
- SQLite 仅作为后续规划，当前未实现

## 项目目录结构
```text
wechat-support-agent/
├── backend/
│   ├── agent.py
│   ├── classifier.py
│   ├── knowledge_base.py
│   ├── main.py
│   └── ticket_summary.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
├── knowledge/
├── prompts/
├── docs/
├── examples/
├── tests/
├── AGENTS.md
├── README.md
└── LICENSE
```

## 本地运行方式
启动后端：
```powershell
cd D:\codex-projects\wechat-support-agent
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

打开前端：
```text
D:\codex-projects\wechat-support-agent\frontend\index.html
```

前端固定请求后端地址：
```text
http://127.0.0.1:8000
```

## 接口说明
### GET `/health`
返回服务状态。

### POST `/chat`
根据客户输入返回 Agent 回复、分类、知识库引用和下一步追问。

### POST `/summary`
根据聊天记录生成结构化工单摘要草稿。

完整请求和返回示例见 `docs/api_reference.md`。

## 页面演示流程
1. 启动后端。
2. 打开 `frontend/index.html`。
3. 输入 `数据库连接超时` 并点击“发送”。
4. 页面展示客户消息和 Agent mock 回复。
5. 点击“生成工单摘要”。
6. 页面展示结构化工单摘要草稿，包括分类、问题现象、已收集信息、可能原因、建议排查步骤和后续跟进事项。
7. 点击“清空会话”可清空当前聊天记录和工单摘要展示。

展示优化说明：
- 前端工单摘要区域已支持更完整的结构化字段展示。
- 摘要生成器会优先基于最近一条用户问题生成摘要。
- 清空会话按钮可用于演示不同问题场景。

详细演示脚本见 `docs/demo_guide.md`。

## 工单摘要示例
```json
{
  "session_id": "demo-session",
  "title": "数据库连接超时问题",
  "category": "database_connection",
  "label": "数据库连接问题",
  "problem_description": "客户反馈数据库连接超时或无法连接。",
  "collected_info": [
    "数据库类型：GaussDB",
    "端口：8000",
    "telnet 检查：不通"
  ],
  "possible_causes": [
    "数据库服务未监听目标端口",
    "防火墙或安全组拦截",
    "连接地址或端口配置错误"
  ],
  "suggested_steps": [
    "确认数据库服务是否正常运行",
    "检查端口监听状态",
    "检查防火墙或安全组策略",
    "确认客户端连接地址和端口配置"
  ],
  "status": "draft",
  "follow_up": [
    "需要客户补充完整报错截图",
    "需要确认服务端监听状态"
  ]
}
```

更多示例见 `examples/`。

## 测试命令
```powershell
python -m pytest tests/test_backend_api.py
python -m pytest tests/test_classifier.py
python -m pytest tests/test_knowledge_base.py
python -m pytest tests/test_ticket_summary.py
```

## 当前完成状态
当前状态：第 7 阶段：GitHub documentation and demo examples completed。

已完成：
- FastAPI mock API：`GET /health`、`POST /chat`、`POST /summary`。
- 前端模拟微信客服聊天页面。
- 问题分类模块。
- 6 类 Markdown 技术支持知识库。
- 后端根据分类读取知识库并增强 `/chat` 回复。
- 规则版工单摘要生成器。
- GitHub 展示文档和演示案例。

## 未完成项
- 未接入真实微信。
- 未接入真实 LLM API。
- 未实现 SQLite。
- 未实现真实工单持久化。
- 未实现完整多轮对话状态管理。
- 未部署到服务器。

## 安全边界
- 不索要客户密码、密钥、token 或未脱敏日志。
- 不记录真实客户信息、账号、密码、密钥或 IP。
- 当前只使用 mock 和规则逻辑，不调用真实外部 AI 服务。
- 高风险操作，例如删除、重启、修改配置、授权变更，必须人工确认。

## 后续路线图
- 接入 SQLite 保存会话和工单草稿。
- 增加完整多轮对话状态管理。
- 将知识库读取与摘要生成进一步结构化。
- 增加部署脚本和线上演示环境。
- 评估企业微信、微信客服或真实 LLM API 接入方案。

## AI-assisted development
本项目全程使用 Codex 以“主 Agent 监控 + 子 Agent 分工”的方式分阶段开发。每一阶段都限制可修改目录、明确禁止事项、执行验收，并通过 Git commit 记录边界清晰的小步交付。最终产物既是一个可运行的 MVP，也是一个展示 AI 辅助软件工程流程的样例项目。
