from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time
import urllib.parse
from urllib import error as urllib_error
from urllib import request

from atlas_trade_ai.adapters.base import AdapterHealth
from atlas_trade_ai.core.config_loader import JsonConfigLoader


class DingTalkAdapter:
    def __init__(self, loader: JsonConfigLoader | None = None) -> None:
        self.loader = loader or JsonConfigLoader()
        self.data = self.loader.load("mock_integrations.json")["dingtalk"]
        self.mode = os.getenv("DINGTALK_MODE", "mock")
        self.webhook_url = os.getenv("DINGTALK_WEBHOOK_URL")
        self.webhook_secret = os.getenv("DINGTALK_WEBHOOK_SECRET")
        self.client_id = os.getenv("DINGTALK_CLIENT_ID")
        self.client_secret = os.getenv("DINGTALK_CLIENT_SECRET")
        self.access_token_url = os.getenv(
            "DINGTALK_ACCESS_TOKEN_URL",
            "https://api.dingtalk.com/v1.0/oauth2/accessToken",
        )
        self.todo_create_url = os.getenv("DINGTALK_TODO_CREATE_URL")

    def health(self) -> AdapterHealth:
        if self.mode == "webhook" and self.webhook_url:
            return AdapterHealth(
                name="钉钉",
                connected=True,
                mode="webhook",
                description="消息通知通过真实钉钉机器人 Webhook 发送，待办仍可回退为 Mock。",
            )
        if self.mode == "openapi" and self.client_id and self.client_secret:
            return AdapterHealth(
                name="钉钉",
                connected=True,
                mode="openapi",
                description="消息通知/待办可通过钉钉开放平台接口发送，需配置真实企业应用凭证。",
            )
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

    def send_message(self, payload: dict) -> dict:
        if self.mode == "webhook" and self.webhook_url:
            return self._send_webhook_message(payload)
        if self.mode == "openapi" and self.client_id and self.client_secret and self.webhook_url:
            return self._send_webhook_message(payload)
        return {
            "success": True,
            "mode": "mock-api",
            "response": {"mock": True},
        }

    def create_todo(self, payload: dict) -> dict:
        if self.mode == "openapi" and self.client_id and self.client_secret and self.todo_create_url:
            return self._create_real_todo(payload)
        return {
            "success": True,
            "mode": "mock-api",
            "todo_id": f"mock_todo_{int(time.time() * 1000)}",
        }

    def _send_webhook_message(self, payload: dict) -> dict:
        url = self._signed_webhook_url()
        body = {
            "msgtype": "markdown",
            "markdown": {
                "title": payload.get("template_code", "AtlasTradeAI 通知"),
                "text": self._build_markdown(payload),
            },
        }
        req = request.Request(
            url,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=15) as resp:
                content = json.loads(resp.read().decode("utf-8"))
            return {"success": True, "mode": self.mode, "response": content}
        except urllib_error.HTTPError as e:
            return {
                "success": False,
                "error": f"HTTP 错误：{e.code} - {e.reason}",
                "mode": self.mode,
                "http_status": e.code,
            }
        except urllib_error.URLError as e:
            return {
                "success": False,
                "error": f"网络错误：{e.reason}",
                "mode": self.mode,
            }
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"JSON 解析错误：{str(e)}",
                "mode": self.mode,
            }
        except TimeoutError as e:
            return {
                "success": False,
                "error": f"请求超时：{str(e)}",
                "mode": self.mode,
            }
        except Exception as e:
            return {"success": False, "error": f"未知错误：{str(e)}", "mode": self.mode}

    def _create_real_todo(self, payload: dict) -> dict:
        try:
            access_token = self._get_access_token()
        except RuntimeError as e:
            return {"success": False, "error": f"获取访问令牌失败：{str(e)}", "mode": self.mode}
        req = request.Request(
            self.todo_create_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-acs-dingtalk-access-token": access_token,
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=15) as resp:
                content = json.loads(resp.read().decode("utf-8"))
            return {"success": True, "mode": self.mode, "todo_id": content.get("id"), "response": content}
        except urllib_error.HTTPError as e:
            return {
                "success": False,
                "error": f"HTTP 错误：{e.code} - {e.reason}",
                "mode": self.mode,
                "http_status": e.code,
            }
        except urllib_error.URLError as e:
            return {
                "success": False,
                "error": f"网络错误：{e.reason}",
                "mode": self.mode,
            }
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"JSON 解析错误：{str(e)}",
                "mode": self.mode,
            }
        except TimeoutError as e:
            return {
                "success": False,
                "error": f"请求超时：{str(e)}",
                "mode": self.mode,
            }
        except Exception as e:
            return {"success": False, "error": f"未知错误：{str(e)}", "mode": self.mode}

    def _get_access_token(self) -> str:
        body = {"appKey": self.client_id, "appSecret": self.client_secret}
        req = request.Request(
            self.access_token_url,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=15) as resp:
                content = json.loads(resp.read().decode("utf-8"))
            return content["accessToken"]
        except urllib_error.HTTPError as e:
            raise RuntimeError(f"获取钉钉访问令牌失败：HTTP {e.code} - {e.reason}") from e
        except urllib_error.URLError as e:
            raise RuntimeError(f"获取钉钉访问令牌失败：网络错误 - {e.reason}") from e
        except json.JSONDecodeError as e:
            raise RuntimeError(f"获取钉钉访问令牌失败：JSON 解析错误 - {str(e)}") from e
        except TimeoutError as e:
            raise RuntimeError(f"获取钉钉访问令牌失败：请求超时 - {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"获取钉钉访问令牌失败：未知错误 - {str(e)}") from e

    def _signed_webhook_url(self) -> str:
        if not self.webhook_secret:
            return self.webhook_url
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.webhook_secret.encode("utf-8")
        string_to_sign = f"{timestamp}\n{self.webhook_secret}".encode("utf-8")
        sign = urllib.parse.quote_plus(
            base64.b64encode(hmac.new(secret_enc, string_to_sign, digestmod=hashlib.sha256).digest())
        )
        separator = "&" if "?" in self.webhook_url else "?"
        return f"{self.webhook_url}{separator}timestamp={timestamp}&sign={sign}"

    def _build_markdown(self, payload: dict) -> str:
        data = payload.get("payload", {})
        lines = [
            f"### {payload.get('template_code', 'AtlasTradeAI 通知')}",
            "",
            f"- 订单号: {data.get('order_no', '-')}",
            f"- 说明: {data.get('message', '-')}",
        ]
        if "escalation_level" in data:
            lines.append(f"- 升级级别: {data.get('escalation_level')}")
        return "\n".join(lines)
