from __future__ import annotations

import json
import os
from typing import Any
from urllib import error, request


def create_enhancer():
    """根据配置创建对应的大模型增强器。"""
    provider = os.getenv("ATLAS_LLM_PROVIDER", "openai").lower()
    if provider == "zhipu":
        from atlas_trade_ai.llm_zhipu import ZhipuEnhancer

        return ZhipuEnhancer()
    else:
        return OpenAIEnhancer()


def get_provider_name(enhancer: object) -> str:
    """从增强器对象获取提供商名称。
    
    优先使用类的 provider 属性，如果不存在则从类名推断。
    
    Args:
        enhancer: 增强器实例
        
    Returns:
        小写的提供商名称，如 'openai', 'zhipu'
    """
    # 优先使用类属性
    if hasattr(enhancer.__class__, 'provider'):
        return enhancer.__class__.provider.lower()
    
    # 回退到从类名推断（保持向后兼容）
    class_name = enhancer.__class__.__name__
    if class_name.endswith('Enhancer'):
        return class_name[:-8].lower()
    return class_name.lower()


class OpenAIEnhancer:
    provider = "openai"  # 类属性，明确声明提供商名称
    
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
