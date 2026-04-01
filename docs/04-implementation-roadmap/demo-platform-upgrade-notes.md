# Demo 平台升级说明

## 1. 升级目标

这一轮升级的目标，是把 AtlasTradeAI 从“可运行的工程骨架”推进到“可演示的完整系统框架”。

重点完成四件事：

- 扩充 Mock Adapter 数据，模拟纷享销客 CRM / 金蝶云星空 ERP / 钉钉
- 将内存仓库替换为 SQLite 演示数据库
- 将跟单员 Agent 升级为规则 + 大模型混合模式
- 将原单页演示页升级为多页面前端应用

## 2. 数据层升级

当前 Demo 已从 `InMemoryStore` 切换为 `SQLiteStore`。

### 当前实现

- 数据文件默认位于 `data/atlas_trade_ai_demo.sqlite`
- 启动容器时会自动重建并写入演示种子数据
- 已落库对象包括：
  - 客户
  - 订单
  - 任务
  - 异常
  - 事件
  - Agent 运行日志
  - 通知记录

### 当前价值

- 事件、任务、异常和通知不再只存在进程内存中
- 前端多个页面可以共享同一份持久化演示数据
- 后续切换 MySQL 时，可以沿用服务层结构

### 后续建议

- 第二阶段可以将 `SQLiteStore` 替换为 `MySQLStore`
- 表结构和字段建议继续参考：
  - [数据库表结构草案（字段级）](/Users/jinniu/Documents/GitHub/AtlasTradeAI/docs/02-system-architecture/database-schema-field-level-draft.md)

## 3. Mock 集成层升级

当前已经增加 `mock_integrations.json` 作为统一伪数据源。

### CRM Mock

- 客户列表
- 报价列表
- 跟进记录

### ERP Mock

- 订单列表
- 生产进度
- 回款信息
- 库存快照

### 钉钉 Mock

- 待办
- 消息发送记录
- 审批记录

### 当前价值

- 在不接真实系统的情况下，也可以完整展示跨系统的数据视图
- 可以验证各系统在 Demo 中的衔接关系
- 后续替换真实适配器时，可以保持接口不变

## 4. Agent 升级

当前跟单员 Agent 已从纯规则模式升级为“规则主导、LLM 可选增强”的混合模式。

### 当前逻辑

1. 先由规则引擎做稳定判断
2. 再由 LLM 对摘要、建议和通知文案做增强
3. 若未配置 `OPENAI_API_KEY` 或调用失败，则自动回退规则结果

### 当前价值

- 保证流程可控、结果稳定
- 同时保留更自然的表达能力
- 不会因为大模型不可用而阻塞演示链路

## 5. 前端应用升级

当前前端已从单页演示页升级为多页面应用，主要页面包括：

- `index.html`
  - 总览驾驶舱
- `orders.html`
  - 订单看板
- `agents.html`
  - Agent 目录与执行日志
- `integrations.html`
  - Mock 集成快照
- `order-detail.html`
  - 单订单详情与阶段进度

### 当前价值

- 可以从不同业务视角理解整个系统
- 可以直观看到订单当前走到哪个阶段
- 可以观察事件触发后任务、异常和 Agent 的执行结果

## 6. 当前入口

推荐直接打开：

- `http://127.0.0.1:8000/platform`
- `http://127.0.0.1:8000/ui/index.html`
- `http://127.0.0.1:8000/ui/orders.html`
- `http://127.0.0.1:8000/ui/agents.html`
- `http://127.0.0.1:8000/ui/integrations.html`

## 7. 后续演进建议

下一阶段建议按以下顺序继续推进：

1. 将 SQLite Demo 仓储切换到 MySQL
2. 将 Mock Adapter 替换为真实读取型 Adapter
3. 为更多角色 Agent 增加专属上下文和规则
4. 将前端升级为框架化工程并增加权限、筛选和图表能力

## 8. 最新补充

当前又进一步补上了 `Order Orchestrator` 的状态机与升级策略增强，包括：

- 合法流转校验
- 阻塞事件升级
- 重复事件升级
- 多异常升级
- 重点客户升级
- 复合事件升级
- 升级对象解析到具体用户
- 工作台升级列表
- 升级通知自动生成
