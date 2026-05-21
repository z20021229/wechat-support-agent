from fastapi.testclient import TestClient

from backend.main import app
from backend.session_state import reset_sessions


client = TestClient(app)


def setup_function() -> None:
    reset_sessions()


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "wechat-support-agent",
    }


def test_chat_returns_mock_reply() -> None:
    response = client.post(
        "/chat",
        json={
            "session_id": "demo-session",
            "message": "数据库连接超时",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["session_id"] == "demo-session"
    assert data["reply"] == "我判断这可能是数据库连接问题。请先补充数据库类型、版本、连接地址、端口、完整报错，以及 ping/telnet 检查结果。"
    assert data["stage"] == "collecting_info"
    assert data["classification"] == {
        "category": "database_connection",
        "label": "数据库连接问题",
        "confidence": 0.8,
        "reason": "命中关键词：连接、超时",
    }
    assert data["knowledge"] == {
        "file": "knowledge/database_connection.md",
        "available": True,
    }
    assert "数据库类型和版本是什么？" in data["next_questions"]
    assert "content" not in data["knowledge"]
    assert data["session_state"] == {
        "collected_info": [],
        "missing_info": ["数据库类型", "数据库版本", "连接地址", "端口", "完整报错", "ping 结果", "telnet 结果"],
    }
    assert data["progress"] == {
        "collected_count": 0,
        "missing_count": 7,
        "completion_ratio": 0,
        "ready_for_guidance": False,
    }
    assert data["troubleshooting_steps"] == []


def test_chat_returns_dynamic_next_questions_from_session_state() -> None:
    client.post(
        "/chat",
        json={
            "session_id": "state-session",
            "message": "数据库连接超时",
        },
    )

    response = client.post(
        "/chat",
        json={
            "session_id": "state-session",
            "message": "GaussDB，端口 8000，telnet 不通",
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert data["session_state"]["collected_info"] == [
        "数据库类型：GaussDB",
        "端口：8000",
        "telnet 结果：不通",
    ]
    assert "端口" not in data["session_state"]["missing_info"]
    assert "telnet 结果" not in data["session_state"]["missing_info"]
    assert "端口是什么？" not in data["next_questions"]
    assert "telnet 检查结果是什么？" not in data["next_questions"]


def test_chat_returns_guidance_when_session_has_enough_info() -> None:
    client.post(
        "/chat",
        json={
            "session_id": "guidance-session",
            "message": "数据库连接超时",
        },
    )

    response = client.post(
        "/chat",
        json={
            "session_id": "guidance-session",
            "message": "端口 8000，telnet 不通",
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert data["stage"] == "guidance"
    assert data["progress"]["ready_for_guidance"] is True
    assert data["progress"]["collected_count"] == 2
    assert data["troubleshooting_steps"]
    assert "检查端口监听状态" in data["troubleshooting_steps"]
    assert "初步" not in data["troubleshooting_steps"]
    assert "端口：8000" in data["session_state"]["collected_info"]
    assert "telnet 结果：不通" in data["session_state"]["collected_info"]


def test_summary_returns_mock_ticket_summary() -> None:
    response = client.post(
        "/summary",
        json={
            "session_id": "demo-session",
            "messages": [
                {
                    "role": "user",
                    "content": "数据库连接超时",
                },
                {
                    "role": "agent",
                    "content": "请补充数据库类型、版本、连接地址、端口、完整报错，以及 ping/telnet 检查结果。",
                },
                {
                    "role": "user",
                    "content": "GaussDB，端口 8000，telnet 不通",
                },
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["session_id"] == "demo-session"
    assert data["title"] == "数据库连接超时问题"
    assert data["category"] == "database_connection"
    assert data["label"] == "数据库连接问题"
    assert data["status"] == "draft"
    assert "数据库类型：GaussDB" in data["collected_info"]
    assert "端口：8000" in data["collected_info"]
    assert "telnet 检查：不通" in data["collected_info"]
    assert "possible_causes" in data
    assert "suggested_steps" in data
    assert "follow_up" in data


def test_summary_uses_session_messages_when_request_messages_empty() -> None:
    client.post(
        "/chat",
        json={
            "session_id": "summary-session",
            "message": "数据库连接超时",
        },
    )
    client.post(
        "/chat",
        json={
            "session_id": "summary-session",
            "message": "GaussDB，端口 8000，telnet 不通",
        },
    )

    response = client.post(
        "/summary",
        json={
            "session_id": "summary-session",
            "messages": [],
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert data["category"] == "database_connection"
    assert "数据库类型：GaussDB" in data["collected_info"]
    assert "端口：8000" in data["collected_info"]
    assert "telnet 检查：不通" in data["collected_info"]


def test_session_reset_endpoint_is_available() -> None:
    response = client.post(
        "/session/reset",
        json={
            "session_id": "reset-session",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "session_id": "reset-session",
        "reset": True,
    }


def test_chat_after_reset_does_not_return_old_collected_info() -> None:
    client.post(
        "/chat",
        json={
            "session_id": "reset-session",
            "message": "数据库连接超时",
        },
    )
    client.post(
        "/chat",
        json={
            "session_id": "reset-session",
            "message": "GaussDB，端口 8000，telnet 不通",
        },
    )

    reset_response = client.post(
        "/session/reset",
        json={
            "session_id": "reset-session",
        },
    )
    response = client.post(
        "/chat",
        json={
            "session_id": "reset-session",
            "message": "数据库连接超时",
        },
    )
    data = response.json()

    assert reset_response.status_code == 200
    assert response.status_code == 200
    assert data["session_state"]["collected_info"] == []
    assert "数据库类型" in data["session_state"]["missing_info"]
    assert "端口" in data["session_state"]["missing_info"]
    assert "telnet 结果" in data["session_state"]["missing_info"]
    assert "GaussDB" not in data["reply"]
    assert "8000" not in data["reply"]
    assert "telnet 结果：不通" not in data["reply"]


def test_chat_sessions_do_not_share_collected_info() -> None:
    client.post(
        "/chat",
        json={
            "session_id": "session-a",
            "message": "数据库连接超时",
        },
    )
    client.post(
        "/chat",
        json={
            "session_id": "session-a",
            "message": "GaussDB，端口 8000，telnet 不通",
        },
    )

    response = client.post(
        "/chat",
        json={
            "session_id": "session-b",
            "message": "数据库连接超时",
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert data["session_state"]["collected_info"] == []
    assert "数据库类型" in data["session_state"]["missing_info"]
    assert "端口" in data["session_state"]["missing_info"]
    assert "telnet 结果" in data["session_state"]["missing_info"]
