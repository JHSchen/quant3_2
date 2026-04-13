# API Integration Guide

## 架构：如何在代码中实现Agent Team

### 单次分析流程（API调用链）

```javascript
// ============================================================
// 投资Agent Team 调用编排器
// ============================================================

const MODELS = {
  strategy: "claude-sonnet-4-20250514",
  adversary: "claude-sonnet-4-20250514",
  risk: "claude-sonnet-4-20250514",
};

const MAX_REBUILD_ITERATIONS = 3;

// ---- 工具函数 ----

function extractTagContent(text, tag) {
  const regex = new RegExp(`<${tag}>([\\s\\S]*?)<\\/${tag}>`, 'g');
  const matches = [];
  let match;
  while ((match = regex.exec(text)) !== null) {
    matches.push(match[1].trim());
  }
  return matches.join('\n');
}

function extractSpeaking(response) {
  const fullText = response.content
    .filter(item => item.type === "text")
    .map(item => item.text)
    .join("\n");
  return extractTagContent(fullText, 'speaking');
}

function extractThinking(response) {
  const fullText = response.content
    .filter(item => item.type === "text")
    .map(item => item.text)
    .join("\n");
  return extractTagContent(fullText, 'thinking');
}

// ---- Agent 调用函数 ----

async function callAgent(systemPrompt, userMessage, model) {
  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: model,
      max_tokens: 4000,
      system: systemPrompt,
      messages: [{ role: "user", content: userMessage }],
    }),
  });
  return await response.json();
}

// ---- 主编排流程 ----

async function runInvestmentAnalysis(userInput) {
  const results = {
    phases: [],
    finalReport: null,
    rebuildCount: 0,
  };

  // Phase 0: 输入校验
  const validation = validateInput(userInput);
  if (validation.status !== "PASS") {
    return { error: validation.message };
  }

  let strategyInput = userInput;
  let converged = false;

  while (!converged && results.rebuildCount < MAX_REBUILD_ITERATIONS) {
    // Phase 1: Strategy Agent
    const strategyResponse = await callAgent(
      STRATEGY_SYSTEM_PROMPT,
      strategyInput,
      MODELS.strategy
    );
    const strategySpeaking = extractSpeaking(strategyResponse);
    const strategyThinking = extractThinking(strategyResponse);

    results.phases.push({
      phase: "strategy",
      iteration: results.rebuildCount,
      speaking: strategySpeaking,
      thinking: strategyThinking, // Orchestrator可见
    });

    // Phase 2: Adversary Agent（只传speaking）
    const adversaryResponse = await callAgent(
      ADVERSARY_SYSTEM_PROMPT,
      `以下是Strategy Agent的策略结论。你不知道他的推理过程。请进行对抗性验证。\n\n${strategySpeaking}`,
      MODELS.adversary
    );
    const adversarySpeaking = extractSpeaking(adversaryResponse);
    const adversaryThinking = extractThinking(adversaryResponse);

    results.phases.push({
      phase: "adversary",
      iteration: results.rebuildCount,
      speaking: adversarySpeaking,
      thinking: adversaryThinking,
    });

    // Phase 3: 收敛判断
    if (adversarySpeaking.includes("REBUILD_TOPOLOGY")) {
      results.rebuildCount++;
      // 将攻击点注入下一轮Strategy输入
      strategyInput = `${userInput}\n\n## 对抗Agent的攻击点（必须在重构中回应）：\n${adversarySpeaking}`;
    } else {
      converged = true;
    }
  }

  if (!converged) {
    return {
      error: "当前拓扑无解",
      reason: results.phases.filter(p => p.phase === "adversary").map(p => p.speaking),
    };
  }

  // Phase 4: Risk Agent（传入合并结论）
  const lastStrategy = results.phases.filter(p => p.phase === "strategy").pop();
  const lastAdversary = results.phases.filter(p => p.phase === "adversary").pop();

  const mergedConclusion = `
## Strategy Agent 结论（经对抗验证）：
${lastStrategy.speaking}

## Adversary Agent 验证结果：
${lastAdversary.speaking}
  `;

  const riskResponse = await callAgent(
    RISK_SYSTEM_PROMPT,
    mergedConclusion,
    MODELS.risk
  );
  const riskSpeaking = extractSpeaking(riskResponse);

  results.phases.push({
    phase: "risk",
    speaking: riskSpeaking,
    thinking: extractThinking(riskResponse),
  });

  // Phase 5: 合成最终报告
  results.finalReport = synthesizeReport(results);
  return results;
}

// ---- 输入校验 ----

function validateInput(input) {
  if (!input || input.trim().length === 0) {
    return { status: "REJECT", message: "输入为空，请提供投资分析目标" };
  }
  // 更复杂的校验可以通过LLM调用实现
  return { status: "PASS" };
}

// ---- 报告合成 ----

