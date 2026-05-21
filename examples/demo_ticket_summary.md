# Demo Ticket Summary

## 输入聊天记录
```json
{
  "session_id": "demo-session",
  "messages": [
    {
      "role": "user",
      "content": "数据库连接超时"
    },
    {
      "role": "agent",
      "content": "请补充数据库类型、版本、连接地址、端口、完整报错，以及 ping/telnet 检查结果。"
    },
    {
      "role": "user",
      "content": "GaussDB，端口 8000，telnet 不通"
    }
  ]
}
```

## 结构化工单摘要
```json
{
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
