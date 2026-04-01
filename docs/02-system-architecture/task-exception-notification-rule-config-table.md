# 任务 / 异常 / 通知规则配置表

## 1. 文档目的

本文档用于把关键事件进一步映射为系统动作配置，明确：

- 什么事件会生成任务
- 什么事件会生成异常
- 什么事件会触发通知
- 对应由哪个 Agent 或模块处理

本文档可视为第一阶段规则引擎的业务配置草案。

## 2. 设计原则

规则配置建议遵循以下原则：

- 一条规则只解决一个清晰问题
- 事件触发后优先落到任务、异常、通知
- 高风险事件必须可升级
- 规则要可配置、可审计、可扩展

## 3. 规则字段说明

建议每条规则至少包含以下字段：

| 字段名 | 说明 |
| --- | --- |
| `rule_code` | 规则编码 |
| `event_type` | 触发事件类型 |
| `condition` | 触发条件 |
| `task_action` | 任务动作 |
| `exception_action` | 异常动作 |
| `notification_action` | 通知动作 |
| `subscriber` | 处理方 |
| `priority` | 规则优先级 |
| `enabled` | 是否启用 |

## 4. 第一阶段核心规则配置表

| rule_code | event_type | 触发条件 | 任务动作 | 异常动作 | 通知动作 | subscriber | priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R001` | `order.confirmed` | 订单正式确认 | 创建“订单跟进启动”任务 | 无 | 通知跟单员 | Follow-up Agent | P2 |
| `R002` | `production.milestone_delayed` | 任一关键生产里程碑超时 | 创建“确认工厂恢复时间”任务 | 创建交付异常 | 通知跟单员、销售 | Follow-up Agent | P1 |
| `R003` | `material.shortage` | 关键物料不足 | 创建“处理物料短缺”任务 | 创建供应风险异常 | 通知供应链负责人 | Supply Chain Agent | P1 |
| `R004` | `shipment.ready` | 发货条件达成 | 创建“安排发货与物流”任务 | 无 | 通知物流负责人 | Logistics Agent | P2 |
| `R005` | `shipment.dispatched` | 发货完成 | 创建“同步发货状态”任务 | 无 | 通知销售 / 跟单 | Logistics Agent | P3 |
| `R006` | `document.missing` | 缺失关键单证 | 创建“补齐单证资料”任务 | 创建单证异常 | 通知单证员、跟单员 | Customs / Documentation Agent | P1 |
| `R007` | `customs.rejected` | 报关被退回 | 创建“处理报关退单”任务 | 创建报关异常 | 通知单证负责人、跟单员 | Customs / Documentation Agent | P1 |
| `R008` | `logistics.delayed` | 物流节点超时 | 创建“确认物流延误原因”任务 | 创建物流异常 | 通知跟单员、销售 | Logistics Agent / Follow-up Agent | P2 |
| `R009` | `payment.due_soon` | 回款临近账期 | 创建“回款提醒”任务 | 无 | 通知销售、财务 | Finance Agent | P2 |
| `R010` | `payment.overdue` | 回款已逾期 | 创建“处理逾期回款”任务 | 创建回款异常 | 通知销售、财务负责人 | Finance Agent / Follow-up Agent | P1 |
| `R011` | `after_sales.complaint_created` | 客户投诉已登记 | 创建“处理客户投诉”任务 | 创建售后异常 | 通知客服负责人 | Customer Service Agent | P2 |
| `R012` | `after_sales.closed` | 售后闭环完成 | 创建“更新客户维护策略”任务 | 关闭售后异常 | 通知 CRM 负责人 | CRM Agent | P3 |

## 5. 规则动作拆解说明

### 5.1 任务动作

任务动作建议配置以下内容：

| 配置项 | 说明 |
| --- | --- |
| `task_title` | 任务标题 |
| `task_type` | 任务类型 |
| `assignee_role` | 责任角色 |
| `priority` | 任务优先级 |
| `due_time_rule` | 截止时间规则 |

例如：

- `production.milestone_delayed`
  - `task_title`: 确认工厂恢复时间
  - `assignee_role`: 跟单员
  - `priority`: high
  - `due_time_rule`: 2小时内

### 5.2 异常动作

异常动作建议配置以下内容：

| 配置项 | 说明 |
| --- | --- |
| `exception_type` | 异常类型 |
| `exception_level` | 异常等级 |
| `auto_create` | 是否自动创建 |
| `upgrade_rule` | 是否升级 |

### 5.3 通知动作

通知动作建议配置以下内容：

| 配置项 | 说明 |
| --- | --- |
| `channel` | 通知渠道 |
| `receiver_role` | 接收角色 |
| `template_code` | 通知模板 |
| `dedupe_window` | 去重时间窗 |

## 6. 建议通知模板映射

| 模板编码 | 适用事件 | 通知对象 | 内容重点 |
| --- | --- | --- | --- |
| `NTF_ORDER_START` | `order.confirmed` | 跟单员 | 订单开始跟进 |
| `NTF_PROD_DELAY` | `production.milestone_delayed` | 跟单员、销售 | 延期风险、恢复时间 |
| `NTF_DOC_MISSING` | `document.missing` | 单证员、跟单员 | 缺失项、截止时间 |
| `NTF_LOGI_DELAY` | `logistics.delayed` | 跟单员、销售 | 延误原因、预计到达 |
| `NTF_PAY_DUE` | `payment.due_soon` | 销售、财务 | 临期金额、账期日期 |
| `NTF_PAY_OVERDUE` | `payment.overdue` | 销售、财务负责人 | 逾期金额、逾期天数 |

## 7. 第一阶段建议启用的最小规则集

为了控制范围，建议第一阶段先启用以下规则：

- `R001`
- `R002`
- `R004`
- `R006`
- `R008`
- `R009`
- `R010`

这组规则已经足以跑通：

- 订单启动
- 生产延期
- 发货准备
- 单证缺失
- 物流延误
- 回款临期
- 回款逾期

## 8. 规则引擎落地建议

第一阶段不一定需要复杂规则平台，但建议规则配置至少具备：

- 编码化管理
- 可开关
- 可调整优先级
- 可追踪命中结果

后续可以逐步演进成：

- 数据库配置表
- 后台管理界面
- 多条件组合规则

## 9. 规则与 Agent 的关系

规则引擎和 Agent 不应互相替代，而应分工明确。

建议关系如下：

- 规则引擎负责确定“是否触发动作”
- Agent 负责生成“更智能的动作内容”

例如：

- 规则决定创建一条“处理逾期回款”任务
- Finance Agent 或 Follow-up Agent 再补充任务摘要、催收建议和通知文案

## 10. 文档结论

任务 / 异常 / 通知规则配置表，是 AtlasTradeAI 从事件系统走向自动流转系统的关键一步。

它能把抽象的事件逻辑，转成系统里真正可执行的动作配置。
