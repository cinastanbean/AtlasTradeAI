# 钉钉真实接入说明

## 1. 当前接入模式

当前工程中的钉钉适配器已经支持三种模式：

- `mock`
  - 默认模式，使用本地伪数据
- `webhook`
  - 通过钉钉机器人 Webhook 发送通知
- `openapi`
  - 通过企业应用凭证调用钉钉开放平台接口

## 2. 当前代码位置

- [dingtalk.py](/Users/jinniu/Documents/GitHub/AtlasTradeAI/src/atlas_trade_ai/adapters/dingtalk.py)
- [notification_service.py](/Users/jinniu/Documents/GitHub/AtlasTradeAI/src/atlas_trade_ai/services/notification_service.py)
- [task_service.py](/Users/jinniu/Documents/GitHub/AtlasTradeAI/src/atlas_trade_ai/services/task_service.py)

## 3. 推荐接入顺序

建议按以下顺序接入真实钉钉：

1. 先接 `webhook`，打通通知链路
2. 再接 `openapi`，打通待办创建
3. 最后再补组织、审批、回执等深度能力

## 4. 当前支持的环境变量

### 基础模式

- `DINGTALK_MODE`
  - `mock` / `webhook` / `openapi`

### Webhook 模式

- `DINGTALK_WEBHOOK_URL`
- `DINGTALK_WEBHOOK_SECRET`

### OpenAPI 模式

- `DINGTALK_CLIENT_ID`
- `DINGTALK_CLIENT_SECRET`
- `DINGTALK_ACCESS_TOKEN_URL`
- `DINGTALK_TODO_CREATE_URL`

## 5. 当前实现说明

### 5.1 消息通知

当配置 `webhook` 或 `openapi + webhook` 时：

- 系统会将通知转为 Markdown 消息
- 自动附带订单号、摘要、升级级别等信息
- 若配置 `secret`，会自动生成签名

### 5.2 待办创建

当前任务服务在创建任务时，会尝试调用钉钉待办创建逻辑。

为了兼容不同企业接入方式，当前实现采用：

- Access Token URL 可配置
- Todo 创建 URL 可配置

这意味着你后面接真实企业应用时，只需要把正确的 URL 和凭证填进去，而不需要重写系统主逻辑。

## 6. 当前边界

当前版本已经具备真实接入骨架，但仍保留以下边界：

- 未内置企业专属待办字段映射
- 未完成真实用户 ID 与钉钉用户体系映射
- 未补审批回执、消息已读回执等深度能力

## 7. 官方参考

官方资料可参考：

- [钉钉开放平台教程中心](https://open.dingtalk.com/tutorial/)
- [钉钉开发者百科：获取 AccessToken](https://open-dingtalk.github.io/developerpedia/docs/learn/basics/authentication/)

说明：

- 由于钉钉开放平台文档和接口路径会演进，当前工程将核心 URL 做成可配置项，是为了降低后续升级成本。
