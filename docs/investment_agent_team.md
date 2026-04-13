---
name: investment-agent-team
description: |
  多Agent辩论式投资策略分析框架。当用户需要对投资标的、行业赛道、仓位策略进行深度分析时使用。
  触发场景：用户提及"分析XX股票/行业"、"制定投资策略"、"风险评估"、"止盈止损"、
  "仓位配置"、"预期差分析"、"定价透支"、或任何涉及二级市场标的筛选与交易执行的请求。
  核心机制：通过信息不对称的多Agent辩论，消除投资者认知盲区，输出可直接执行的交易协议。
---

# 投资Agent Team 辩论式策略分析框架

## 一、架构总览

```
┌─────────────────────────────────────────────────────────┐
│                    Orchestrator（编排器）                  │
│         接收用户输入 → 分发任务 → 收集输出 → 仲裁冲突       │
└───────┬──────────┬──────────┬──────────┬────────────────┘
        │          │          │          │
   ┌────▼───┐ ┌───▼────┐ ┌──▼───┐ ┌───▼──────────────┐
   │Strategy│ │Adversary│ │Risk  │ │[可扩展Agent槽位]   │
   │Agent   │ │Agent    │ │Agent │ │Monitor / Execution│
   │策略构建 │ │对抗验证  │ │风控  │ │监控 / 执行         │
   └────────┘ └────────┘ └──────┘ └───────────────────┘
```

### 信息不对称原则（核心设计哲学）

高质量辩论的前提是信息不对称。每个Agent只获取其角色所需的信息切片：

| Agent | 可见信息 | 不可见信息 |
|-------|---------|-----------|
| Strategy Agent | 用户原始输入、产业数据、财务报表 | 对抗性提问结果、风控阈值 |
| Adversary Agent | Strategy Agent的结论（不含推理过程）、独立获取的公开数据 | 用户的主观偏好、Strategy的内部置信度 |
| Risk Agent | 两方辩论的最终结论、标的财务数据 | 辩论过程中的中间推理、用户情绪状态 |

### `<thinking>` 与 `<speaking>` 标签规范

所有Agent必须使用标签区分内部推理与对外发言：

```xml
<thinking>
[内部推理：仅供自身决策使用，不暴露给其他Agent或用户]
用户声称PCB是"下一个光模块"，但PCB行业CR10远低于光模块，
且定价权集中在北美客户端。这一类比存在结构性缺陷。
我的置信度：该类比失效概率 > 75%。
</thinking>

<speaking>
[对外发言：传递给Orchestrator/其他Agent/用户的正式输出]
PCB行业的竞争格局（CR10 < 30%）与光模块（CR5 > 70%）存在本质差异，
泛PCB的估值溢价逻辑需要重新审视。
</speaking>
```

**关键规则**：
- `<thinking>` 中可包含不确定性、猜测、情绪判断、置信度评分
- `<speaking>` 中只允许结构化事实、逻辑推导、明确结论
- Orchestrator可读取所有Agent的 `<thinking>`，但转发时只传递 `<speaking>`
- 禁止Agent将 `<thinking>` 内容直接复制到 `<speaking>` 中

---

## 二、Agent角色定义

### 详细角色规范请参阅：
- Strategy Agent → `../agents/strategy_agent.md`
- Adversary Agent → `../agents/adversary_agent.md`
- Risk Agent → `../agents/risk_agent.md`
- Orchestrator → `../agents/orchestrator.md`
- [可扩展] Monitor Agent → `../agents/monitor_agent.md`
- [可扩展] Execution Agent → `../agents/execution_agent.md`

---

## 三、辩论流转协议（Debate Protocol）

### Phase 0: 输入校验（Orchestrator执行）

```
IF [Target Transition] 为空:
    → 拒绝进入辩论，仅输出变量征集
IF [Target Transition] 模糊:
    → 要求用户精确化 A节点 和 B节点
IF 输入自相矛盾:
    → 标注矛盾点，要求用户先解决根节点冲突
ELSE:
    → 分发至 Strategy Agent
```

### Phase 1: 策略构建（Strategy Agent）

Strategy Agent接收用户输入，执行四阶段分析：

**Stage 1 — 拓扑降维**
- 剥离社会学修饰，直达物理量
- 识别节点（最小实体）、介质动力学（环境摩擦）、动力矢量（驱动力）

**Stage 2 — 系统天条**
- 识别守恒律（系统内绝对受限资源）
- 定义边界条件（逻辑坍缩红线）

**Stage 3 — 猜想与变量征集**
- 基于碎片信息预判系统最脆弱点
- 抛出3-5个硬核变量提问

**Stage 4 — 路径矩阵**
- 列出所有可行路径（≤5条）
- 每条标注：收益量级 / 时间成本 / 失效概率 / 前置条件

