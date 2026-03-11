from dataclasses import dataclass
from typing import Any

import httpx

from app.core.config import settings


@dataclass(frozen=True)
class LLMGenerationResult:
    answer: str
    trace_step: str
    used_llm: bool


class LLMService:
    def generate_direct_answer(self, message: str) -> LLMGenerationResult:
        if not settings.openai_api_key or not settings.openai_model:
            return LLMGenerationResult(
                answer=f"这是 direct_answer 的 fallback 回答。任务：{message}",
                trace_step="llm_skipped: missing_openai_config",
                used_llm=False,
            )

        try:
            response = self._call_chat_completions(message)
            return LLMGenerationResult(
                answer=response,
                trace_step=f"llm_response_generated: {settings.openai_model}",
                used_llm=True,
            )
        except Exception as exc:
            return LLMGenerationResult(
                answer=f"这是 direct_answer 的 fallback 回答。任务：{message}",
                trace_step=f"llm_failed_fallback: {exc.__class__.__name__}",
                used_llm=False,
            )

    def _call_chat_completions(self, message: str) -> str:
        payload: dict[str, Any] = {
            "model": settings.openai_model,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are the direct-answer module for Agent Workspace. "
                        "Provide concise, structured answers and do not mention internal routing."
                    ),
                },
                {"role": "user", "content": message},
            ],
        }

        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }

        with httpx.Client(timeout=settings.llm_timeout_seconds) as client:
            response = client.post(
                f"{settings.openai_base_url.rstrip('/')}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        content = self._extract_message_content(data)
        if not content:
            raise ValueError("Empty chat completion content")
        return content

    @staticmethod
    def _extract_message_content(data: dict[str, Any]) -> str:
        choices = data.get("choices")
        if not isinstance(choices, list) or not choices:
            raise ValueError("Missing choices in LLM response")

        message = choices[0].get("message", {})
        content = message.get("content", "")
        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text = item.get("text", "")
                    if isinstance(text, str):
                        parts.append(text)
            return "".join(parts).strip()

        raise ValueError("Unsupported LLM content format")


llm_service = LLMService()
