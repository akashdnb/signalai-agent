import json
from typing import Any

import httpx

from signalai_agent.config import settings


SYSTEM_PROMPT = """
You are the SignalAI planning layer. Produce a JSON object with a `steps` array.
Each step must contain: capability, input, reason.
Only use these read-safe capabilities:
- company.search
- company.get
- lead.list
- conversation.list
- automation.list
Never invent capabilities. Never produce destructive or outbound actions.
Keep the plan to the configured maximum number of steps.
""".strip()


class LLMPlanner:
    async def plan(self, instruction: str) -> dict[str, Any]:
        if not settings.llm_base_url or not settings.llm_api_key or not settings.llm_model:
            raise RuntimeError("llm_not_configured")

        headers = {
            "Authorization": f"Bearer {settings.llm_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.llm_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": instruction},
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        }
        async with httpx.AsyncClient(timeout=httpx.Timeout(settings.llm_timeout_seconds)) as client:
            response = await client.post(
                f"{str(settings.llm_base_url).rstrip('/')}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            body = response.json()

        content = body["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise TypeError("invalid_llm_plan")
        return parsed
