# API Reference

## GET `/health`

### 请求示例
```bash
curl http://127.0.0.1:8000/health
```

### 返回示例
```json
{
  "status": "ok",
  "service": "wechat-support-agent"
}
```

### 字段说明
- `status`：服务状态。
- `service`：服务名称。

## POST `/chat`

### 请求示例
```json
{
  "session_id": "demo-session",
  "message": "数据库连接超时"
}
```

### 返回示例
```json
{
  "session_id": "demo-session",
  "reply": "我判断这可能是数据库连接问题。请先补充数据库类型、版本、连接地址、端口、完整报错，以及 ping/telnet 检查结果。",
  "stage": "collecting_info",
  "classification": {
    "category": "database_connection",
    "label": "数据库连接问题",
    "confidence": 0.8,
    "reason": "命中关键词：连接、超时"
  },
  "knowledge": {
    "file": "knowledge/database_connection.md",
    "available": true
  },
  "next_questions": [
    "数据库类型和版本是什么？",
    "连接地址和端口是什么？",
    "完整报错信息是什么？",
    "ping 和 telnet 检查结果是什么？"
  ]
}
```

### 字段说明
- `session_id`：会话 ID。
- `reply`：Agent 当前回复。
- `stage`：当前处理阶段。
- `classification`：问题分类结果。
- `knowledge.file`：引用的知识库文件。
- `knowledge.available`：知识库是否可读取。
- `next_questions`：建议继续追问的问题。

## POST `/summary`

### 请求示例
```json
{
  "session_id": "demo-session",
  "messages": [
    {
      "role": "user",
      "content": "数据库连接超时"
    },
    {
      "role": "user",
      "content": "GaussDB，端口 8000，telnet 不通"
    }
  ]
}
```

### 返回示例
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

### 字段说明
- `session_id`：会话 ID。
- `title`：工单标题草稿。
- `category`：问题分类。
- `label`：分类中文名称。
- `problem_description`：问题现象描述。
- `collected_info`：已收集到的信息。
- `possible_causes`：可能原因。
- `suggested_steps`：建议排查步骤。
- `status`：摘要状态。
- `follow_up`：后续需要补充或确认的事项。
