from __future__ import annotations

import json
import os
from typing import Any
from urllib import error, request


class OpenAIEnhancer:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/responses")
        self.model = os.getenv("ATLAS_AGENT_MODEL", "gpt-5-mini")

    def is_enabled(self) -> bool:
        return bool(self.api_key)

    def enhance(self, prompt: str) -> dict[str, Any] | None:
        if not self.api_key:
            return None

        payload = {
            "model": self.model,
            "input": prompt,
            "text": {"format": {"type": "json_object"}},
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
        if "output_text" in payload and payload["output_text"]:
            return payload["output_text"]
        for item in payload.get("output", []):
            for content in item.get("content", []):
                text = content.get("text")
                if text:
                    return text
        return None
