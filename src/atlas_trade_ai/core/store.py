from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class InMemoryStore:
    customers: dict[str, dict] = field(default_factory=dict)
    orders: dict[str, dict] = field(default_factory=dict)
    tasks: dict[str, dict] = field(default_factory=dict)
    exceptions: dict[str, dict] = field(default_factory=dict)
    events: dict[str, dict] = field(default_factory=dict)
    notifications: list[dict] = field(default_factory=list)
    counters: dict[str, int] = field(
        default_factory=lambda: {
            "task": 0,
            "exception": 0,
            "event": 0,
            "notification": 0,
        }
    )

    def next_id(self, prefix: str) -> str:
        self.counters[prefix] += 1
        return f"{prefix}_{self.counters[prefix]:03d}"
