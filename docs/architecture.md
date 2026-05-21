# Architecture

## 总览
wechat-support-agent 当前是一个本地 MVP，由静态前端页面和 FastAPI 后端组成。前端模拟微信客服聊天窗口，后端提供健康检查、聊天回复和工单摘要接口。

## 前端页面
- 文件：`frontend/index.html`、`frontend/app.js`、`frontend/style.css`
- 作用：展示聊天窗口、发送客户问题、展示 Agent 回复、触发工单摘要生成。
- 请求地址固定为 `http://127.0.0.1:8000`。
- 不使用 React、Vue、Webpack、Vite 或 Node 构建链。

## FastAPI 后端
- 文件：`backend/main.py`
- 接口：
  - `GET /health`
  - `POST /chat`
  - `POST /summary`
- 当前后端只使用本地规则和 Markdown 文件，不连接外部服务。

## 问题分类模块
- 文件：`backend/classifier.py`
- 作用：使用关键词规则将客户问题分类为：
  - `database_connection`
  - `permission_error`
  - `sql_error`
  - `performance_issue`
  - `service_unavailable`
  - `other`

## 知识库模块
- 文件：`backend/knowledge_base.py`
- 内容来源：`knowledge/*.md`
- 作用：按分类读取对应 Markdown 知识库，供后端生成更贴近技术支持场景的追问。
- `/chat` 只返回知识库文件引用和可用状态，不返回完整 Markdown 原文。

## 工单摘要模块
- 文件：`backend/ticket_summary.py`
- 作用：根据聊天记录生成结构化工单摘要草稿。
- 当前使用轻量规则提取数据库类型、端口、ping/telnet、SQL、权限、性能等信息。

## 为什么当前不接真实微信
第一版目标是验证技术支持 Agent 的接待、分类、知识库引用和摘要生成流程。真实微信或企业微信接入会引入鉴权、回调、安全审计、消息合规和部署复杂度，因此留到后续阶段评估。

## 为什么当前不接真实 LLM
第一版使用 mock 和规则逻辑，便于快速验证产品流程和代码结构。真实 LLM API 会引入费用、密钥管理、内容安全、隐私保护和不确定输出控制，因此当前不接入。
