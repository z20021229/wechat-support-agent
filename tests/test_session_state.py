from backend.session_state import (
    get_session_progress,
    get_or_create_session,
    reset_session,
    reset_sessions,
    update_session_with_message,
)


def setup_function() -> None:
    reset_sessions()


def test_new_session_can_be_created() -> None:
    session = get_or_create_session("demo-session")

    assert session["session_id"] == "demo-session"
    assert session["category"] == "other"
    assert session["messages"] == []
    assert session["collected_info"] == []


def test_new_session_progress_starts_at_zero() -> None:
    session = get_or_create_session("demo-session")

    assert get_session_progress(session) == {
        "collected_count": 0,
        "missing_count": 5,
        "completion_ratio": 0,
        "ready_for_guidance": False,
    }


def test_user_message_is_written_to_messages() -> None:
    session = update_session_with_message("demo-session", "user", "数据库连接超时")

    assert session["messages"] == [{"role": "user", "content": "数据库连接超时"}]


def test_latest_user_message_updates() -> None:
    update_session_with_message("demo-session", "user", "数据库连接超时")
    session = update_session_with_message("demo-session", "user", "GaussDB，端口 8000")

    assert session["latest_user_message"] == "GaussDB，端口 8000"


def test_database_connection_extracts_port() -> None:
    update_session_with_message("demo-session", "user", "数据库连接超时")
    session = update_session_with_message("demo-session", "user", "端口 8000")

    assert "端口：8000" in session["collected_info"]


def test_progress_increases_after_collecting_info() -> None:
    update_session_with_message("demo-session", "user", "数据库连接超时")
    session = update_session_with_message("demo-session", "user", "端口 8000")
    progress = get_session_progress(session)

    assert progress["collected_count"] == 1
    assert progress["completion_ratio"] > 0
    assert progress["ready_for_guidance"] is False


def test_database_connection_extracts_telnet_failure() -> None:
    update_session_with_message("demo-session", "user", "数据库连接超时")
    session = update_session_with_message("demo-session", "user", "telnet 不通")

    assert "telnet 结果：不通" in session["collected_info"]


def test_collected_info_is_removed_from_missing_info() -> None:
    update_session_with_message("demo-session", "user", "数据库连接超时")
    session = update_session_with_message("demo-session", "user", "GaussDB，端口 8000，telnet 不通")

    assert "端口" not in session["missing_info"]
    assert "telnet 结果" not in session["missing_info"]
    assert "数据库类型" not in session["missing_info"]


def test_database_connection_ready_for_guidance_with_port_and_telnet() -> None:
    update_session_with_message("demo-session", "user", "数据库连接超时")
    session = update_session_with_message("demo-session", "user", "端口 8000，telnet 不通")
    progress = get_session_progress(session)

    assert progress["ready_for_guidance"] is True
    assert progress["collected_count"] == 2
    assert progress["missing_count"] == 5


def test_sessions_are_isolated_by_session_id() -> None:
    first = update_session_with_message("session-a", "user", "数据库连接超时 端口 8000")
    second = update_session_with_message("session-b", "user", "权限不足 denied")

    assert first["session_id"] == "session-a"
    assert second["session_id"] == "session-b"
    assert first["category"] == "database_connection"
    assert second["category"] == "permission_error"
    assert "端口：8000" in first["collected_info"]
    assert "端口：8000" not in second["collected_info"]


def test_session_b_does_not_inherit_database_details_from_session_a() -> None:
    update_session_with_message("session-a", "user", "数据库连接超时")
    update_session_with_message("session-a", "user", "GaussDB，端口 8000，telnet 不通")

    session_b = update_session_with_message("session-b", "user", "数据库连接超时")

    assert session_b["collected_info"] == []
    assert "数据库类型" in session_b["missing_info"]
    assert "端口" in session_b["missing_info"]
    assert "telnet 结果" in session_b["missing_info"]


def test_reset_session_clears_collected_info() -> None:
    update_session_with_message("demo-session", "user", "数据库连接超时")
    update_session_with_message("demo-session", "user", "GaussDB，端口 8000，telnet 不通")

    reset_session("demo-session")
    session = get_or_create_session("demo-session")

    assert session["collected_info"] == []
    assert session["messages"] == []
    assert session["latest_user_message"] == ""


def test_new_database_connection_session_starts_with_missing_info_only() -> None:
    session = update_session_with_message("fresh-session", "user", "数据库连接超时")

    assert session["collected_info"] == []
    assert "数据库类型" in session["missing_info"]
    assert "端口" in session["missing_info"]
    assert "telnet 结果" in session["missing_info"]
    assert "数据库类型：GaussDB" not in session["collected_info"]
    assert "端口：8000" not in session["collected_info"]
    assert "telnet 结果：不通" not in session["collected_info"]
