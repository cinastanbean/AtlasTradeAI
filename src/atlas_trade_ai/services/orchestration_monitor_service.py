from __future__ import annotations

from atlas_trade_ai.core.store import SQLiteStore


class OrchestrationMonitorService:
    def __init__(self, store: SQLiteStore) -> None:
        self.store = store

    def list_escalated_orders(self) -> list[dict]:
        orders = self.store.list_orders()
        results: list[dict] = []
        for order in orders:
            orchestration = order.get("last_orchestration")
            if not orchestration:
                continue
            escalation = orchestration.get("escalation") or {}
            if not escalation.get("required"):
                continue
            results.append(
                {
                    "order_id": order["order_id"],
                    "order_no": order["order_no"],
                    "customer_name": order.get("customer_name"),
                    "current_status": order.get("current_status"),
                    "sub_status": order.get("sub_status"),
                    "blocked": orchestration.get("blocked", False),
                    "sla_hours": orchestration.get("sla_hours"),
                    "escalation_level": escalation.get("level"),
                    "escalation_reasons": escalation.get("reasons", []),
                    "escalation_targets": escalation.get("resolved_targets", []),
                    "composite_signals": escalation.get("composite_signals", []),
                    "next_owner_agent": orchestration.get("next_owner_agent"),
                }
            )
        results.sort(
            key=lambda item: (
                {"critical": 0, "high": 1, "medium": 2, "low": 3, "none": 4}.get(
                    item["escalation_level"], 9
                ),
                item["order_no"],
            )
        )
        return results

    def get_composite_risk_stats(self) -> list[dict]:
        stats: dict[str, int] = {}
        for order in self.store.list_orders():
            orchestration = order.get("last_orchestration") or {}
            escalation = orchestration.get("escalation") or {}
            for signal in escalation.get("composite_signals", []):
                stats[signal] = stats.get(signal, 0) + 1
        return [
            {"signal": signal, "count": count}
            for signal, count in sorted(stats.items(), key=lambda item: item[1], reverse=True)
        ]
