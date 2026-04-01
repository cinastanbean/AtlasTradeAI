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
    B --> C["状态机校验：当前状态能否推进"]
    C --> D["判断是否阻塞"]
    D --> E["判断是否需要升级"]
    E --> F["决定下一责任 Agent"]
    F --> G["回写订单主视图"]
    G --> H["触发 Follow-up / Finance / Logistics 等 Agent"]
    H --> I["生成任务 / 异常 / 通知"]
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

## 6. 状态机与升级策略

当前增强后的 `Order Orchestrator` 已具备：

### 6.1 状态机校验

会检查：

- 当前事件是否允许从当前订单状态进入目标状态
- 当前状态到目标状态是否符合状态机定义

如果不允许：

- 保持原订单状态
- 记录非法流转原因
- 自动触发升级信号

### 6.2 升级策略

当前会综合判断：

- 事件是否属于阻塞型事件
- 是否为 `P1` 优先级
- 同类事件是否重复触发
- 当前订单未解决异常数是否过多
- 客户是否属于战略客户 / 重点客户

当前会产出：

- `escalation.level`
- `escalation.required`
- `escalation.reasons`
- `escalation.targets`
- `escalation.resolved_targets`
- `escalation.composite_signals`

### 6.3 升级对象解析

当前 `Order Orchestrator` 会根据组织目录解析升级对象：

- 将 Agent 级目标转换为具体用户
- 自动补充销售 owner
- 在 critical 情况下自动带上运营总监或中枢观察者

因此升级结果已经不只是“应该通知 Finance Agent”，而是会进一步变成具体的人和角色。

### 6.4 复合风险判断

当前已经支持部分多事件组合判断，例如：

- `production.milestone_delayed` + `document.missing`
- `logistics.delayed` + `payment.overdue`

这种情况下会产生 `composite_signals`，并直接进入更高的升级等级。

### 6.5 SLA 提示

每类编排规则当前都可配置：

- `sla_hours`

用于提示当前阶段应在多长时间内完成响应。

## 7. 当前输出结果

`Order Orchestrator` 当前会输出：

- `status_before`
- `status_after`
- `sub_status_before`
- `sub_status_after`
- `current_layer`
- `target_layer`
- `blocked`
- `sla_hours`
- `transition_allowed`
- `escalation`
- `next_owner_agent`
- `next_agents`
- `decision_summary`

并且：

- 会记录一条 `Order Orchestrator` 运行日志
- 会把最新编排结果回写到订单对象中
- 会在订单详情页和进度页中展示出来
- 会在工作台升级列表中聚合展示
- 会自动产生升级通知

## 8. 后续建议

下一阶段建议继续增强：

1. 让升级策略支持按组织角色路由到具体人和具体群
2. 让 Orchestrator 支持多事件合并判断
3. 引入历史上下文，让其具备更强的流程推理能力
4. 将部分策略开放为后台配置而不是本地 JSON
