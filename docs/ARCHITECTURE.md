# SignalAI Agent Architecture

## Purpose

`signalai-agent` is the reasoning/orchestration runtime for AI agents operating on SignalAI capabilities. It decides what actions may be useful, plans multi-step work, manages model context, invokes tools and coordinates long-running tasks.

It does not own product truth.

## Boundary

```text
User / SignalAI UI / AG-UI
          |
          v
     agent runtime
          |
   +------+-------+
   |              |
 MCP tools    server capabilities
   |              |
   +------+-------+
          |
     SignalAI server
          |
     domain + DB
```

The agent may reason; the server authorizes and validates.

## Responsibilities

- model routing
- prompt/context assembly
- planning
- tool selection
- multi-step orchestration
- streaming responses/events
- task state for long-running agent runs
- human approval pauses
- model/tool tracing
- token and cost controls
- evaluation hooks

## Out of scope

- direct production database access
- independent CRM state
- bypassing server authorization
- provider-specific APIs
- MCP server implementation
- journey publication rules

## Tool access

The agent can use SignalAI capabilities through approved interfaces, including MCP where appropriate. Tool access is policy-controlled and should be allowlisted per agent/task.

Never expose a raw database/query tool to an autonomous model.

## Planning model

A run should be represented as:

```text
request
  -> understand goal
  -> build plan
  -> validate available tools/permissions
  -> execute step
  -> observe result
  -> re-plan if needed
  -> approval gate when required
  -> complete
```

Each step should have a bounded timeout and retry policy.

## Human approval

High-impact actions must pause before execution. The approval request should describe:

- intended action
- target
- expected side effect
- relevant parameters
- why the agent selected it

Approval is enforced by the server/capability layer, not merely by a prompt instruction.

## Memory

Separate:

- conversation context
- task/run state
- durable product state
- model-generated working memory

Model working memory must never silently become authoritative CRM or journey state.

## Model routing

Model selection should consider task complexity, latency, quality and cost. Routing policy should be observable and configurable rather than embedded in individual prompts.

## Long-running tasks

Agent tasks that exceed an HTTP request lifecycle should become durable jobs and execute through `signalai-worker`. The agent service should track plan/task state while the worker performs long-running execution.

## AG-UI

AG-UI is an interaction protocol/interface for streaming agent state to product clients. It should consume agent events rather than embedding agent implementation details in the frontend.

## Reliability

Agent runs require:

- run IDs
- correlation IDs
- bounded loops
- tool timeouts
- retryable vs permanent error classification
- cancellation
- partial-result handling
- budget/token limits
- deterministic audit records for side effects

## Security

Treat model output and external retrieved content as untrusted. Authorization must be checked at the capability boundary for every meaningful action.

The agent must not infer permission from user wording, retrieved content or another tool's output.
