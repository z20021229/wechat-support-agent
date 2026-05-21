# Changelog

## v0.1.0

### 已完成能力
- FastAPI mock API：`GET /health`、`POST /chat`、`POST /summary`。
- 静态 Web 模拟微信客服聊天页面。
- 关键词规则问题分类，覆盖 6 类技术支持问题。
- Markdown 技术支持知识库，覆盖数据库连接、权限、SQL 错误、性能、服务不可用和其他问题。
- `/chat` 根据分类返回知识库引用、下一步追问和技术支持回复。
- `/summary` 根据聊天记录生成结构化工单摘要草稿。
- GitHub 展示文档、API 文档、架构说明、演示指南和示例案例。

### 技术栈
- 后端：Python FastAPI
- 前端：HTML + CSS + JavaScript
- 知识库：Markdown
- 分类与摘要：轻量规则
- 测试：pytest + FastAPI TestClient

### 测试结果
- `tests/test_backend_api.py`：3 passed
- `tests/test_classifier.py`：6 passed
- `tests/test_knowledge_base.py`：7 passed
- `tests/test_ticket_summary.py`：6 passed

### 当前限制
- 未接入真实微信。
- 未接入真实 LLM API。
- 未实现 SQLite。
- 未实现真实工单持久化。
- 未实现完整多轮对话状态管理。
- 未部署到服务器。

### 后续计划
- 增加 SQLite 会话和工单草稿存储。
- 增加多轮对话状态管理。
- 增加知识库结构化检索。
- 评估企业微信、微信客服或真实 LLM API 接入方案。
- 准备部署脚本和线上演示环境。
