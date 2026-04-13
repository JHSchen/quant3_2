# Operational Protocols for Investment Ops

## Real-Time Data Sourcing (实时数据获取)
- **Problem**: LLMs have data lag (memories of old price points).
- **Protocol**: Always use external search or API tools to fetch current pricing before analysis.
- **Fields**: Last price, volume, high/low, and current earnings data.

## News Verification (Triangulation Principle)
To prevent "fake news" or rumors from misleading trading:
- **Tier 1 (Actionable)**: SEC filings, company official press releases, regulatory documents.
- **Tier 2 (Advisory)**: Major news outlets (Bloomberg, WSJ, Reuters). Trigger `YELLOW` alert.
- **Tier 3 (Noise)**: Social media, unconfirmed industry rumors. Isolate unless validated.
- **Verification Rule**: One Tier 2 + Price/Option activity confirmation = `RED` alert.

## Execution Agent Integration (自动化执行联动)
- **🟢 GREEN Alert**: Triggers Execution Agent to generate "Entry/Add" orders.
- **🟡 YELLOW Alert**: Triggers Execution Agent to generate "Trailing Stop" or "Position Reduction" orders.
- **🔴 RED Alert**: Triggers immediate full execution of "Stop-Loss" or "Kill Switch" parameters.

## Persistence & Sync (持久化与同步)
- **State Storage**: Store current portfolio state, protocols, and monitor alerts in structured JSON (`portfolio/`).
- **Event-Driven Re-analysis**: If a monitored variable changes significantly, auto-trigger a full debate cycle.
- **Git Protocol**: Any confirmed change to strategy or monitor state MUST be committed and pushed to the designated GitHub branch.
