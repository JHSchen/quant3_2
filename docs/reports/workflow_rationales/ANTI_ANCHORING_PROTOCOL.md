# 行为金融学修复协议：防锚定跳变控制 (FGO Protocol)

## 1. 痛点定义 (The Anchoring Trap)
在结构性基本面利好（如 MU HBM4 提前出货）发生时，Agent 往往仍旧锚定历史支撑位（如 $505）进行挂单，导致在价格跳空（Gap-up）时完全踏空。这被定义为 **“执行层钝化”**。

## 2. 强制触发逻辑 (Trigger Rules)
当下属任一条件满足时，Agent **必须** 废弃“等待回踩”逻辑，强制执行“市价底仓”：
- **新闻强度 (News Intensity)**: 经过 Triangulation 验证的利好新闻，权重 > 8/10。
- **价格偏离 (Price Deviation)**: 现价高于协议基准价 (Baseline) > 5%，且伴随成交量放大 > 50%。
- **供应端冲击 (Supply Shock)**: 逻辑节点涉及“产能枯竭”、“涨价螺旋”或“技术突破”。

## 3. 执行修正指令 (Corrective Actions)
1. **废弃补仓限价 (Bypass Limit T1)**: 若发生向上跳空，原计划的 Limit T1 必须立即转为 Market T2。
2. **强制底仓 (Mandatory Seed)**: 必须在 1 个交易时段内完成 Target Weight 的 50% 构建，不允许因“等待更优价位”而延迟。
3. **二阶动量检查**: 若股价突破 1.5x ATR 且基本面逻辑未证伪，严禁进行任何“减仓复盘”动作，直至达到 Fundamental TP。

## 4. 历史惨痛案例 (Legacy Failures)
- **2026-05-05 (MU)**: 锚定 $505 回踩，错失 $517 -> $576 (11.4%) 的跳空行情。原因：未识别 HBM4 提前出货对 WAP 逻辑的瞬间强化。
