# Demo Chat: Database Connection

## 客户输入
```text
数据库连接超时
```

## Agent 回复
```text
我判断这可能是数据库连接问题。请先补充数据库类型、版本、连接地址、端口、完整报错，以及 ping/telnet 检查结果。
```

## 预期分类
```json
{
  "category": "database_connection",
  "label": "数据库连接问题",
  "confidence": 0.8,
  "reason": "命中关键词：连接、超时"
}
```

## 后续追问
- 数据库类型和版本是什么？
- 连接地址和端口是什么？
- 完整报错信息是什么？
- ping 和 telnet 检查结果是什么？
