# Roadmap

本路线图用于冻结 `v0.1.0` 初始 MVP，并规划后续版本。当前仓库仍保持 mock/规则版能力，不接真实微信、不接真实 LLM API、不做数据库持久化。

## v0.1.0：初始 MVP
- 类微信聊天页面。
- FastAPI 后端。
- 问题分类。
- Markdown 知识库。
- 知识库增强回复。
- 工单摘要生成器。
- GitHub 展示文档。

## v0.2.0：Session State
- 多轮会话状态管理。
- 识别已收集信息。
- 识别缺失信息。
- `next_questions` 动态变化。
- `summary` 基于会话状态生成。

## v0.3.0：Persistence
- SQLite 保存会话。
- SQLite 保存工单。
- 查询历史工单。
- 导出工单。

## v0.4.0：Knowledge Retrieval
- 知识库检索增强。
- 从 Markdown 中提取关键排查步骤。
- 回复引用知识库来源。

## v0.5.0：LLM Integration
- 接入真实 LLM API。
- 支持配置 API Key。
- 支持 mock / real 两种模式。

## v0.6.0：WeChat Integration
- 企业微信或微信客服接入方案。
- Webhook 设计。
- 消息收发流程。

## v1.0.0：Deployable Release
- Docker 部署。
- 安全配置。
- 日志审计。
- 可演示部署版本。
