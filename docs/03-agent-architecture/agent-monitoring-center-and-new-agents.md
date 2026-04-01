# Agent 监控中台与新增 Agent 说明

## 1. 文档目的

本文档说明两件事：

- 当前系统中新增了哪些高价值 Agent
- `Agent 监控中台` 如何查看每个 Agent 的技能、运行模式和工作记录

## 2. 当前新增 Agent

在原有的 Sales / CRM / Follow-up / Supply Chain / Logistics / Customs / Finance / Customer Service 基础上，当前又新增了：

### 2.1 Document Intelligence Agent

职责：

- 单证抽取
- 单证比对
- 一致性检查
- 修正建议输出

适合模式：

- 规则 + 大模型混合

原因：

- 结构性校验适合规则
- 修正建议与说明适合大模型增强

### 2.2 Operations Analyst Agent

职责：

- 经营复盘
- 关键指标分析
- 风险诊断摘要
- 管理层视角建议

适合模式：

- 大模型增强为主

原因：

- 重点在总结、诊断和表达

### 2.3 Knowledge Agent

职责：

- 案例归档
- SOP 沉淀
- 知识复用建议

适合模式：

- 大模型增强为主

原因：

- 重点在知识提炼和归纳

## 3. 当前 Agent 监控中台

当前已经提供：

- `/ui/agents.html`
- `/api/agents/monitor`

这个页面更像一个监控中台，而不是简单的列表页。

### 当前能看到什么

- Agent 总数
- 活跃 Agent 数
- 最近运行记录
- 每个 Agent 的技能清单
- 每个 Agent 的运行模式
- 每个 Agent 的智能类型
- 每个 Agent 的订阅事件
- 每个 Agent 的最近执行
- 每个 Agent 的引擎来源

## 4. 当前监控价值

这套监控中台的价值在于：

- 能看出系统里到底有哪些 Agent
- 能看出每个 Agent 是做什么的
- 能看出每个 Agent 最近有没有真的在工作
- 能看出它主要是规则驱动还是大模型增强

## 5. 后续建议

后续可以继续增强：

1. 增加按 Agent 过滤执行日志
2. 增加每个 Agent 的成功率 / 平均响应时间
3. 增加每个 Agent 的输入输出样例查看
4. 增加按业务层分组的监控图表
