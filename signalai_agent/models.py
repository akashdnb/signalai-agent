from typing import Literal

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    tenant_id: str = Field(min_length=1)
    correlation_id: str = Field(min_length=1)
    instruction: str = Field(min_length=1, max_length=10_000)


class PlanStep(BaseModel):
    capability: str
    input: dict = Field(default_factory=dict)
    reason: str


class AgentPlan(BaseModel):
    status: Literal["planned"]
    steps: list[PlanStep] = Field(default_factory=list)
