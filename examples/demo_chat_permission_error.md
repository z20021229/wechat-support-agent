# Demo Chat: Permission Error

## 客户输入
```text
执行 SQL 提示权限不足
```

## Agent 回复
```text
我判断这可能是权限问题。请先补充当前用户、执行的操作、完整报错，以及相关对象权限信息。
```

## 需要补充的信息
- 当前用户。
- 执行 SQL。
- 对象名。
- 完整报错。
- 授权情况。

## 预期分类
```json
{
  "category": "permission_error",
  "label": "权限问题",
  "confidence": 0.8
}
```
