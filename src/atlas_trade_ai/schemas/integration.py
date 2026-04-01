from __future__ import annotations

from pydantic import BaseModel


class AdapterHealthRead(BaseModel):
    name: str
    connected: bool
    mode: str
    description: str
