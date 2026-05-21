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
    assert response.json() == {
        "session_id": "demo-session",
        "reply": "请补充数据库类型、版本、连接地址、端口、完整报错，以及 ping/telnet 结果。",
        "stage": "collecting_info",
        "classification": {
            "category": "database_connection",
            "label": "数据库连接问题",
            "confidence": 0.8,
            "reason": "命中关键词：连接、超时",
        },
    }


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
