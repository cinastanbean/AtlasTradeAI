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
    assert "agent_run_count" in payload["data"]


def test_rule_catalog_endpoint() -> None:
    response = client.get("/api/rules/workflow")
    assert response.status_code == 200
    payload = response.json()
    assert any(item["rule_code"] == "R002" for item in payload["data"])
    assert any("subscribers" in item for item in payload["data"])


def test_integrations_endpoint() -> None:
    response = client.get("/api/integrations")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["data"]) == 3
    assert payload["data"][0]["mode"] == "mock-api"


def test_integration_snapshot_endpoint() -> None:
    response = client.get("/api/integrations/crm")
    assert response.status_code == 200
    payload = response.json()
    assert any(item["section"] == "customers" for item in payload["data"])


def test_demo_scenario_endpoint() -> None:
    response = client.get("/api/demo/scenarios")
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"][0]["code"]


def test_platform_page_endpoint() -> None:
    response = client.get("/platform")
    assert response.status_code == 200
    assert "订单驱动智能贸易操作系统" in response.text


def test_frontend_orders_page_endpoint() -> None:
    response = client.get("/ui/orders.html")
    assert response.status_code == 200
    assert "订单作战看板" in response.text


def test_agent_catalog_endpoint() -> None:
    response = client.get("/api/agents/catalog")
    assert response.status_code == 200
    payload = response.json()
    assert any(item["agent_key"] == "finance_agent" for item in payload["data"])


def test_order_progress_endpoint() -> None:
    response = client.get("/api/orders/ord_001/progress")
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["stages"]


def test_demo_scenario_creates_agent_runs() -> None:
    response = client.post("/api/demo/scenarios/doc_missing_ord_002/run")
    assert response.status_code == 200
    runs = client.get("/api/agent-runs").json()["data"]
    assert any(item["agent_name"] in {"Customs / Documentation Agent", "Follow-up Agent"} for item in runs)
