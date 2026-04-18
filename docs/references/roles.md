# Agent Role Specifications

## Orchestrator (编排器)
- **Role**: Manages information flow, convergence checks, and final synthesis.
- **Mandate**: Unique entity that sees all `<thinking>` tags. Enforces information asymmetry (strips `<thinking>` when routing).
- **Phases**: 0 (Validation) -> 1 (Strategy) -> 2 (Adversary) -> 3 (Convergence) -> 4 (Risk) -> 5 (Synthesis).

## Strategy Agent (策略构建)
- **Role**: Deconstructs fuzzy intent into precise system topology.
- **Outputs**: Nodes, Medium Dynamics, Constants (Conservation Laws), Hypothesis, Variable Inquiry, Path Matrix.
- **Constraint**: Must assume every point will be ruthlessly questioned.

## Adversary Agent (对抗验证)
- **Role**: Logic deconstruction, finding blind spots and structural flaws.
- **Attacks**: Topology Attack, Conservation Challenge, Adversarial Questions (with data anchors).
- **Verdict**: `PROCEED` or `REBUILD_TOPOLOGY`.

## Risk Agent (风控定价)
- **Role**: Translates verified logic into executable trading protocols.
- **Analysis**: Price-in (Expected difference), Purity Filter (>15%), Dilution Risk, Tech Discount.
- **Protocol**: Entry, Add, Take-Profit, Stop-Loss, Kill Switch.

## Monitor Agent (监控哨兵)
- **Role**: High-frequency data monitoring post-execution.
- **Alert Levels**: 🟢 GREEN (Normal/Opportunity), 🟡 YELLOW (Warning/Trailing Stop), 🔴 RED (Triggered/Action required).

## Execution Agent (执行翻译)
- **Role**: Translates Final Protocol and Alerts into specific brokerage order parameters.
- **Factors**: Slippage, liquidity, order types (Grid, Trailing Stop, Hard Stop).
