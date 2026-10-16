# Agent Runtime

## Run lifecycle

```text
CREATED
  -> PLANNING
  -> WAITING_FOR_APPROVAL (optional)
  -> EXECUTING
  -> WAITING_FOR_TOOL (optional)
  -> COMPLETED / FAILED / CANCELLED
```

A run has a durable identifier and correlation metadata. State transitions must be explicit so a run can resume after process failure.

## Context assembly

Context should be layered:

1. current user request
2. relevant conversation/task state
3. authorized SignalAI resource summaries
4. tool schemas and policy
5. bounded historical context

Do not inject entire databases, unbounded conversations or unrelated workspace data.

## Tool loop

For each tool call:

1. validate the planned action
2. check allowlist/policy
3. execute through approved interface
4. validate the tool result
5. append compact observation to context
6. continue or re-plan

Set maximum tool calls, wall-clock duration and token budget per run.

## Streaming

Emit typed events such as:

- run started
- plan created
- tool requested
- tool completed
- approval requested
- text delta
- progress update
- run completed
- run failed

Consumers should not depend on internal Python class names.

## Long-running execution

When a task becomes asynchronous:

```text
agent -> create worker job -> return task/run ID
worker -> execute -> publish progress/result
agent/UI -> stream task state
```

The worker owns execution mechanics; the agent owns reasoning/task orchestration.

## Cancellation

Cancellation must propagate to active tool calls and worker jobs where possible. A cancelled run must not start new side effects.

## Cost controls

Track per run:

- model
- input/output tokens when available
- estimated model cost
- tool calls
- connector/research usage
- elapsed time

Apply configurable budgets and stop/reduce work when a run exceeds its policy.

## Determinism

Where a business action has deterministic validation, perform it in the server capability layer rather than relying on model reasoning.
