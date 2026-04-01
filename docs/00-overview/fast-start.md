# Fast Start

## 1. 目标

这份文档帮助你在最短时间内跑起 AtlasTradeAI 当前这版工程骨架，并快速理解这个智能贸易操作系统如何运行。

## 2. 当前你能得到什么

当前仓库已经具备：

- 完整的架构设计文档体系
- 第一版可运行后端骨架
- 跟单员 Agent 原型
- 事件 -> 任务 / 异常 / 通知 的演示链路
- API 接口与演示页

这意味着你现在可以：

- 直接启动系统看整体结构
- 从接口层理解模块关系
- 从代码层理解事件和 Agent 如何协同

## 3. 启动方式

在仓库根目录执行：

```bash
PYTHONPATH=src uvicorn atlas_trade_ai.app:app --reload
```

启动后可以访问：

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/demo`
- `http://127.0.0.1:8000/docs`

## 4. 建议的第一轮查看路径

建议按这个顺序看：

1. 打开 `/demo`
2. 打开 `/docs` 看 OpenAPI
3. 调用 `/api/overview/architecture`
4. 调用 `/api/workbench/summary`
5. 查看 `/api/orders`
6. 向 `/api/events` 写入事件
7. 再查看 `/api/tasks` 和 `/api/exceptions`

## 5. 关键接口

### 架构与总览

- `GET /api/overview/architecture`
- `GET /api/workbench/summary`

### 业务主线

- `GET /api/customers`
- `GET /api/orders`
- `GET /api/orders/{id}`

### 事件驱动

- `POST /api/events`
- `GET /api/events`

### 承接动作

- `GET /api/tasks`
- `POST /api/tasks`
- `GET /api/exceptions`
- `POST /api/exceptions`

### Agent

- `POST /api/agents/follow-up/run`

### 配置与集成

- `GET /api/rules/events`
- `GET /api/rules/workflow`
- `GET /api/integrations`

## 6. 最关键的演示链路

你最应该先理解的是这条链路：

1. 订单已经存在于系统中
2. 向 `/api/events` 写入一个关键事件
3. 系统命中工作流规则
4. 调用跟单员 Agent
5. 自动生成任务、异常和通知

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

- 底层数据库还未接入
- 外部系统适配器仍是占位
- 规则配置先以 JSON 文件方式提供
- Agent 仍以规则型实现为主

这是有意为之，因为当前阶段目标是先把整个系统的框架和运行方式看清楚。

## 10. 接下来建议你怎么用它

如果你的目标是理解整个项目，我建议你按这三层去看：

### 第一层：系统结构

看：

- `/demo`
- `/api/overview/architecture`
- [第一版工程骨架说明](/Users/jinniu/Documents/GitHub/AtlasTradeAI/docs/04-implementation-roadmap/engineering-skeleton-overview.md)

### 第二层：事件和规则

看：

- `/api/rules/events`
- `/api/rules/workflow`
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
