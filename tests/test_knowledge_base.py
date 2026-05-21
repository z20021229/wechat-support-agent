from backend.knowledge_base import load_knowledge


def test_loads_database_connection_knowledge() -> None:
    knowledge = load_knowledge("database_connection")

    assert knowledge["category"] == "database_connection"
    assert knowledge["file"] == "knowledge/database_connection.md"
    assert knowledge["available"] is True
    assert "数据库连接问题" in knowledge["content"]


def test_loads_permission_error_knowledge() -> None:
    knowledge = load_knowledge("permission_error")

    assert knowledge["category"] == "permission_error"
    assert knowledge["file"] == "knowledge/permission_error.md"
    assert knowledge["available"] is True
    assert "权限问题" in knowledge["content"]


def test_loads_sql_error_knowledge() -> None:
    knowledge = load_knowledge("sql_error")

    assert knowledge["category"] == "sql_error"
    assert knowledge["file"] == "knowledge/sql_error.md"
    assert knowledge["available"] is True
    assert "SQL 执行错误" in knowledge["content"]


def test_loads_performance_issue_knowledge() -> None:
    knowledge = load_knowledge("performance_issue")

    assert knowledge["category"] == "performance_issue"
    assert knowledge["file"] == "knowledge/performance_issue.md"
    assert knowledge["available"] is True
    assert "性能问题" in knowledge["content"]


def test_loads_service_unavailable_knowledge() -> None:
    knowledge = load_knowledge("service_unavailable")

    assert knowledge["category"] == "service_unavailable"
    assert knowledge["file"] == "knowledge/service_unavailable.md"
    assert knowledge["available"] is True
    assert "服务不可用" in knowledge["content"]


def test_loads_other_knowledge() -> None:
    knowledge = load_knowledge("other")

    assert knowledge["category"] == "other"
    assert knowledge["file"] == "knowledge/other_issue.md"
    assert knowledge["available"] is True
    assert "其他问题" in knowledge["content"]


def test_unknown_category_falls_back_to_other_knowledge() -> None:
    knowledge = load_knowledge("unknown")

    assert knowledge["category"] == "other"
    assert knowledge["file"] == "knowledge/other_issue.md"
    assert knowledge["available"] is True
