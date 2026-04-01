# 跟单员 Agent 原型实现说明

## 1. 文档目的

本文档说明当前仓库中已经落下的第一版跟单员 Agent 原型实现。

## 2. 当前实现范围

当前原型是一个轻量、可运行的规则型 Agent，主要用于验证以下链路：

- 接收统一事件输入
- 组装订单、客户、履约、回款上下文
- 根据事件类型输出风险判断
- 生成任务草稿
- 生成异常标记
- 生成通知草稿

## 3. 代码位置

- [src/atlas_trade_ai/models.py](/Users/jinniu/Documents/GitHub/AtlasTradeAI/src/atlas_trade_ai/models.py)
- [src/atlas_trade_ai/rules.py](/Users/jinniu/Documents/GitHub/AtlasTradeAI/src/atlas_trade_ai/rules.py)
- [src/atlas_trade_ai/agent.py](/Users/jinniu/Documents/GitHub/AtlasTradeAI/src/atlas_trade_ai/agent.py)
- [src/atlas_trade_ai/cli.py](/Users/jinniu/Documents/GitHub/AtlasTradeAI/src/atlas_trade_ai/cli.py)
- [examples/followup_event.json](/Users/jinniu/Documents/GitHub/AtlasTradeAI/examples/followup_event.json)
- [tests/test_follow_up_agent.py](/Users/jinniu/Documents/GitHub/AtlasTradeAI/tests/test_follow_up_agent.py)

## 4. 当前支持的事件

当前原型优先支持：

- `production.milestone_delayed`
- `document.missing`
- `logistics.delayed`
- `payment.due_soon`
- `payment.overdue`
- 其他未显式支持的事件会进入通用跟进逻辑

## 5. 运行方式

在仓库根目录执行：

```bash
PYTHONPATH=src python -m atlas_trade_ai
```

该命令会读取示例文件并输出一份结构化结果。

## 6. 当前设计取舍

当前版本采用规则型实现，而不是直接接入大模型，主要原因是：

- 先验证事件驱动链路
- 先稳定输入输出协议
- 先验证任务 / 异常 / 通知落点
- 降低第一版实现复杂度

## 7. 下一步演进建议

后续可以按以下顺序迭代：

1. 增加更多事件类型
2. 引入事件到任务 / 异常的规则表
3. 增加上下文加载器与服务适配层
4. 用大模型替换或增强规则生成摘要和建议
5. 接入真实任务中心和钉钉通知

## 8. 文档结论

当前这版代码已经是 AtlasTradeAI 跟单员 Agent 的第一个可运行原型。

它还不是完整业务系统，但已经把前面文档里的“事件 -> Agent -> 任务 / 异常 / 通知”主链落成了代码骨架。
