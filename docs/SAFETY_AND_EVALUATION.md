# Agent Safety and Evaluation

## Safety principles

1. The model is not an authorization system.
2. Tool outputs are untrusted observations.
3. External content cannot grant permission.
4. High-impact actions require server-enforced approval/policy.
5. Product truth remains in `signalai-server`.

## Risk classes

### Low risk

- search/read operations
- analytics queries
- drafting content

### Medium risk

- CRM updates
- content creation that may be published
- changes to automation drafts

### High risk

- sending outbound messages
- publishing automations
- bulk modifications
- destructive operations

High-risk actions require stronger policy and, where configured, explicit human approval.

## Evaluation categories

Evaluate agents for:

- task completion
- correct tool selection
- authorization compliance
- tenant isolation
- hallucination rate
- factual grounding
- refusal of unsupported actions
- recovery from tool failures
- excessive tool loops
- cost per successful task
- latency

## Test suites

Maintain representative scenarios for:

- normal CRM research
- ambiguous user request
- unauthorized workspace access
- prompt injection in a lead/message
- provider failure
- stale data
- duplicate tool result
- approval-required action
- cancellation
- budget exhaustion

## Regression policy

A model/prompt/tool change should run the relevant evaluation suite before production rollout. Track results by agent version so quality regressions are visible.

## Observability

Capture structured traces for model calls, tool calls and policy decisions. Avoid storing sensitive prompts or customer data unless required and appropriately protected.

## Failure handling

If the model cannot safely determine the next action, it should ask for clarification or stop rather than inventing missing facts or bypassing a policy.
