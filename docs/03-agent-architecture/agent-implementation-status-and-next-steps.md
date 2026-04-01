# Agent 实现现状与下一步清单

## 1. 当前已实现 Agent

当前工程中已经具备以下可执行 Agent：

- Sales Agent
- CRM Agent
- Follow-up Agent
- Supply Chain Agent
- Logistics Agent
- Customs / Documentation Agent
- Finance Agent
- Customer Service Agent

## 2. 当前实现形态

### 已具备规则 + 大模型混合能力

- Follow-up Agent
- Sales Agent
- CRM Agent
- Logistics Agent
- Finance Agent
- Customer Service Agent

### 当前以规则为主

- Supply Chain Agent
- Customs / Documentation Agent

## 3. 当前已落地的关键事件

- `quotation.accepted`
- `order.confirmed`
- `production.milestone_delayed`
- `document.missing`
- `customs.rejected`
- `logistics.delayed`
- `payment.due_soon`
- `payment.overdue`
- `after_sales.complaint_created`

## 4. 建议下一步优先级

建议后续按如下顺序继续增强：

1. 增加 `Order Orchestrator` 中枢编排层
2. 增加 `Document Intelligence Agent`
3. 增加 `Operations Analyst Agent`
4. 增加 `Knowledge Agent`
5. 为更多 Agent 提供专属上下文和历史知识注入
