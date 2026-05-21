# Multi-Agent Workflow

## 工作模式
本项目采用 Main Agent 监控 + 子 Agent 分工的开发方式。所有子 Agent 必须在 Main Agent 指定的阶段、目录和任务范围内工作。

## 角色
- Main Agent：阶段控制、任务拆分、审查、集成和发布。
- Backend Agent：后端接口、数据存储和 mock Agent 服务。
- Frontend Agent：Web 模拟咨询页面和浏览器交互。
- Knowledge Agent：Markdown 知识库、问题分类素材和提示词内容。
- Test Agent：测试计划、自动化测试和验收检查。
- Docs Agent：项目文档、路线图、安全说明和阶段总结。

## 任务流
1. Main Agent 明确阶段目标和禁止事项。
2. Main Agent 将任务拆给一个或多个子 Agent。
3. 子 Agent 在允许目录内完成小范围变更。
4. Main Agent 审查变更是否符合阶段边界。
5. Test Agent 或 Main Agent 执行必要检查。
6. Main Agent 汇总结果并决定是否进入下一阶段。

## 变更原则
- 小步提交。
- 文档与实际状态一致。
- 不提前实现未来阶段。
- 不写真实敏感信息。
- 不引入与 MVP 无关的复杂依赖。

## 第 0 阶段边界
第 0 阶段只允许初始化仓库、目录和治理文档。不得实现业务接口、聊天页面、真实微信接入或真实 LLM 接入。
