# v0.1.0 MVP Release

## 项目名称
wechat-support-agent

## v0.1.0 MVP 说明
v0.1.0 是“微信/类微信远程技术支持 Agent 分身”的阶段性 MVP。它使用静态 Web 页面模拟客户咨询，使用 FastAPI 后端完成问题分类、知识库引用、技术支持追问和结构化工单摘要生成。

## Agent 提效场景
本项目选择的 Agent 提效场景是：微信/类微信远程技术支持 Agent 分身。

## AI 小工具
本项目中的 AI 辅助小工具是：技术支持工单摘要生成器。

## 核心功能
- Web 模拟微信客服聊天页面。
- FastAPI mock API。
- 关键词规则问题分类。
- 6 类 Markdown 技术支持知识库。
- `/chat` 返回分类、知识库引用和下一步追问。
- `/summary` 根据聊天记录生成结构化工单摘要草稿。
- README、docs 和 examples 展示材料。

## 本地运行方式
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

## 测试命令
```powershell
python -m pytest tests/test_backend_api.py
python -m pytest tests/test_classifier.py
python -m pytest tests/test_knowledge_base.py
python -m pytest tests/test_ticket_summary.py
```

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
- 高风险操作必须人工确认。
