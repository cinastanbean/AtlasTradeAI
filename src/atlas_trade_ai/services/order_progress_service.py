from __future__ import annotations

from atlas_trade_ai.core.store import SQLiteStore


class OrderProgressService:
    def __init__(self, store: SQLiteStore) -> None:
        self.store = store

    def get_progress(self, order_id: str) -> dict:
        order = self.store.get_order(order_id)
        current_status = order["current_status"]
        current_layer = order.get("current_layer")
        next_owner_agent = order.get("next_owner_agent")
        blocked = order.get("blocked", False)
        status_order = [
            "待确认",
            "已确认",
            "执行中",
            "待发货",
            "已发货",
            "运输 / 交付中",
            "待回款",
            "已完成",
        ]
        stage_labels = [
            ("客户经营层", "待确认"),
            ("订单中枢层", "已确认"),
            ("履约推进层", "执行中"),
            ("交付与合规层", "待发货"),
            ("交付与合规层", "已发货"),
            ("交付与合规层", "运输 / 交付中"),
            ("资金结算层", "待回款"),
            ("售后服务层", "已完成"),
        ]
        current_index = status_order.index(current_status) if current_status in status_order else 0
        if current_layer is None and current_index < len(stage_labels):
            current_layer = stage_labels[current_index][0]
        stages = []
        for index, (layer, status) in enumerate(stage_labels):
            state = "pending"
            if index < current_index:
                state = "completed"
            elif index == current_index:
                state = "current"
            stages.append(
                {
                    "layer": layer,
                    "status": status,
                    "state": state,
                }
            )
        return {
            "order_id": order_id,
            "order_no": order["order_no"],
            "current_status": current_status,
            "current_layer": current_layer,
            "next_owner_agent": next_owner_agent,
            "blocked": blocked,
            "stages": stages,
        }
