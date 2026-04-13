# Agent Architecture Design Patterns

To maintain the high quality of the Investment Agent Team, follow these architectural principles when refining or adding features:

## 1. Information Asymmetry (信息不对称原则)
- **Constraint**: Each agent must have a limited "information slice."
- **Why**: Prevents "groupthink." If the Adversary Agent knows the Strategy Agent's internal reasoning, it will attack the *reasoning* instead of the *conclusion*.
- **Implementation**: Orchestrator must strip `<thinking>` tags when passing data between agents.

## 2. Tagged Reasoning (标签化推理)
- **Mandate**: Every agent MUST use `<thinking>` (internal/uncertain) and `<speaking>` (formal/structured).
- **Quality Check**: `<speaking>` should never contain "I think" or "maybe"—it must be a direct logical derivative of the `<thinking>` process.

## 3. Operational Grounding (实战锚定)
- **Data Sourcing**: Agents must not "hallucinate" prices. The workflow must include a tool-call to fetch real-time data before the first agent (Strategy) starts.
- **Triangulation**: News verification must require at least two independent sources or one Tier 1 official source.

## 4. Execution Loop (执行闭环)
- **Alert Logic**: Map logic states (GREEN/YELLOW/RED) to specific brokerage instructions.
- **Persistence**: Every change to an agent's role or a target's protocol must be synced to structured JSON files (`portfolio/`) and pushed to Git.

## 5. Re-analysis Trigger (重构触发)
- **Automatic Invalidation**: If a monitored variable (like "Model 2 production delay") is detected, the Orchestrator MUST force a re-analysis cycle.
- **User Confirmation**: No Git sync should occur for strategy updates without explicit user approval.
