from signalai_agent.config import settings
from signalai_agent.llm import LLMPlanner
from signalai_agent.models import AgentPlan, AgentRequest, PlanStep


ALLOWED_CAPABILITIES = {
    "company.search",
    "company.get",
    "lead.list",
    "conversation.list",
    "automation.list",
}


class CapabilityPlanner:
    """Plan only through an explicit allowlist of read-safe capabilities."""

    def __init__(self) -> None:
        self._llm = LLMPlanner()

    async def plan(self, request: AgentRequest) -> AgentPlan:
        if settings.llm_base_url and settings.llm_api_key and settings.llm_model:
            raw = await self._llm.plan(request.instruction)
            return self._validate_plan(raw)
        return self._fallback_plan(request)

    def _validate_plan(self, raw: dict) -> AgentPlan:
        raw_steps = raw.get("steps", [])
        if not isinstance(raw_steps, list):
            raise ValueError("invalid_llm_plan_steps")
        steps: list[PlanStep] = []
        for raw_step in raw_steps[: settings.max_steps]:
            if not isinstance(raw_step, dict):
                continue
            capability = raw_step.get("capability")
            if capability not in ALLOWED_CAPABILITIES:
                continue
            raw_input = raw_step.get("input", {})
            steps.append(
                PlanStep(
                    capability=capability,
                    input=raw_input if isinstance(raw_input, dict) else {},
                    reason=str(raw_step.get("reason", "")),
                )
            )
        return AgentPlan(status="planned", steps=steps)

    def _fallback_plan(self, request: AgentRequest) -> AgentPlan:
        text = request.instruction.lower()
        steps: list[PlanStep] = []
        if "lead" in text:
            steps.append(PlanStep(capability="lead.list", reason="The request references leads."))
        elif "conversation" in text or "inbox" in text:
            steps.append(PlanStep(capability="conversation.list", reason="The request references conversations."))
        elif "automation" in text or "journey" in text:
            steps.append(PlanStep(capability="automation.list", reason="The request references automations."))
        elif "company" in text:
            steps.append(PlanStep(capability="company.search", reason="The request references companies."))
        return AgentPlan(status="planned", steps=steps[: settings.max_steps])
