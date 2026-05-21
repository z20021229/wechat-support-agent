# wechat-support-agent

## 项目简介
wechat-support-agent 是一个“微信远程技术支持 Agent 分身”的 MVP 项目。第一版不接真实微信，而是用 Web 页面模拟客户在微信中咨询技术问题，帮助验证技术支持 Agent 的接待、信息收集、分类、排查建议和工单摘要流程。

## 解决的问题
远程技术支持通常需要反复追问问题背景、设备环境、错误现象和已尝试操作。这个项目希望用 Agent 流程减少人工接待中的重复工作，并为后续工单处理提供结构化摘要。

## MVP 功能
计划中的 MVP 功能包括：
- 模拟客户咨询入口。
- 技术问题接待和澄清提问。
- 基础信息收集。
- 问题分类。
- 排查建议生成。
- 工单摘要生成。

当前仓库处于第 1 阶段：Backend mock API skeleton completed。已完成后端 FastAPI mock 服务，前端聊天页面、真实微信接入、真实 LLM API、SQLite 和知识库读取尚未实现。

## 技术栈
- 后端：Python FastAPI
- 前端：HTML + CSS + JavaScript
- 数据库：SQLite
- 知识库：Markdown
- 第一版不接真实微信
- 第一版不接真实 LLM API，先使用 mock
- 后续可扩展企业微信或微信客服接口

## 多 Agent 开发模式
项目采用 Main Agent 监控 + 子 Agent 分工的方式开发：
- Main Agent：控制阶段边界、任务拆分、审查和集成。
- Backend Agent：负责后端 API、SQLite 和 mock Agent 服务的后续实现。
- Frontend Agent：负责 Web 模拟咨询界面的后续实现。
- Knowledge Agent：负责 Markdown 知识库和提示词素材。
- Test Agent：负责测试策略和自动化测试。
- Docs Agent：负责文档、路线图和安全说明。

详细规则见 `AGENTS.md` 和 `docs/multi_agent_workflow.md`。

## 项目目录结构
```text
wechat-support-agent/
├── backend/
├── frontend/
├── knowledge/
├── prompts/
├── docs/
├── examples/
├── tests/
├── AGENTS.md
├── README.md
├── .gitignore
└── LICENSE
```

## 当前状态
当前状态：第 1 阶段：Backend mock API skeleton completed。

当前已完成：
- FastAPI 后端 mock 服务。
- `GET /health`。
- `POST /chat`。
- `POST /summary`。
- 后端基础测试 3 passed。

当前未完成：
- 未实现前端聊天页面。
- 未接入真实微信。
- 未接入真实 LLM API。
- 未实现 SQLite。
- 未实现知识库读取。

## 后端本地启动
```powershell
cd D:\codex-projects\wechat-support-agent
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

## 后续路线图
- 第 1 阶段：定义后端最小接口契约和 mock Agent 流程。
- 第 2 阶段：实现 Web 模拟咨询页面并连接 mock 后端。
- 第 3 阶段：整理 Markdown 知识库样例和问题分类规则。
- 第 4 阶段：生成工单摘要并完成端到端演示。
- 第 5 阶段：评估真实企业微信、微信客服或 LLM API 接入方案。

## 安全说明
第一版只使用 mock，不接真实微信、不接真实 LLM API、不保存真实客户信息。仓库中不得写入账号、密码、密钥、token、真实客户资料、真实 IP 或内部系统地址。后续任何真实服务接入都必须先完成安全设计和审查。
