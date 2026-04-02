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
    assert payload["data"]["orchestration"]["applied"] is True
    assert payload["data"]["orchestration"]["next_owner_agent"] == "supply_chain_agent"
    assert payload["data"]["generated_task_ids"]
    assert payload["data"]["generated_exception_ids"]


def test_workbench_summary_endpoint() -> None:
    response = client.get("/api/workbench/summary")
    assert response.status_code == 200
    payload = response.json()
    assert "order_count" in payload["data"]
    assert "agent_run_count" in payload["data"]
    assert "escalated_order_count" in payload["data"]


def test_workbench_escalations_endpoint() -> None:
    client.post("/api/demo/scenarios/doc_missing_ord_002/run")
    response = client.get("/api/workbench/escalations")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["data"], list)


def test_workbench_composite_risks_endpoint() -> None:
    client.post(
        "/api/events",
        json={
            "event_type": "logistics.delayed",
            "event_time": "2026-04-02T09:00:00+08:00",
            "source_system": "atlas_trade_ai",
            "biz_object_type": "order",
            "biz_object_id": "ord_002",
            "order_id": "ord_002",
            "customer_id": "cus_002",
            "priority": "P2",
            "payload": {"eta_delay_days": 3},
        },
    )
    client.post("/api/demo/scenarios/payment_overdue_ord_002/run")
    response = client.get("/api/workbench/composite-risks")
    assert response.status_code == 200
    payload = response.json()
    assert any(item["signal"] == "delivery_finance_compound_risk" for item in payload["data"])


def test_workbench_sla_overdue_endpoint() -> None:
    client.post("/api/demo/scenarios/doc_missing_ord_002/run")
    response = client.get("/api/workbench/sla-overdue?now_iso=2026-04-02T18:00:00+08:00")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["data"], list)
    assert any(item["order_id"] == "ord_002" for item in payload["data"])


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


def test_frontend_agents_page_endpoint() -> None:
    response = client.get("/ui/agents.html")
    assert response.status_code == 200
    assert "Agent 监控中台" in response.text


def test_frontend_tasks_page_endpoint() -> None:
    response = client.get("/ui/tasks.html")
    assert response.status_code == 200
    assert "负责人任务台" in response.text


def test_agent_catalog_endpoint() -> None:
    response = client.get("/api/agents/catalog")
    assert response.status_code == 200
    payload = response.json()
    assert any(item["agent_key"] == "finance_agent" for item in payload["data"])
    assert any(item["execution_mode"] == "hybrid" for item in payload["data"])
    assert any(item["agent_key"] == "knowledge_agent" for item in payload["data"])


def test_agent_monitor_endpoint() -> None:
    response = client.get("/api/agents/monitor")
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["agent_count"] >= 10
    assert isinstance(payload["data"]["agent_cards"], list)


def test_task_owner_view_endpoint() -> None:
    response = client.get("/api/tasks/owners")
    assert response.status_code == 200
    payload = response.json()
    assert "owners" in payload["data"]


def test_order_progress_endpoint() -> None:
    response = client.get("/api/orders/ord_001/progress")
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["stages"]
    assert "current_layer" in payload["data"]


def test_order_orchestration_endpoint() -> None:
    client.post("/api/demo/scenarios/payment_overdue_ord_002/run")
    response = client.get("/api/orders/ord_002/orchestration")
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["next_owner_agent"] == "finance_agent"
    assert payload["data"]["blocked"] is True
    assert payload["data"]["escalation"]["required"] is True


def test_demo_scenario_creates_agent_runs() -> None:
    response = client.post("/api/demo/scenarios/doc_missing_ord_002/run")
    assert response.status_code == 200
    runs = client.get("/api/agent-runs").json()["data"]
    assert any(item["agent_name"] in {"Customs / Documentation Agent", "Follow-up Agent"} for item in runs)


def test_sales_and_crm_scenario_creates_two_agent_runs() -> None:
    response = client.post("/api/demo/scenarios/quotation_accepted_ord_005/run")
    assert response.status_code == 200
    runs = client.get("/api/agent-runs").json()["data"]
    names = {item["agent_name"] for item in runs}
    assert "Sales Agent" in names
    assert "CRM Agent" in names


