# 事件目录与事件字段清单

## 1. 文档目的

本文档用于定义 AtlasTradeAI 第一阶段建议落地的标准事件目录，以及每类事件应携带的字段规范。

本文档的目标是把前面的“统一事件模型”和“层间事件触发矩阵”进一步收敛成可实现的事件清单。

## 2. 设计原则

事件目录设计建议遵循以下原则：

- 事件命名统一
- 事件字段统一
- 事件按业务域分层管理
- 优先覆盖第一阶段高价值场景
- 支持任务、异常、通知和 Agent 直接消费

## 3. 事件命名规范

建议统一采用：

- `对象.动作`

例如：

- `order.confirmed`
- `shipment.dispatched`
- `payment.overdue`

对于风险和升级事件，建议采用：

- `risk.风险名`
- `followup.动作`
- `escalation.动作`

例如：

- `risk.delivery_delay`
- `followup.required`
- `escalation.payment_overdue`

## 4. 事件基础字段清单

所有标准事件建议统一包含以下字段：

| 字段名 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| `event_id` | string | 是 | 事件唯一 ID |
| `event_type` | string | 是 | 事件类型 |
| `event_time` | string | 是 | 事件发生时间 |
| `source_system` | string | 是 | 来源系统 |
| `source_record_id` | string | 否 | 来源记录 ID |
| `biz_object_type` | string | 是 | 业务对象类型 |
| `biz_object_id` | string | 是 | 业务对象 ID |
| `order_id` | string | 否 | 关联订单 ID |
| `customer_id` | string | 否 | 关联客户 ID |
| `owner_id` | string | 否 | 当前责任人 |
| `status_before` | string | 否 | 变化前状态 |
| `status_after` | string | 否 | 变化后状态 |
| `priority` | string | 否 | 事件优先级 |
| `risk_level` | string | 否 | 风险等级 |
| `payload` | object | 否 | 扩展业务字段 |
| `trace_id` | string | 否 | 链路追踪 ID |

## 5. 第一阶段事件目录总览

第一阶段建议优先支持以下事件。

### 5.1 客户经营层事件

| 事件类型 | 说明 | 主要触发源 |
| --- | --- | --- |
| `customer.created` | 新客户创建 | CRM |
| `customer.updated` | 客户信息更新 | CRM |
| `quotation.sent` | 报价已发送 | CRM / 报价中心 |
| `quotation.accepted` | 报价被客户接受 | CRM / 销售确认 |
| `order.confirm_request` | 销售确认准备下单 | 销售动作 |

### 5.2 订单中枢层事件

| 事件类型 | 说明 | 主要触发源 |
| --- | --- | --- |
| `order.created` | 订单创建 | 订单中心 |
| `order.confirmed` | 订单正式确认 | 订单中心 |
| `order.status_changed` | 订单状态变化 | 状态机 |
| `order.execution_ready` | 订单具备执行条件 | 订单中心 / 状态机 |
| `order.closed` | 订单关闭 | 订单中心 |

### 5.3 履约推进层事件

| 事件类型 | 说明 | 主要触发源 |
| --- | --- | --- |
| `followup.execution_started` | 跟单接管订单 | Follow-up Agent / 任务中心 |
| `followup.required` | 订单需要重点跟进 | 规则引擎 / Agent |
| `task.created` | 跟进任务创建 | 任务中心 |
| `exception.created` | 异常创建 | 异常中心 |

### 5.4 供应链执行层事件

| 事件类型 | 说明 | 主要触发源 |
| --- | --- | --- |
| `procurement.created` | 采购创建 | ERP / 供应链中心 |
| `production.started` | 生产开始 | ERP / 工厂反馈 |
| `production.milestone_delayed` | 生产节点延期 | ERP / 规则引擎 |
| `material.shortage` | 物料短缺 | ERP / 供应链中心 |
| `shipment.ready` | 具备发货条件 | 供应链中心 |

### 5.5 交付与合规层事件

