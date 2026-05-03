# IAT 量化操作协议 v2.0 (IAT Quantitative Operational Protocol)

## 核心辩论流 (The Core Debate Loop)

### 阶段 1：策略代理 (Strategy) - 增长质量审计
**目标**：寻找具备经济增量的“拓扑节点”。
**必须输出指标**：
- **ROIC vs WACC**：必须 > 1.2x。理由：确认企业是在创造财富还是在毁灭资本。
- **自由现金流 (FCF) 转换率**：(OCF-CapEx)/NetIncome > 70%。理由：排除账面利润幻象。
- **营收/利润 3Y-CAGR**：量化增长斜率。

### 阶段 2：对手代理 (Adversary) - 生存压力测试
**目标**：利用财务模型进行“找茬”。
**必须输出指标**：
- **Altman Z-Score**：若 < 1.8 立即触发 VETO（否决）。理由：量化破产风险。
- **Piotroski F-Score**：必须 >= 6 分。理由：通过 9 个维度审计财务健康度。
- **DSO (应收账款周转天数) 趋势**：若同比增加 > 15%，触发“虚假销售”预警。

### 阶段 3：风险代理 (Risk) - 期望定价与分配
**目标**：将逻辑转化为数学期望。
**必须输出指标**：
- **Beta 分解 (Alpha/Beta Ratio)**：Alpha 贡献必须 > 30%。理由：不买“随大盘漂泊”的平庸标的。
- **凯利公式 (Kelly Criterion)**：`K = (W * (R+1) - 1) / R`。理由：科学分配仓位。
- **估值百分位 (PE/PB Percentile)**：排除在高估值阶段入场。

---
## 执行与反馈
1. **JSON 协议化**：所有指标写入 `portfolio/protocols/` 下的 JSON。
2. **审计评分**：每笔分析必须在末尾附带基于上述指标的 **[Audit Scorecard]**。
