# Order Orchestrator 设计说明

## 1. 角色定义

`Order Orchestrator` 不是普通业务 Agent，而是订单中枢的编排控制层。

它的职责不是代替 Sales、Follow-up、Finance 等角色执行具体工作，而是：

- 判断订单当前应该处于哪个阶段
- 决定当前事件是否会推动阶段变化
- 判断当前订单是否进入阻塞态
- 决定下一跳应该由哪个 Agent 接管
- 将中枢决策回写到订单主视图

## 2. 为什么它最有价值

如果没有 `Order Orchestrator`，系统虽然有多个 Agent，但更像是“多个独立处理器”。

有了 `Order Orchestrator` 以后，系统才会更像真正的智能操作系统：

- 所有关键事件先进入订单中枢
- 中枢先做阶段决策
- 再分发给后续业务 Agent
- 最后把执行结果回写订单看板

这意味着系统开始具备真正的自动流转能力。

## 3. 当前实现方式

当前实现位于：

- [order_orchestrator_service.py](/Users/jinniu/Documents/GitHub/AtlasTradeAI/src/atlas_trade_ai/services/order_orchestrator_service.py)
- [order_orchestration_rules.json](/Users/jinniu/Documents/GitHub/AtlasTradeAI/config/order_orchestration_rules.json)

当前采用“规则编排”为主，原因是：

- 订单状态机必须稳定
- 阶段推进必须可审计
- 编排结果必须可回放

## 4. 当前编排流程

```mermaid
flowchart LR
    A["业务事件进入"] --> B["Order Orchestrator"]
    B --> C["判断订单阶段是否变化"]
    C --> D["判断是否阻塞"]
    D --> E["决定下一责任 Agent"]
    E --> F["回写订单主视图"]
    F --> G["触发 Follow-up / Finance / Logistics 等 Agent"]
    G --> H["生成任务 / 异常 / 通知"]
```

## 5. 当前已覆盖的关键事件

- `quotation.accepted`
- `order.confirmed`
- `production.milestone_delayed`
- `shipment.ready`
- `shipment.dispatched`
- `document.missing`
- `customs.rejected`
- `logistics.delayed`
- `payment.due_soon`
- `payment.overdue`
- `after_sales.complaint_created`

## 6. 当前输出结果

`Order Orchestrator` 当前会输出：

- `status_before`
- `status_after`
- `sub_status_before`
- `sub_status_after`
- `current_layer`
- `target_layer`
- `blocked`
- `next_owner_agent`
- `next_agents`
- `decision_summary`

并且：

- 会记录一条 `Order Orchestrator` 运行日志
- 会把最新编排结果回写到订单对象中
- 会在订单详情页和进度页中展示出来

## 7. 后续建议

下一阶段建议继续增强：

1. 将编排规则从静态映射提升为“状态机 + 条件判断”
2. 引入 SLA、优先级和升级策略
3. 让 Orchestrator 支持多事件合并判断
4. 引入历史上下文，让其具备更强的流程推理能力
