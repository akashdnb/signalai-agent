from fastapi import Header, HTTPException

from signalai_agent.config import settings


def require_service_token(authorization: str | None = Header(default=None)) -> None:
    if not settings.service_token:
        raise HTTPException(status_code=503, detail="agent_auth_not_configured")
    expected = f"Bearer {settings.service_token}"
    if authorization != expected:
        raise HTTPException(status_code=401, detail="unauthorized")
