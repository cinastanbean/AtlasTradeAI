from __future__ import annotations

from pydantic import BaseModel


class AdapterHealthRead(BaseModel):
    name: str
    connected: bool
    mode: str
    description: str


class IntegrationSnapshotRead(BaseModel):
    section: str
    items: list[dict]
