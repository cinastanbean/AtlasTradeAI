from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class OrderDashboardRead(BaseModel):
    order: dict[str, Any]
    customer: dict[str, Any]
    tasks: list[dict[str, Any]]
    exceptions: list[dict[str, Any]]
    events: list[dict[str, Any]]
    agent_runs: list[dict[str, Any]]
    orchestration: dict[str, Any] | None = None
