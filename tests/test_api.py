from fastapi.testclient import TestClient

from atlas_trade_ai.app import app


client = TestClient(app)


def test_architecture_overview_endpoint() -> None:
    response = client.get("/api/overview/architecture")
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["hub"]["name"] == "订单中枢"


def test_list_orders_endpoint() -> None:
    response = client.get("/api/orders")
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["items"][0]["order_no"] == "SO-2026-0001"


def test_event_pipeline_generates_task_and_exception() -> None:
    response = client.post(
        "/api/events",
        json={
            "event_type": "production.milestone_delayed",
            "event_time": "2026-04-01T10:30:00+08:00",
            "source_system": "kingdee_k3cloud",
            "biz_object_type": "order",
            "biz_object_id": "ord_001",
            "order_id": "ord_001",
            "customer_id": "cus_001",
            "priority": "P1",
            "payload": {
                "milestone_type": "生产完成",
                "delay_days": 2,
                "receivable_amount": 128000.0,
                "received_amount": 0.0,
                "due_date": "2026-04-30",
                "overdue_days": 0,
            },
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["accepted"] is True
    assert payload["data"]["matched_rule"] == "R002"
    assert payload["data"]["generated_task_ids"]
    assert payload["data"]["generated_exception_ids"]


def test_workbench_summary_endpoint() -> None:
    response = client.get("/api/workbench/summary")
    assert response.status_code == 200
    payload = response.json()
    assert "order_count" in payload["data"]


def test_rule_catalog_endpoint() -> None:
    response = client.get("/api/rules/workflow")
    assert response.status_code == 200
    payload = response.json()
    assert any(item["rule_code"] == "R002" for item in payload["data"])


def test_integrations_endpoint() -> None:
    response = client.get("/api/integrations")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["data"]) == 3
