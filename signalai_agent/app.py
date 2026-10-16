from contextlib import asynccontextmanager

from fastapi import FastAPI

from signalai_agent.config import settings
from signalai_agent.models import AgentPlan, AgentRequest
from signalai_agent.planner import CapabilityPlanner


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app = FastAPI(title="SignalAI Agent", version=settings.service_version, lifespan=lifespan)
planner = CapabilityPlanner()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.service_name}


@app.get("/ready")
async def ready() -> dict[str, str]:
    return {"status": "ready", "service": settings.service_name}


@app.post("/v1/plan", response_model=AgentPlan)
async def plan(request: AgentRequest) -> AgentPlan:
    return planner.plan(request)
