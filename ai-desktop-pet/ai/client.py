"""OpenAI 兼容 API 客户端"""
import requests

from config import AI_REQUEST_TIMEOUT


class AIClient:
    """调用 OpenAI 兼容的 /chat/completions 接口。"""

    def __init__(self, base_url: str = "", api_key: str = "", model: str = ""):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model or "deepseek-chat"

    def is_configured(self) -> bool:
        return bool(self.base_url)

    def chat(self, messages: list[dict], temperature: float = 0.8) -> str:
        if not self.is_configured():
            raise RuntimeError("AI 未配置")
        url = self.base_url.rstrip("/") + "/chat/completions"
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=AI_REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
