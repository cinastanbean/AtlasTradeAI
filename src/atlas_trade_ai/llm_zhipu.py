from __future__ import annotations

import json
import os
from typing import Any
from urllib import error, request


class ZhipuEnhancer:
    """智谱 AI 大模型增强器，支持 GLM-4 系列模型。"""

    def __init__(self) -> None:
        self.api_key = os.getenv("ZHIPU_API_KEY")
        self.base_url = os.getenv(
            "ZHIPU_BASE_URL",
            "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        )
        self.model = os.getenv("ATLAS_AGENT_MODEL", "glm-4-air")

    def is_enabled(self) -> bool:
        return bool(self.api_key)

    def enhance(self, prompt: str) -> dict[str, Any] | None:
        if not self.api_key:
            return None

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0.7,
            "top_p": 0.9,
        }
        req = request.Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except (TimeoutError, error.URLError, error.HTTPError, json.JSONDecodeError):
            return None

        output_text = self._extract_text(data)
        if not output_text:
            return None
        try:
            return json.loads(output_text)
        except json.JSONDecodeError:
            return None

    def _extract_text(self, payload: dict[str, Any]) -> str | None:
        choices = payload.get("choices", [])
        if not choices:
            return None
        return choices[0].get("message", {}).get("content")