def test_document_intelligence_scenario_creates_agent_run() -> None:
    response = client.post("/api/demo/scenarios/customs_rejected_ord_002/run")
    assert response.status_code == 200
    runs = client.get("/api/agent-runs").json()["data"]
    assert any(item["agent_name"] == "Document Intelligence Agent" for item in runs)


def test_operations_and_knowledge_scenario_creates_agent_runs() -> None:
    response = client.post("/api/demo/scenarios/payment_completed_ord_004/run")
    assert response.status_code == 200
    runs = client.get("/api/agent-runs").json()["data"]
    names = {item["agent_name"] for item in runs}
    assert "Operations Analyst Agent" in names
    assert "Knowledge Agent" in names


def test_generic_agent_run_endpoint() -> None:
    response = client.post(
        "/api/agents/finance_agent/run",
        json={
            "trigger_event": {
                "event_id": "evt_fin_001",
                "event_type": "payment.overdue",
                "event_time": "2026-04-01T12:00:00+08:00",
                "source_system": "erp",
                "biz_object_type": "order",
                "biz_object_id": "ord_004",
            },
            "order_context": {
                "order_id": "ord_004",
                "order_no": "SO-2026-0004",
                "current_status": "待回款",
                "sub_status": "客户已签收",
                "risk_level": "high",
                "planned_delivery_date": "2026-03-20",
                "payment_status": "逾期",
            },
            "customer_context": {
                "customer_id": "cus_004",
                "customer_name": "华南电商客户D",
                "customer_level": "成长客户",
                "business_type": "内销",
                "owner_id": "user_sales_01",
            },
            "fulfillment_context": {
                "milestones": [],
                "latest_logistics_status": "delivered",
                "document_status": "not_required",
                "customs_status": None,
                "exceptions": [],
            },
            "payment_context": {
                "receivable_amount": 56000.0,
                "received_amount": 0.0,
                "due_date": "2026-03-28",
                "overdue_days": 4,
            },
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["risk_assessment"]["risk_type"] == "finance_risk"
    assert payload["data"]["engine"]["mode"] in {"rules", "hybrid"}


def test_orchestrator_repeated_event_escalates() -> None:
    client.post("/api/demo/scenarios/doc_missing_ord_002/run")
    response = client.post("/api/demo/scenarios/doc_missing_ord_002/run")
    assert response.status_code == 200
    orchestration = response.json()["data"]["result"]["orchestration"]
    assert orchestration["escalation"]["required"] is True
    assert orchestration["escalation"]["level"] in {"high", "critical"}
    assert orchestration["escalation"]["resolved_targets"]
    tasks = client.get("/api/tasks").json()["data"]["items"]
    assert any(item["task_title"].startswith("处理中枢升级") for item in tasks)


def test_orchestrator_blocks_illegal_transition() -> None:
    response = client.post(
        "/api/events",
        json={
            "event_type": "payment.overdue",
            "event_time": "2026-04-02T10:00:00+08:00",
            "source_system": "kingdee_k3cloud",
            "biz_object_type": "order",
            "biz_object_id": "ord_001",
            "order_id": "ord_001",
            "customer_id": "cus_001",
            "priority": "P1",
            "payload": {
                "receivable_amount": 128000.0,
                "received_amount": 0.0,
                "due_date": "2026-03-20",
                "overdue_days": 10
            },
        },
    )
    assert response.status_code == 200
    orchestration = response.json()["data"]["orchestration"]
    assert orchestration["transition_allowed"] is False
    assert orchestration["status_after"] == orchestration["status_before"]
    assert orchestration["escalation"]["required"] is True


def test_task_status_update_endpoint() -> None:
    tasks = client.get("/api/tasks").json()["data"]["items"]
    task_id = tasks[0]["task_id"]
    response = client.post(
        f"/api/tasks/{task_id}/status",
        json={"task_status": "已完成", "operator": "tester"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["task_status"] == "已完成"
