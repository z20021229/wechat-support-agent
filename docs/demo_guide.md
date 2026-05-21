# Demo Guide

## 启动后端
```powershell
cd D:\codex-projects\wechat-support-agent
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

后端默认地址：
```text
http://127.0.0.1:8000
```

## 打开前端页面
用浏览器打开：
```text
D:\codex-projects\wechat-support-agent\frontend\index.html
```

## 输入测试问题
推荐输入：
```text
数据库连接超时
```

页面会展示客户消息，并调用 `POST /chat` 返回 Agent 回复、分类、知识库引用和下一步追问。

## 生成工单摘要
点击“生成工单摘要”按钮。页面会调用 `POST /summary`，根据当前聊天记录生成结构化工单摘要草稿。

## 推荐演示案例
### 数据库连接问题
客户输入：
```text
数据库连接超时
```

可继续补充：
```text
GaussDB，端口 8000，telnet 不通
```

预期效果：
- 分类为数据库连接问题。
- Agent 追问数据库类型、版本、连接地址、端口、完整报错和 ping/telnet 结果。
- 工单摘要提取数据库类型、端口和 telnet 检查结果。

### 权限问题
客户输入：
```text
执行 SQL 提示权限不足
```

预期效果：
- 分类为权限问题。
- Agent 追问当前用户、执行 SQL、对象名、完整报错和授权情况。

### 空摘要
在没有聊天记录时调用 `/summary`，预期返回 draft 摘要，并提示需要客户补充问题描述。
