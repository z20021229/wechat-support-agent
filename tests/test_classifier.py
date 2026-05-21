from backend.classifier import classify_issue


def test_classifies_database_connection_issue() -> None:
    result = classify_issue("数据库连接超时")

    assert result.category == "database_connection"
    assert result.label == "数据库连接问题"
    assert result.confidence == 0.8
    assert result.reason == "命中关键词：连接、超时"


def test_classifies_permission_issue() -> None:
    result = classify_issue("当前用户权限不足，执行操作 denied")

    assert result.category == "permission_error"
    assert result.label == "权限问题"


def test_classifies_sql_error() -> None:
    result = classify_issue("SQL 执行失败，提示字段不存在")

    assert result.category == "sql_error"
    assert result.label == "SQL 执行错误"


def test_classifies_performance_issue() -> None:
    result = classify_issue("查询很慢，CPU 和内存占用很高")

    assert result.category == "performance_issue"
    assert result.label == "性能问题"


def test_classifies_service_unavailable_issue() -> None:
    result = classify_issue("服务启动失败，端口未监听")

    assert result.category == "service_unavailable"
    assert result.label == "服务不可用"


def test_classifies_other_issue() -> None:
    result = classify_issue("界面显示异常，需要人工确认")

    assert result.category == "other"
    assert result.label == "其他问题"
    assert result.confidence == 0.3
    assert result.reason == "未命中已知关键词"