| 事件类型 | 说明 | 主要触发源 |
| --- | --- | --- |
| `shipment.dispatched` | 发货完成 | ERP / 物流中心 |
| `logistics.in_transit` | 物流在途 | 物流系统 |
| `logistics.delayed` | 物流延误 | 物流系统 / 规则引擎 |
| `document.missing` | 单证缺失 | 单证中心 |
| `document.validated` | 单证校验通过 | 单证中心 |
| `customs.submitted` | 报关提交 | 报关流程 |
| `customs.rejected` | 报关被退回 | 报关流程 |
| `delivery.completed` | 交付完成 | 物流 / 客户确认 |

### 5.6 资金结算层事件

| 事件类型 | 说明 | 主要触发源 |
| --- | --- | --- |
| `invoice.created` | 开票记录创建 | ERP / 财务系统 |
| `payment.due_soon` | 回款临期 | 规则引擎 |
| `payment.received` | 回款到账 | ERP / 财务系统 |
| `payment.overdue` | 回款逾期 | 规则引擎 |
| `payment.completed` | 回款完成 | 财务系统 |

### 5.7 售后服务层事件

| 事件类型 | 说明 | 主要触发源 |
| --- | --- | --- |
| `after_sales.created` | 售后问题创建 | 售后中心 |
| `after_sales.complaint_created` | 投诉创建 | 客服 / 客户反馈 |
| `after_sales.closed` | 售后闭环完成 | 售后中心 |

## 6. 关键事件字段示例

### 6.1 `order.confirmed`

建议附加字段：

| 字段名 | 说明 |
| --- | --- |
| `order_no` | 订单编号 |
| `business_type` | 内销 / 外贸 |
| `confirmed_time` | 确认时间 |
| `planned_delivery_date` | 计划交期 |
| `total_amount` | 订单金额 |
| `currency` | 币种 |

### 6.2 `production.milestone_delayed`

建议附加字段：

| 字段名 | 说明 |
| --- | --- |
| `milestone_type` | 延期里程碑类型 |
| `planned_time` | 原计划时间 |
| `delay_days` | 延期天数 |
| `factory_name` | 工厂名称 |
| `impact_scope` | 影响范围 |

### 6.3 `document.missing`

建议附加字段：

| 字段名 | 说明 |
| --- | --- |
| `document_type` | 单证类型 |
| `missing_items` | 缺失项列表 |
| `deadline` | 补齐截止时间 |

### 6.4 `payment.overdue`

建议附加字段：

| 字段名 | 说明 |
| --- | --- |
| `due_date` | 应回款日期 |
| `overdue_days` | 逾期天数 |
| `receivable_amount` | 应收金额 |
| `received_amount` | 已收金额 |

## 7. 事件优先级建议

建议统一使用四级优先级：

| 优先级 | 说明 | 典型事件 |
| --- | --- | --- |
| `P1` | 重大阻塞 / 高风险 | `customs.rejected`、`payment.overdue` |
| `P2` | 高优先异常 | `production.milestone_delayed`、`document.missing` |
| `P3` | 常规流程事件 | `order.confirmed`、`shipment.dispatched` |
| `P4` | 记录性事件 | `customer.updated`、`invoice.created` |

## 8. 第一阶段建议实现的最小事件包

为了控制实现范围，建议第一阶段至少落以下 10 个事件：

1. `quotation.accepted`
2. `order.confirmed`
3. `order.status_changed`
4. `production.milestone_delayed`
5. `shipment.ready`
6. `shipment.dispatched`
7. `document.missing`
8. `logistics.delayed`
9. `payment.due_soon`
10. `payment.overdue`

## 9. 事件字段校验建议

第一阶段建议至少做以下校验：

- `event_id` 不可为空
- `event_type` 必须在事件目录中
- `event_time` 必须合法
- `biz_object_type` 和 `biz_object_id` 必须成对出现
- 关键事件必须带 `order_id`

## 10. 文档结论

事件目录与字段清单，是后续事件总线、规则引擎、任务中心、异常中心和跟单员 Agent 落地的基础配置文档。

只有事件目录稳定，系统自动流转机制才会稳定。
