# Data Sourcing & News Verification Strategy

由于大语言模型（LLM）存在数据滞后和幻觉，Monitor Agent 在实盘环境中必须挂载外部实时数据 API，并执行严格的消息交叉验证。

## 1. 实时行情数据获取 (Pricing & Fundamentals)

Monitor Agent 必须通过脚本（例如 Python 的 `yfinance`, `ccxt`, 或专用机构接口如 Bloomberg Terminal API, Wind, Tushare）获取：
- **实时/延时 15 分钟的价格**：替代内部模拟推演的占位符。
- **成交量与技术指标**：判断是否触发“放量下跌/熔断”。
- **财报源数据**：直接解析 10-Q / 10-K（SEC EDGAR 数据库），提取核心增量数据（例如：BABA 阿里云利润占比，TSLA 储能利润占比）。

## 2. 消息源监控与真实性核验 (News Verification Protocol)

针对事件驱动（Event-Driven）的策略（如：关税落地、苹果合作、FSD授权），采用 **Triangulation（三角验证）原则** 过滤噪音和自媒体小作文：

### 规则 A：信源权重分级
- **Tier 1 (可直接触发风控动作)**: SEC 公告 (8-K)、公司官方新闻稿 (IR 网站)、监管部门红头文件 (如美国商务部)。
- **Tier 2 (触发黄色预警/需人工确认)**: Bloomberg, Reuters, WSJ 等一线财经媒体的“独家报道 (Exclusive)”。
- **Tier 3 (噪音过滤/仅供参考)**: X (Twitter) 大V、Substack 分析师、未经证实的产业链传闻。

### 规则 B：交叉验证逻辑 (Cross-Validation)
1. **单一 Tier 2 报道** -> 触发 `YELLOW Alert`（提请用户关注），但不执行止盈/止损买卖。
2. **Tier 2 报道 + 期权/暗盘异动 (隐性资金抢跑)** -> 升格为 `RED Alert`，按滑点管理方案先减仓 20%-30% 避险。
3. **Tier 1 官方公告** -> 立即触发 `RED Alert`，全量执行 Final Protocol（如触发 Kill Switch，无条件清仓）。

### 规则 C：AI 溯源防伪
当 Monitor Agent 抓取到爆炸性新闻时，必须调用搜索引擎 API（如 Google Custom Search 或 Perplexity API）反查该新闻的最早出处。如果溯源指向的是单一且未具名的匿名博客，直接标记为 `[False Positive Risk]` 并隔离。
