from backend.ticket_summary import generate_ticket_summary


REQUIRED_FIELDS = {
    "title",
    "category",
    "problem_description",
    "collected_info",
    "possible_causes",
    "suggested_steps",
    "status",
    "follow_up",
}


def assert_required_fields(summary: dict) -> None:
    assert REQUIRED_FIELDS.issubset(summary.keys())
    assert summary["status"] == "draft"


def test_empty_messages_returns_draft_summary() -> None:
    summary = generate_ticket_summary("demo-session", [])

    assert summary["session_id"] == "demo-session"
    assert summary["category"] == "other"
    assert summary["title"] == "待确认的问题标题"
    assert "需要客户补充问题描述" in summary["follow_up"]
    assert_required_fields(summary)


def test_database_connection_summary() -> None:
    summary = generate_ticket_summary(
        "demo-session",
        [
            {"role": "user", "content": "数据库连接超时"},
            {"role": "agent", "content": "请补充连接信息"},
            {"role": "user", "content": "GaussDB，端口 8000，telnet 不通"},
        ],
    )

    assert summary["category"] == "database_connection"
    assert summary["label"] == "数据库连接问题"
    assert "数据库类型：GaussDB" in summary["collected_info"]
    assert "端口：8000" in summary["collected_info"]
    assert "telnet 检查：不通" in summary["collected_info"]
    assert_required_fields(summary)


def test_permission_error_summary() -> None:
    summary = generate_ticket_summary(
        "demo-session",
        [{"role": "user", "content": "当前用户权限不足，执行操作 denied"}],
    )

    assert summary["category"] == "permission_error"
    assert summary["label"] == "权限问题"
    assert_required_fields(summary)


def test_sql_error_summary() -> None:
    summary = generate_ticket_summary(
        "demo-session",
        [{"role": "user", "content": "SQL 执行失败，提示 ORA ERROR 字段不存在"}],
    )

    assert summary["category"] == "sql_error"
    assert summary["label"] == "SQL 执行错误"
    assert_required_fields(summary)


def test_performance_issue_summary() -> None:
    summary = generate_ticket_summary(
        "demo-session",
        [{"role": "user", "content": "查询很慢，CPU 和内存占用很高"}],
    )

    assert summary["category"] == "performance_issue"
    assert summary["label"] == "性能问题"
    assert_required_fields(summary)


def test_service_unavailable_summary() -> None:
    summary = generate_ticket_summary(
        "demo-session",
        [{"role": "user", "content": "服务启动失败，端口未监听"}],
    )

    assert summary["category"] == "service_unavailable"
    assert summary["label"] == "服务不可用"
    assert_required_fields(summary)


def test_summary_prefers_latest_classifiable_user_issue() -> None:
    summary = generate_ticket_summary(
        "demo-session",
        [
            {"role": "user", "content": "数据库连接超时"},
            {"role": "agent", "content": "请补充数据库类型、版本、端口等"},
            {"role": "user", "content": "执行SQL提示权限不足"},
            {"role": "agent", "content": "请补充当前用户、执行SQL、对象名等"},
            {"role": "user", "content": "SQL执行报错 ORA-00942 表不存在"},
        ],
    )

    assert summary["title"] == "SQL 执行错误问题"
    assert summary["category"] == "sql_error"
    assert summary["label"] == "SQL 执行错误"
    assert "SQL 相关信息已提供" in summary["collected_info"]
    assert "ORA 错误码已提供" in summary["collected_info"]
    assert_required_fields(summary)


def test_latest_permission_issue_takes_priority_over_earlier_connection_issue() -> None:
    summary = generate_ticket_summary(
        "demo-session",
        [
            {"role": "user", "content": "数据库连接超时"},
            {"role": "agent", "content": "请补充数据库连接信息"},
            {"role": "user", "content": "执行 SQL 提示权限不足 denied"},
        ],
    )

    assert summary["title"] == "权限不足问题"
    assert summary["category"] == "permission_error"
    assert summary["label"] == "权限问题"
    assert_required_fields(summary)
