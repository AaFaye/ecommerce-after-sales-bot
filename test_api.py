import pytest
from fastapi.testclient import TestClient

from db import TicketStatus
import main as app_main


@pytest.fixture
def client():
    """依赖 conftest 的 _isolate_db：每次返回全新 TestClient，数据库为内存库。"""
    return TestClient(app_main.app)


def test_chat_normal_reply(client):
    resp = client.post("/api/chat", json={"user_id": "u1", "message": "你好"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticket_id"] is None
    assert "您好" in data["reply"]


def test_chat_create_ticket(client):
    resp = client.post("/api/chat", json={"user_id": "u2", "message": "我买的衣服要退款"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticket_id"] == 1
    assert "工单" in data["reply"]


def test_list_tickets(client):
    client.post("/api/chat", json={"user_id": "u3", "message": "退货"})
    client.post("/api/chat", json={"user_id": "u3", "message": "换货"})
    resp = client.get("/api/tickets?user_id=u3")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 2
    assert items[0]["status"] == TicketStatus.pending


def test_update_ticket_status(client):
    created = client.post("/api/chat", json={"user_id": "u4", "message": "漏发了"})
    ticket_id = created.json()["ticket_id"]
    resp = client.patch(f"/api/tickets/{ticket_id}", json={"status": "resolved"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "resolved"


def test_get_missing_ticket(client):
    assert client.get("/api/tickets/999").status_code == 404