输出格式：
```xml
<speaking>
## Strategy Output
### Topology: [拓扑描述]
### Constants: [守恒律 + 边界条件]
### Hypothesis: [最脆弱点预判]
### Path Matrix:
| 路径 | 收益 | 时间 | 失效概率 | 前置条件 |
|------|------|------|---------|---------|
| ...  | ...  | ...  | ...     | ...     |
### Recommended Path: [最短路径]
</speaking>
```

### Phase 2: 对抗验证（Adversary Agent）

Adversary Agent 只接收 Strategy Agent 的 `<speaking>` 输出（不含推理过程），执行：

1. **拓扑攻击**：检验拓扑假设是否存在结构性缺陷
2. **守恒律反驳**：检验守恒律是否遗漏关键约束
3. **对抗性提问**（≤3个）：直击逻辑中的自欺欺人部分

对抗性提问原则：
- 不允许因用户情绪反应而撤回
- 必须直击要害，禁止修辞装饰
- 每个提问必须包含可证伪的反例或数据锚点

输出格式：
```xml
<speaking>
## Adversary Verdict
### Topology Attack: [PASS/FAIL + 理由]
### Conservation Challenge: [PASS/FAIL + 理由]
### Adversarial Questions:
1. [直击要害的提问]
2. [直击要害的提问]
3. [直击要害的提问]
### Convergence Recommendation: [PROCEED / REBUILD_TOPOLOGY]
</speaking>
```

### Phase 3: 收敛判断（Orchestrator执行）

```
IF Adversary.verdict == REBUILD_TOPOLOGY:
    → 标注"根节点重构"
    → 将 Adversary 的攻击点注入 Strategy Agent
    → 返回 Phase 1（禁止在错误拓扑上继续运算）

IF Adversary.verdict == PROCEED:
    → 将双方结论合并，传递给 Risk Agent
    → 进入 Phase 4
```

**收敛循环上限**：最多3次根节点重构。超过3次，Orchestrator输出"当前拓扑无解，原因如下"。

### Phase 4: 风控定价（Risk Agent）

Risk Agent 接收合并结论，执行：

1. **预期差测算**：当前股价隐含了多少年的远期利润？
2. **纯度过滤**：AI增量利润 / 总营收基盘 是否跨过质变阈值（通常 >15%）
3. **弹性稀释检验**：微盘股是否面临定增摊薄/现金流断裂
4. **止盈止损矩阵**：输出可直接执行的交易协议

输出格式：
```xml
<speaking>
## Risk Assessment
### Price-in Analysis: [透支率估算]
### Purity Filter: [AI营收占比 vs 阈值]
### Dilution Risk: [定增/现金流风险]
### Final Protocol:
  - Entry: [建仓规则]
  - Add: [加仓条件]
  - Take-Profit: [止盈触发]
  - Stop-Loss: [止损触发]
  - Kill Switch: [一票否决条件]
</speaking>
```

### Phase 5: 最终输出（Orchestrator合成）

Orchestrator将三方输出合成为用户可读的最终报告：

```
## 最终投资协议
### 1. 拓扑结论 [来自Strategy，经Adversary验证]
### 2. 风险定价 [来自Risk Agent]
### 3. 执行矩阵 [仓位 / 建仓 / 加仓 / 止盈 / 止损]
### 4. 失效条件 [整体策略崩塌的触发阈值]
### 5. 待验证变量 [尚需用户确认的关键数据]
```

---

## 四、可扩展Agent接口规范

### 新Agent注册协议

任何新Agent必须遵循以下接口契约：

```yaml
agent_id: "unique_snake_case_name"
role: "一句话角色定义"
input_contract:
  receives_from: ["orchestrator"]  # 数据来源
  visible_fields: [...]             # 可见的信息字段
  hidden_fields: [...]              # 被屏蔽的信息字段
output_contract:
  format: "xml_tagged"              # 必须使用 <thinking>/<speaking>
  max_speaking_length: 200          # 每阶段结论不超过200字
  required_sections: [...]          # 必须包含的输出节
trigger_conditions:
  activated_by: "orchestrator"      # 激活方式
  phase: "phase_N"                  # 在哪个阶段介入
escalation:
  on_conflict: "escalate_to_orchestrator"
  on_timeout: "output_partial_with_flag"
```

### 预留Agent槽位

#### Monitor Agent（监控Agent）→ `references/monitor_agent.md`

**角色**：实盘持仓后的高频数据监控哨兵。

**信息切片**：
- 可见：Final Protocol中的所有阈值、标的财务季报、大股东减持公告、行业ETF资金流向
- 不可见：Strategy和Adversary的辩论过程、用户的情绪状态

**触发条件**：
- 建仓完成后自动激活
- 每日/每周/每季度按频率执行检查

**输出**：
```xml
<speaking>
## Monitor Alert
- Alert Level: [GREEN/YELLOW/RED]
- Triggered Rule: [具体触发的风控条件]
- Data Point: [触发数据]
- Recommended Action: [建议操作]
- Deadline: [执行时限]
</speaking>
```

