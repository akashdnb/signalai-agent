# SignalAI Agent

Python agent runtime for planning and orchestration over SignalAI capabilities. The agent does not access product persistence directly.

## Current runtime

- FastAPI service
- authenticated planning endpoint
- OpenAI-compatible `/chat/completions` planning provider when configured
- conservative read-only capability allowlist
- deterministic fallback planner when an LLM provider is intentionally not configured

## Safety boundary

The model can only produce plans containing explicitly allowed read capabilities. Write/destructive/outbound actions are not executable from this planning endpoint.

Long-running work must be represented as a server-owned job and executed by `signalai-worker`. The agent must not directly access PostgreSQL or provider APIs.

## Configuration

Set `SIGNALAI_LLM_BASE_URL`, `SIGNALAI_LLM_API_KEY`, and `SIGNALAI_LLM_MODEL` to enable model planning. The endpoint remains protected by `SIGNALAI_SERVICE_TOKEN`.
