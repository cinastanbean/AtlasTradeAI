
## 📊 Agent 系统使用大模型情况分析

### 🎯 **总结：所有 11 个 Agent 都具备使用大模型的能力**

你的系统采用了**"规则 + 大模型混合"**的架构设计，所有 Agent 都可以通过 [`IntelligentRoleAgentService`](file:///Users/jinniu/Documents/GitHub/AtlasTradeAI/src/atlas_trade_ai/services/intelligent_role_agent_service.py) 或 [`FollowUpAgent`](file:///Users/jinniu/Documents/GitHub/AtlasTradeAI/src/atlas_trade_ai/agent.py) 使用 [`OpenAIEnhancer`](file:///Users/jinniu/Documents/GitHub/AtlasTradeAI/src/atlas_trade_ai/llm.py) 调用大模型。

---

### 📋 **Agent 完整列表与大模型使用情况**

#### **1. 已配置为 Hybrid 模式（规则 + 大模型）的 Agent（9 个）**

这些 Agent **默认会尝试使用大模型**增强输出：

| # | Agent 名称 | Agent Key | 运行模式 | 智能类型 | 大模型用途 |
|---|-----------|-----------|---------|---------|-----------|
| 1 | **Sales Agent** | `sales_agent` | Hybrid | 商机推进 + 客户沟通建议 | 优化销售沟通建议与报价表达 |
| 2 | **CRM Agent** | `crm_agent` | Hybrid | 客户画像 + 分层提醒 | 生成客户画像总结和经营建议 |
| 3 | **Follow-up Agent** | `follow_up_agent` | Hybrid | 履约风险识别 + 任务编排 | 优化摘要、建议和通知表达 |
| 4 | **Logistics Agent** | `logistics_agent` | Hybrid | 交付时效判断 + 客户同步建议 | 生成客户同步话术和物流解释 |
| 5 | **Finance Agent** | `finance_agent` | Hybrid | 回款风险识别 + 催收建议 | 生成催收建议和财务沟通摘要 |
| 6 | **Customer Service Agent** | `customer_service_agent` | Hybrid | 投诉分流 + 服务闭环建议 | 生成回复建议和问题摘要 |
| 7 | **Document Intelligence Agent** | `document_intelligence_agent` | Hybrid | 单证理解 + 一致性校验建议 | 生成修正建议和单证说明 |
| 8 | **Operations Analyst Agent** | `operations_analyst_agent` | Hybrid | 经营诊断 + 复盘分析 | 生成经营报告摘要和诊断建议 |
| 9 | **Knowledge Agent** | `knowledge_agent` | Hybrid | 知识沉淀 + 经验归档 | 生成知识归纳和 SOP 总结 |

---

#### **2. 已配置为 Rules 模式（纯规则）的 Agent（2 个）**

这些 Agent **当前不使用大模型**，但具备随时启用的能力：

| # | Agent 名称 | Agent Key | 运行模式 | 智能类型 | 为什么不用大模型 |
|---|-----------|-----------|---------|---------|----------------|
| 1 | **Supply Chain Agent** | `supply_chain_agent` | Rules | 排产建议 + 产能风险识别 | 面对强结构化流程，需要明确状态边界和可审计性 |
| 2 | **Customs / Documentation Agent** | `customs_agent` | Rules | 单证校验 + 合规阻塞识别 | 需要明确的合规校验规则，结构性校验适合规则 |

---

### 🔧 **大模型调用机制**

#### **核心组件：OpenAIEnhancer**
位置：[`src/atlas_trade_ai/llm.py`](file:///Users/jinniu/Documents/GitHub/AtlasTradeAI/src/atlas_trade_ai/llm.py)

**配置环境变量：**
```bash
OPENAI_API_KEY=sk-...           # 必填，启用大模型的关键
OPENAI_BASE_URL=https://...     # 可选，默认 OpenAI 官方 API
ATLAS_AGENT_MODEL=gpt-5-mini    # 可选，默认使用 gpt-5-mini
```

**工作原理：**
1. 所有 Hybrid 模式的 Agent 在生成规则结果后，会调用 `_maybe_enhance()` 方法
2. 如果 `OPENAI_API_KEY` 已配置，则调用 OpenAI API 优化输出
3. 如果 API 调用失败，自动回退到纯规则结果，不会中断流程

---

### 📊 **大模型使用统计**

根据 [`AgentMonitorService`](file:///Users/jinniu/Documents/GitHub/AtlasTradeAI/src/atlas_trade_ai/services/agent_monitor_service.py) 的监控能力，你可以：

1. **查看每个 Agent 的大模型使用情况**
   - 在 `/api/agents/monitor` 接口中可以看到 `engine_providers` 字段
   - 显示最近 20 次运行中使用的引擎提供者（如 `openai`、`rule-engine`）

2. **追踪大模型调用成功率**
   - 每次 Agent 运行都会记录 `engine` 字段
   - 包含 `llm_used: true/false` 和 `provider` 信息

---

### 🎯 **大模型在 Agent 中的具体作用**

根据文档 [`intelligence-capabilities-and-agent-evolution.md`](file:///Users/jinniu/Documents/GitHub/AtlasTradeAI/docs/03-agent-architecture/intelligence-capabilities-and-agent-evolution.md)，大模型主要用于：

#### **✅ 适合大模型的职责**
- **优化表达能力**：让摘要、建议、通知更自然
- **生成沟通话术**：面向客户的钉钉/邮件模板
- **总结与诊断**：经营分析、客户画像、问题复盘
- **知识归纳**：SOP 沉淀、案例归档

#### **❌ 不适合大模型的职责**
- **风险判断**：由规则引擎保证稳定性和可审计性
- **状态流转**：需要明确的状态边界
- **任务结构生成**：需要确定性的输出格式

---

### 📈 **如何查看哪些 Agent 实际使用了大模型**

访问 Agent 监控中台：
- **UI 界面**：`/ui/agents.html`
- **API 接口**：`/api/agents/monitor`

在返回结果中查看：
```json
{
  "engine_providers": ["openai", "rule-engine"],  // 显示使用的引擎
  "execution_mode": "hybrid",                      // 运行模式
  "intelligence_type": "客户画像 + 分层提醒"        // 智能类型
}
```

---

### 💡 **关键结论**

✅ **所有 11 个 Agent 都具备大模型能力**  
✅ **9 个 Agent 配置为 Hybrid 模式（默认使用大模型）**  
✅ **2 个 Agent 配置为 Rules 模式（当前不使用，但可随时启用）**  
✅ **大模型调用失败时自动降级，不影响业务运行**  
✅ **可通过环境变量灵活控制大模型的使用**  

你的架构设计非常先进，采用了**"规则打底 + 大模型增强"**的混合模式，既保证了稳定性，又获得了大模型的表达能力！