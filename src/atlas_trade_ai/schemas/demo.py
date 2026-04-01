from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class DemoScenarioRead(BaseModel):
    code: str
    name: str
    description: str
    event: dict[str, Any]


class DemoScenarioRunResponse(BaseModel):
    scenario: dict[str, Any]
    result: dict[str, Any]
