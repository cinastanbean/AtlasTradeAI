from __future__ import annotations

from atlas_trade_ai.adapters.base import AdapterHealth
from atlas_trade_ai.core.config_loader import JsonConfigLoader


class DingTalkAdapter:
    def __init__(self, loader: JsonConfigLoader | None = None) -> None:
        self.loader = loader or JsonConfigLoader()
        self.data = self.loader.load("mock_integrations.json")["dingtalk"]

    def health(self) -> AdapterHealth:
        return AdapterHealth(
            name="钉钉",
            connected=True,
            mode="mock-api",
            description=f"消息通知与待办触达适配器，当前使用 Mock 数据，待办 {len(self.data['todos'])} 条。",
        )

    def list_todos(self) -> list[dict]:
        return self.data["todos"]

    def list_messages(self) -> list[dict]:
        return self.data["messages"]

    def list_approvals(self) -> list[dict]:
        return self.data["approvals"]
