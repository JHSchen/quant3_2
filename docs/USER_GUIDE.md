# Investment Agent Team User Guide

Welcome to the **Investment Agent Team**, a specialized multi-agent framework deployed on Gemini CLI designed for professional-grade investment analysis and portfolio management.

## 1. Core Architecture

The system operates using a **Simulated Debate Protocol** to eliminate cognitive biases:

- **Orchestrator**: Manages the flow and enforces information asymmetry.
- **Strategy Agent**: Deconstructs targets into logical topologies and path matrices.
- **Adversary Agent**: Ruthlessly challenges the strategy to find structural flaws.
- **Risk Agent**: Translates logic into hard trading protocols (Price-in, Purity, Exit rules).
- **Monitor Agent**: Tracks real-time data and issues GREEN/YELLOW/RED alerts.
- **Execution Agent**: Translates alerts into specific brokerage order parameters.

## 2. Getting Started

### Installation
1. Ensure you are in the project workspace.
2. Install the skills:
   ```bash
   gemini skills install skills/investment-agent-ops.skill --scope workspace
   gemini skills install skills/agent-architect-guide.skill --scope workspace
   ```
3. Reload skills in your interactive session: `/skills reload`.

### Basic Usage
- **Analyze a stock**: `Analyze Tesla (TSLA) based on the latest FSD news.`
- **Check portfolio status**: `What is the current monitor alert for BABA?`
- **Update strategy**: `Update my TSLA protocol because Elon Musk just announced X.`

## 3. Operational Protocols

### Real-Time Data Sourcing
The system is mandated to fetch live market prices and news before any analysis. It rejects "hallucinated" data from the model's training memory.

### News Verification (Triangulation)
To prevent reacting to rumors, the system prioritizes:
1. **Tier 1**: SEC Filings / Official Press Releases.
2. **Tier 2**: Major news outlets (Bloomberg, Reuters, WSJ).
3. **Verification**: A Tier 2 news item must be cross-referenced with market activity (Volume/Options) before triggering a RED alert.

## 4. Automation & Sync

Every confirmed strategy or monitoring update is persisted:
- **Location**: `portfolio/protocols/[TICKER]_protocol.json` and `portfolio/active_portfolio_monitor.json`.
- **Git Sync**: The system automatically commits and pushes confirmed changes to the GitHub repository to maintain a synchronized "investment brain."

## 5. Customization

Use the `agent-architect-guide` skill to refine the system:
- "I want to make the Adversary Agent more aggressive regarding valuation."
- "Add a Macro Agent to monitor Fed interest rate changes."

## 6. Folder Structure
- `agents/`: Source specifications for all agent roles.
- `portfolio/`: Structured JSON configurations for your active positions.
- `skills/`: Packaged `.skill` files and source code.
- `docs/`: Technical guides, data verification strategies, and user documentation.
