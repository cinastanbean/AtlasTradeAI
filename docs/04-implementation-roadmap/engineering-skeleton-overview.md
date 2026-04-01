# 第一版工程骨架说明

## 1. 文档目的

本文档说明当前仓库中已经落下的第一版工程骨架，用于帮助从设计文档过渡到真正的代码工程理解。

## 2. 当前工程目标

这一版工程骨架的目标不是把所有底层实现做完，而是把整个系统的结构跑出来，让你可以从代码层直观看到：

- 系统如何分层
- 各模块如何组织
- API 如何暴露
- 事件如何流转
- 跟单员 Agent 如何接入

## 3. 当前工程结构

```text
src/atlas_trade_ai/
  api/
    router.py
    routes/
  adapters/
    CRM / ERP / DingTalk Mock 适配器
  core/
    bootstrap.py
    store.py
    config_loader.py
  schemas/
    common.py
    customer.py
    order.py
    task.py
    exception.py
    event.py
    agent.py
    notification.py
    dashboard.py
    demo.py
    agent_run.py
  services/
    customer_service.py
    order_service.py
    task_service.py
    exception_service.py
    event_service.py
    notification_service.py
    agent_service.py
    overview_service.py
    workflow_service.py
    rule_registry_service.py
    context_builder_service.py
    integration_service.py
    workbench_service.py
    dashboard_service.py
    demo_scenario_service.py
    agent_run_service.py
  agent.py
  llm.py
  models.py
  rules.py
  app.py
  container.py
  web/
    platform.html
  webapp/
    index.html
    orders.html
    agents.html
    integrations.html
    order-detail.html
    assets/
```

## 4. 当前分层说明

### 4.1 API 层

负责暴露系统接口。

当前已包含：

- 客户接口
- 订单接口
- 任务接口
- 异常接口
- 事件接口
- 跟单员 Agent 接口
- 通知接口
- 架构总览接口
- 工作台接口
- Agent 运行日志接口
- Demo 场景接口
- 集成状态接口
- 规则配置接口
- 订单作战视图接口

### 4.2 Service 层

负责承接核心业务逻辑。

当前已包含：

- CustomerService
- OrderService
- TaskService
- ExceptionService
- EventService
- NotificationService
- FollowUpAgentService

### 4.3 Core / Infrastructure 层

负责提供当前版本的基础设施能力。

当前使用：

- `SQLiteStore`
- `bootstrap` 种子数据
- `config_loader` JSON 配置加载

这一层后续可以进一步替换成 MySQL / PostgreSQL、消息总线和真实系统适配器。

### 4.4 Agent 层

当前已经把第一版跟单员 Agent 接入到工程骨架中，并增强为规则 + 大模型混合模式。

当前结构是：

- `models.py` 负责 Agent 输入输出上下文
- `rules.py` 负责规则型判断
- `agent.py` 负责混合模式执行入口
- `llm.py` 负责可选的大模型增强
- `agent_service.py` 负责在系统服务层接入 Agent

### 4.5 Workflow / Orchestration 层

当前新增了：

- `RuleRegistryService`
- `ContextBuilderService`
- `WorkflowService`

这一层负责把事件、规则、上下文构建和 Agent 执行串成一条主链。

## 5. 当前已实现的系统闭环

当前骨架已经跑通：

- API 接收事件
- 事件写入事件服务
- 事件服务根据订单上下文调用跟单员 Agent
- 跟单员 Agent 生成任务草稿、异常标记和通知草稿
- 系统将结果落到任务中心、异常中心和通知中心

当前还新增了：

- 配置化规则加载
- Agent 运行日志记录
- Demo 场景回放
- 工作台汇总与订单作战视图接口
- Mock 集成层数据接口
- 多页面前端应用
- SQLite 演示数据库

## 6. 运行方式

启动 API 服务：

```bash
PYTHONPATH=src uvicorn atlas_trade_ai.app:app --reload
```

运行跟单员 Agent CLI 示例：

```bash
PYTHONPATH=src python -m atlas_trade_ai
```

运行测试：

```bash
PYTHONPATH=src python -m pytest -q
```

## 7. 当前实现边界

当前版本有意保持轻量，主要限制包括：

- 数据库存储当前为 SQLite Demo 版
- 未接入真实 CRM / ERP / 钉钉，仅提供 Mock 适配器
- 规则配置当前基于本地 JSON
- 大模型能力为可选增强，默认可安全回退到规则结果
- 前端当前仍是轻量原生应用，而不是生产级前端工程

但它已经足够用来帮助理解：

- 整个项目的代码结构
- 各模块之间的关系
- 事件驱动的处理链路

## 8. 后续演进建议

后续建议按以下顺序演进：

1. 将 SQLite 演示仓储迁移到 MySQL 仓储
2. 引入真实集成适配层，对接 CRM / ERP / 钉钉
3. 将前端原生应用升级到框架化前端工程
4. 用大模型增强更多角色 Agent 输出
5. 增加更多业务 Agent 和模块

## 9. 文档结论

当前这版工程骨架，已经把设计文档中的核心结构正式转成了代码框架。

它的价值不是底层能力有多完整，而是已经把整个智能贸易操作系统的骨架形态呈现出来了。
