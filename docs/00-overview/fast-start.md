# Fast Start

## 1. 目标

这份文档帮助你在最短时间内跑起 AtlasTradeAI 当前这版工程骨架，并快速理解这个智能贸易操作系统如何运行。

## 2. 当前你能得到什么

当前仓库已经具备：

- 完整的架构设计文档体系
- 第一版可运行后端骨架
- SQLite 演示数据库
- Mock CRM / ERP / 钉钉 集成快照
- 跟单员 Agent 的规则 + 大模型混合模式
- 事件 -> 任务 / 异常 / 通知 的演示链路
- 多页面前端应用

这意味着你现在可以：

- 直接启动系统看整体结构
- 从接口层理解模块关系
- 从代码层理解事件和 Agent 如何协同
- 在演示平台上观察多 Agent 如何围绕订单协同

## 3. 启动方式

在仓库根目录执行：

```bash
PYTHONPATH=src uvicorn atlas_trade_ai.app:app --reload
```

启动后可以访问：

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/demo`
- `http://127.0.0.1:8000/platform`
- `http://127.0.0.1:8000/app`
- `http://127.0.0.1:8000/ui/index.html`
- `http://127.0.0.1:8000/docs`

## 4. 建议的第一轮查看路径

建议按这个顺序看：

1. 打开 `/platform` 或 `/ui/index.html`
2. 打开 `/docs` 看 OpenAPI
3. 调用 `/api/overview/architecture`
4. 调用 `/api/workbench/summary`
5. 查看 `/api/agents/catalog`
6. 查看 `/api/orders`
7. 查看 `/api/orders/{id}/progress`
8. 查看 `/api/orders/{id}/orchestration`
9. 查看 `/api/demo/scenarios`
10. 运行一个 Demo 场景
11. 再查看 `/api/tasks`、`/api/exceptions`、`/api/agent-runs`

## 5. 关键接口

### 架构与总览

- `GET /api/overview/architecture`
- `GET /api/workbench/summary`
- `GET /api/workbench/escalations`
- `GET /api/workbench/sla-overdue`
- `GET /api/dashboard/orders/{id}`

### 业务主线

- `GET /api/customers`
- `GET /api/orders`
- `GET /api/orders/{id}`
- `GET /api/orders/{id}/progress`
- `GET /api/orders/{id}/orchestration`

### 事件驱动

- `POST /api/events`
- `GET /api/events`
- `GET /api/demo/scenarios`
- `POST /api/demo/scenarios/{code}/run`

### 承接动作

- `GET /api/tasks`
- `GET /api/tasks/owners`
- `POST /api/tasks`
- `POST /api/tasks/{task_id}/status`
- `GET /api/exceptions`
- `POST /api/exceptions`

### Agent

- `POST /api/agents/follow-up/run`
- `GET /api/agent-runs`
- `GET /api/agent-runs/{run_id}`
- `GET /api/agents/catalog`
- `GET /api/agents/monitor`

### 配置与集成

- `GET /api/rules/events`
- `GET /api/rules/workflow`
- `GET /api/integrations`
- `GET /api/integrations/crm`
- `GET /api/integrations/erp`
- `GET /api/integrations/dingtalk`
- `GET /api/demo/scenarios`
- `POST /api/demo/scenarios/{code}/run`

## 6. 最关键的演示链路

你最应该先理解的是这条链路：

1. 平台中已经存在几张演示订单
2. 在 `/platform` 里运行一个 Demo 场景，或向 `/api/events` 写入一个关键事件
3. 系统命中工作流规则
4. 调用跟单员 Agent
5. 自动生成任务、异常和通知
6. 在工作台、订单作战页和 Agent 日志中观察结果

你还可以直接观察：

- 哪些 Agent 被触发
- 订单当前处于哪一个阶段
- 当前阶段属于哪个业务层
- 下一步将由哪个 Agent 接管

这条链路就是 AtlasTradeAI 第一阶段最核心的“智能操作系统”演示。

## 7. 示例事件

可直接使用类似下面的事件：

```json
{
  "event_type": "production.milestone_delayed",
  "event_time": "2026-04-01T10:30:00+08:00",
  "source_system": "kingdee_k3cloud",
  "biz_object_type": "order",
  "biz_object_id": "ord_001",
  "order_id": "ord_001",
  "customer_id": "cus_001",
  "priority": "P1",
  "payload": {
    "milestone_type": "生产完成",
    "delay_days": 2
  }
}
```

## 8. 运行测试

执行：

```bash
PYTHONPATH=src python -m pytest -q
```

## 9. 当前工程边界

当前版本重点是“结构完整、链路清晰、方便理解”，因此：

- 当前数据库为 SQLite Demo 版，便于零成本启动
- 外部系统适配器为 Mock 版，便于完整展示 CRM / ERP / 钉钉 的数据流
- 规则配置已改为 JSON 文件方式提供
- 跟单员 Agent 已支持规则 + 大模型混合模式，但默认会在未配置 `OPENAI_API_KEY` 时自动回退规则引擎
- 前端当前为原生多页面应用，便于清晰展示各业务视角

这仍然是有意为之，因为当前阶段目标是先把整个系统的框架和运行方式看清楚，同时保留后续切换到 MySQL 与真实系统适配器的空间。

## 10. 接下来建议你怎么用它

如果你的目标是理解整个项目，我建议你按这三层去看：

### 第一层：系统结构

看：

- `/platform`
- `/ui/orders.html`
- `/ui/tasks.html`
- `/ui/agents.html`
- `/ui/integrations.html`
- `/api/agents/monitor`
- `/api/workbench/escalations`
- `/api/workbench/sla-overdue`
- `/api/overview/architecture`
- `/api/agents/catalog`
- [第一版工程骨架说明](/Users/jinniu/Documents/GitHub/AtlasTradeAI/docs/04-implementation-roadmap/engineering-skeleton-overview.md)

### 第二层：事件和规则

看：

- `/api/rules/events`
- `/api/rules/workflow`
- `/api/demo/scenarios`
- `/api/orders/ord_001/progress`
- [事件目录与事件字段清单](/Users/jinniu/Documents/GitHub/AtlasTradeAI/docs/02-system-architecture/event-catalog-and-field-specification.md)
- [任务 / 异常 / 通知规则配置表](/Users/jinniu/Documents/GitHub/AtlasTradeAI/docs/02-system-architecture/task-exception-notification-rule-config-table.md)

### 第三层：代码骨架

看：

- `src/atlas_trade_ai/api/`
- `src/atlas_trade_ai/services/`
- `src/atlas_trade_ai/core/`
- `src/atlas_trade_ai/agent.py`
- `src/atlas_trade_ai/rules.py`

## 11. 文档结论

当前这版 Fast Start 的目的，不是教你如何完成所有底层实现，而是帮助你快速进入这个项目，看到：

- 系统是什么
- 模块怎么分
- 事件怎么跑
- Agent 怎么接
- 整个智能贸易操作系统如何开始工作
