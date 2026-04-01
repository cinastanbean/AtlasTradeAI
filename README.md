# AtlasTradeAI

AtlasTradeAI 是一个以文档为核心的项目，用于设计面向贸易公司的智能经营操作系统与智能体层。

本仓库当前的主要产出不是业务代码，而是业务架构、流程设计、领域模型、系统蓝图、分阶段实施方案，以及相关的设计思考过程。

当前仓库也已经开始包含一版轻量的跟单员 Agent 原型代码，用于验证事件驱动链路和任务 / 异常 / 通知输出结构。
当前仓库已经进一步扩展为第一版工程骨架，包含 API 层、服务层、内存态数据层、事件处理链路和跟单员 Agent 接入示例。

## 仓库结构

- `docs/`
  - 项目的核心文档目录，用于存放架构方案、设计草稿、决策记录与规划材料。
- `src/`
  - 跟单员 Agent 原型与后续业务实现代码目录。
- `examples/`
  - 示例事件输入与演示数据。
- `tests/`
  - 原型代码的基础测试。
- `docs/00-overview/`
  - 项目定位、设计原则、总体说明等基础文档。
- `docs/01-business-architecture/`
  - 业务架构、端到端流程、业务域边界、经营协同模型等文档。
- `docs/02-system-architecture/`
  - 系统蓝图、模块拆分、集成架构、事件流设计等文档。
- `docs/03-agent-architecture/`
  - 智能体职责、触发机制、执行边界、Agent 工作流设计等文档。
- `docs/04-implementation-roadmap/`
  - 分阶段实施方案、MVP 范围、里程碑与交付路径等文档。

## 工作原则

- 以订单全生命周期为主线进行设计。
- 以文档驱动业务架构与系统架构设计。
- 将 AI 作为可控业务流程之上的增强层。
- 对关键操作保持可追溯、可审计、可人工接管。

## 当前阶段

项目的第一阶段目标是完成一家同时经营内销与外贸业务的贸易公司的业务架构设计，并在此基础上继续展开系统架构、智能体架构与 MVP 落地方案设计。

## 图示化表达

为了更直观地展示整体方案，后续文档将尽量使用以下方式表达设计内容：

- Mermaid 流程图
- Mermaid 模块关系图
- Mermaid 时序图
- 必要时补充独立图片资产

当前优先推荐使用 Markdown 内嵌 Mermaid，以便快速迭代和版本管理。

## 文档入口

完整文档索引见：

- [docs/00-overview/document-index.md](/Users/jinniu/Documents/GitHub/AtlasTradeAI/docs/00-overview/document-index.md)

## 工程运行

启动 API 服务：

```bash
PYTHONPATH=src uvicorn atlas_trade_ai.app:app --reload
```

运行跟单员 Agent 示例：

```bash
PYTHONPATH=src python -m atlas_trade_ai
```
