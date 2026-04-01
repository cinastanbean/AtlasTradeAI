from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AdapterHealth:
    name: str
    connected: bool
    mode: str
    description: str