function synthesizeReport(results) {
  const strategy = results.phases.filter(p => p.phase === "strategy").pop();
  const adversary = results.phases.filter(p => p.phase === "adversary").pop();
  const risk = results.phases.filter(p => p.phase === "risk").pop();

  return `
# 最终投资协议

## 1. 拓扑结论
${strategy.speaking}

## 2. 对抗性验证（经${results.rebuildCount}次重构）
${adversary.speaking}

## 3. 风控定价与执行矩阵
${risk.speaking}
  `.trim();
}
```

### 持续监控流程（定时任务）

```javascript
// ============================================================
// Monitor Agent 定时检查（可部署为 cron job）
// ============================================================

async function runMonitorCheck(portfolio, finalProtocol) {
  const alerts = [];

  for (const position of portfolio) {
    // 拉取最新数据
    const marketData = await fetchMarketData(position.ticker);
    const financialData = await fetchFinancialData(position.ticker);

    // 构建Monitor Agent输入
    const monitorInput = `
## 持仓标的：${position.ticker} (${position.name})
## 当前价格：${marketData.price}
## 持仓成本：${position.costBasis}
## 今日涨跌幅：${marketData.changePercent}%
## 今日成交量：${marketData.volume}（20日均量：${marketData.avgVolume20}）
## 最新季报数据：
- 经营性现金流：${financialData.operatingCashFlow}
- 存货周转天数：${financialData.inventoryDays}
- 毛利率：${financialData.grossMargin}
- 资产负债率：${financialData.debtRatio}

## 风控阈值（来自Final Protocol）：
${JSON.stringify(finalProtocol[position.ticker], null, 2)}
    `;

    const monitorResponse = await callAgent(
      MONITOR_SYSTEM_PROMPT,
      monitorInput,
      "claude-sonnet-4-20250514"
    );

    const alertSpeaking = extractSpeaking(monitorResponse);

    // 解析Alert Level
    const alertLevel = parseAlertLevel(alertSpeaking);
    if (alertLevel !== "GREEN") {
      alerts.push({
        ticker: position.ticker,
        level: alertLevel,
        details: alertSpeaking,
        timestamp: new Date().toISOString(),
      });
    }
  }

  return alerts;
}

function parseAlertLevel(speaking) {
  if (speaking.includes("RED") || speaking.includes("🔴")) return "RED";
  if (speaking.includes("YELLOW") || speaking.includes("🟡")) return "YELLOW";
  return "GREEN";
}
```

### 与用户已有监控系统的集成

```javascript
// ============================================================
// 集成到用户现有的投资监控agent（本地Python脚本）
// ============================================================

// 用户已有的本地agent使用Claude/Gemini API进行每日分析
// 以下展示如何将Agent Team的输出注入其工作流

// 1. 将Final Protocol导出为JSON配置文件
function exportProtocolAsConfig(finalProtocol) {
  return {
    version: "1.0",
    generated_at: new Date().toISOString(),
    positions: Object.entries(finalProtocol).map(([ticker, rules]) => ({
      ticker,
      entry: rules.entry,
      add: rules.add,
      take_profit: rules.takeProfit,
      stop_loss: rules.stopLoss,
      kill_switch: rules.killSwitch,
    })),
    global_kill_switches: [
      { condition: "北美CSP Capex同比下滑>15%", check_frequency: "weekly" },
      { condition: "社融增速<8% 且 M1持续负增长", check_frequency: "monthly" },
    ],
  };
}

// 2. 将配置文件写入用户的投资逻辑文件（供本地agent读取）
// 用户的本地agent已有editable investment logic file
// Agent Team的输出可直接追加为新的规则块
```

## 降级模式：单一LLM顺序执行

当无法并行调用多个API时，使用单一conversation的多轮对话模拟Agent Team：

```javascript
async function runSingleLLMMode(userInput) {
  const messages = [];

  // Round 1: Strategy Agent
  messages.push({
    role: "user",
    content: `[System] 你现在是 Strategy Agent。${STRATEGY_BRIEF_PROMPT}\n\n用户输入：${userInput}`
  });
  const r1 = await callWithHistory(messages);
  messages.push({ role: "assistant", content: r1 });
  const strategySpeaking = extractSpeaking({ content: [{ type: "text", text: r1 }] });

  // Round 2: Adversary Agent（角色切换，只传speaking）
  messages.push({
    role: "user",
    content: `[System] 你现在是 Adversary Agent。你不知道Strategy Agent的推理过程。
以下是他的结论，请进行对抗性验证：\n\n${strategySpeaking}`
  });
  const r2 = await callWithHistory(messages);
  messages.push({ role: "assistant", content: r2 });

  // Round 3: 收敛判断 + Risk Agent
  // ... 类似模式继续
}
```

## 数据接口说明

Agent Team不内置行情/财务数据获取能力。以下是推荐的外部数据源接口：

| 数据类型 | 推荐接口 | 用途 |
|---------|---------|------|
| A股行情 | Tushare / AKShare | 实时价格、成交量、K线 |
| 财务报表 | Tushare / 东方财富API | 季报/年报核心指标 |
| ETF资金流向 | 东方财富/同花顺数据 | 板块拥挤度判断 |
| 公告/新闻 | 巨潮资讯/东方财富 | 事件驱动监控 |
| 宏观数据 | 央行/国家统计局 | 社融、M1、CPI |
| 美股/港股 | Yahoo Finance / Alpha Vantage | 跨市场标的 |