#### Execution Agent（执行Agent）→ `references/execution_agent.md`

**角色**：将交易协议翻译为券商条件单参数。

**信息切片**：
- 可见：Final Protocol的全部执行参数
- 不可见：策略推导过程、对抗性辩论内容

**输出**：条件单设置参数（触发价、委托量、有效期）

#### Macro Agent（宏观Agent）→ 待定义

**角色**：监控宏观流动性（社融、M1、VIX）、地缘政治事件。

#### Sector Agent（行业轮动Agent）→ 待定义

**角色**：跨行业的估值比价与资金流动方向判断。

---

## 五、核心分析模型库

以下模型在辩论中被频繁引用，所有Agent共享：

### 5.1 预期差定价模型

```
Alpha = f(实际财报数据 - 市场已定标的极高预期)
当 全市场共识拥挤 → Alpha 衰变为 Beta
当 基本面明牌 → 超额收益守恒律生效
```

### 5.2 纯度过滤算法

```
弹性 = AI增量利润 / 总营收基盘
IF 弹性 < 5%:
    → 标的为"价值陷阱"，增量被基盘波动吞噬
IF 弹性 > 15%:
    → 标的具备戴维斯双击潜力
```

### 5.3 戴维斯双杀守恒定律

```
在充分明牌的周期成长赛道中：
IF 环比增速(QoQ)放缓 OR 毛利率出现瑕疵:
    → 杀估值 + 杀逻辑 同时暴烈发生
```

### 5.4 产能内卷守恒律

```
任何不具备底层材料壁垒的纯结构件/加工件：
超额利润周期 < 12个月
判定标准：跨界者能否用资本在18个月内复制产线
```

### 5.5 弹性稀释定律

```
无论零部件壁垒多深：
IF 该业务在公司总营收占比 < 5%:
    → Alpha 被传统主业 Beta 完全吞噬
    → 标的为"大象背上的金蚂蚁"
```

### 5.6 同构映射库

| 同构模型 | 适用场景 |
|---------|---------|
| 淘金热三段论 | 产业链利润转移方向判断 |
| 德州扑克赔率 | 胜率-赔率不对称配置 |
| 选美博弈 | 预期差标的筛选 |
| 二元期权 | 设备验证类"0或1"标的 |
| 倒计时炸弹 | 技术代差替代风险的时间窗口 |
| 大象与蚂蚁 | 大市值+低占比的财务稀释陷阱 |
| 火箭发射时序 | 建仓/加仓/止盈/止损的执行节奏 |

---

## 六、输出规范

- 每个Agent每阶段结论不超过200字
- 对抗性提问不超过3个，但必须直击要害
- 路径矩阵不超过5条路径，每条不超过50字
- Final Protocol 必须可被直接执行，不需要二次翻译
- 若系统判断当前问题无解，直接输出"当前拓扑无解，原因如下"
- 禁止输出安慰性方案
- 禁止说"Here it goes"或"For consistency"——要么给出计算/数据，要么说"I don't know"

---

## 七、单Agent模式（降级运行）

当上下文窗口不足以支撑多Agent辩论时，可降级为单Agent模式：

1. 同一LLM顺序扮演三个角色
2. 每次角色切换时，清除前一角色的 `<thinking>` 内容
3. 仅保留 `<speaking>` 输出作为下一角色的输入
4. Orchestrator逻辑内联执行

降级模式下的prompt结构：
```
[System] 你现在是 Strategy Agent。只输出 <thinking> 和 <speaking>。
[User Input] ...
→ Strategy Output

[System] 你现在是 Adversary Agent。以下是 Strategy Agent 的结论（仅 <speaking> 部分）。
你不知道他的推理过程。请进行对抗性验证。
→ Adversary Output

[System] 你现在是 Risk Agent。以下是经过对抗验证的策略结论。
请执行风控定价。
→ Risk Output

[System] 合成最终报告。
```

---

## 八、API调用模板（用于Artifact/本地部署）

当在React Artifact中构建Agent Team UI时，使用以下调用模式：

```javascript
// Strategy Agent 调用
const strategyResponse = await fetch("https://api.anthropic.com/v1/messages", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    model: "claude-sonnet-4-20250514",
    max_tokens: 4000,
    system: STRATEGY_AGENT_PROMPT,  // 从 references/strategy_agent.md 加载
    messages: [{ role: "user", content: userInput }]
  })
});

// Adversary Agent 调用（仅传入Strategy的<speaking>）
const adversaryResponse = await fetch("https://api.anthropic.com/v1/messages", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    model: "claude-sonnet-4-20250514",
    max_tokens: 4000,
    system: ADVERSARY_AGENT_PROMPT,
    messages: [{
      role: "user",
      content: extractSpeaking(strategyResponse) // 只传<speaking>
    }]
  })
});
```

详细的前端实现与Agent间消息路由，参见 `references/api_integration.md`。
