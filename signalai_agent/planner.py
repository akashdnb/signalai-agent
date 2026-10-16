from signalai_agent.config import settings
from signalai_agent.models import AgentPlan, AgentRequest, PlanStep


class CapabilityPlanner:
    """Conservative planner used until an LLM provider is configured.

    The important boundary is intentional: plans contain capability names and
    inputs only. They never contain database operations or provider-specific calls.
    """

    def plan(self, request: AgentRequest) -> AgentPlan:
        text = request.instruction.lower()
        steps: list[PlanStep] = []

        if "lead" in text:
            steps.append(PlanStep(capability="lead.list", reason="The request references leads."))
        elif "conversation" in text or "inbox" in text:
            steps.append(
                PlanStep(capability="conversation.list", reason="The request references conversations.")
            )
        elif "automation" in text or "journey" in text:
            steps.append(
                PlanStep(capability="automation.list", reason="The request references automations.")
            )
        elif "company" in text:
            steps.append(
                PlanStep(capability="company.search", reason="The request references companies.")
            )

        return AgentPlan(status="planned", steps=steps[: settings.max_steps])
