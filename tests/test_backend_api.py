from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


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
    assert data["reply"] == (
        "我判断这可能是数据库连接问题。请先补充数据库类型、版本、连接地址、端口、完整报错，以及 ping/telnet 检查结果。"
    )
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


def test_summary_returns_mock_ticket_summary() -> None:
    response = client.post(
        "/summary",
        json={
            "session_id": "demo-session",
            "messages": [],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "title": "待确认的问题标题",
        "summary": "当前为 mock 工单摘要，后续阶段会根据聊天记录生成完整内容。",
        "status": "draft",
    }
