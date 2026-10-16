import pytest

from signalai_agent.models import AgentRequest
from signalai_agent.planner import CapabilityPlanner


@pytest.mark.asyncio
async def test_planner_maps_lead_request_to_read_capability():
    plan = await CapabilityPlanner().plan(
        AgentRequest(tenant_id="tenant", correlation_id="corr", instruction="show my leads")
    )
    assert plan.steps[0].capability == "lead.list"


@pytest.mark.asyncio
async def test_planner_does_not_invent_unsupported_actions():
    plan = await CapabilityPlanner().plan(
        AgentRequest(tenant_id="tenant", correlation_id="corr", instruction="delete everything")
    )
    assert plan.steps == []
