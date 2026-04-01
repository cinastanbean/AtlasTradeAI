# API 请求 / 响应样例清单

## 1. 文档目的

本文档用于定义 AtlasTradeAI 第一阶段核心接口的请求与响应样例，作为后续前后端联调、服务拆分和接口实现的参考。

本文档重点覆盖：

- 订单主线相关接口
- 任务与异常相关接口
- 事件写入与查询接口
- 跟单员 Agent 调用接口

## 2. 设计原则

第一阶段接口设计建议遵循以下原则：

- 优先围绕订单主线设计
- 接口返回结构统一
- 支持前端直接消费
- 支持事件系统和 Agent 编排层调用

## 3. 统一响应结构建议

建议所有接口统一返回：

```json
{
  "code": 0,
  "message": "ok",
  "data": {}
}
```

列表接口可扩展：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "items": [],
    "total": 0,
    "page": 1,
    "page_size": 20
  }
}
```

## 4. 客户中心接口样例

### 4.1 查询客户列表

`GET /api/customers?page=1&page_size=20&keyword=华东`

响应样例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "items": [
      {
        "customer_id": "cus_001",
        "customer_name": "华东重点客户A",
        "customer_level": "重点客户",
        "business_type": "内销",
        "owner_id": "user_sales_01"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 20
  }
}
```

### 4.2 查询客户详情

`GET /api/customers/cus_001`

响应样例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "customer_id": "cus_001",
    "customer_name": "华东重点客户A",
    "customer_level": "重点客户",
    "business_type": "内销",
    "country_or_region": "中国",
    "payment_terms": "月结30天",
    "contacts": [
      {
        "contact_id": "ct_001",
        "contact_name": "张三",
        "phone": "13800000000"
      }
    ]
  }
}
```

## 5. 订单中心接口样例

### 5.1 查询订单列表

`GET /api/orders?page=1&page_size=20&status=执行中`

响应样例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "items": [
      {
        "order_id": "ord_001",
        "order_no": "SO-2026-0001",
        "customer_name": "华东重点客户A",
        "current_status": "执行中",
        "sub_status": "生产中",
        "risk_level": "medium",
        "planned_delivery_date": "2026-04-10"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 20
  }
}
```

### 5.2 查询订单详情

`GET /api/orders/ord_001`

响应样例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "order_id": "ord_001",
    "order_no": "SO-2026-0001",
    "customer_id": "cus_001",
    "customer_name": "华东重点客户A",
    "business_type": "内销",
    "current_status": "执行中",
    "sub_status": "生产中",
    "risk_level": "medium",
    "planned_delivery_date": "2026-04-10",
    "payment_status": "待回款",
    "milestones": [
      {
        "milestone_type": "生产完成",
        "planned_time": "2026-04-05T18:00:00+08:00",
        "actual_time": null,
        "milestone_status": "delayed",
        "is_overdue": true
      }
    ]
  }
}
```

### 5.3 更新订单状态

`POST /api/orders/ord_001/status`

请求样例：

```json
{
  "status_after": "待发货",
  "sub_status": "待出库",
  "operator": "user_followup_01",
  "reason": "生产完成并通过验货"
}
```

响应样例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "order_id": "ord_001",
    "status_before": "执行中",
    "status_after": "待发货",
    "sub_status": "待出库"
  }
}
```

## 6. 任务中心接口样例

### 6.1 创建任务

`POST /api/tasks`

请求样例：

```json
{
  "task_type": "followup",
  "task_title": "确认工厂恢复时间",
  "task_description": "生产里程碑超时，需要确认最新恢复时间",
  "related_order_id": "ord_001",
  "assignee_id": "user_followup_01",
  "priority": "high",
  "due_time": "2026-04-01T14:00:00+08:00"
}
```

响应样例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "task_id": "task_001",
    "task_status": "待处理"
  }
}
```

### 6.2 查询我的任务

`GET /api/tasks?assignee_id=user_followup_01&status=待处理`

响应样例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "items": [
      {
        "task_id": "task_001",
        "task_title": "确认工厂恢复时间",
        "priority": "high",
        "task_status": "待处理",
        "related_order_id": "ord_001"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 20
  }
}
```

## 7. 异常中心接口样例

### 7.1 创建异常

`POST /api/exceptions`

请求样例：

```json
{
  "exception_type": "交付异常",
  "exception_level": "P1",
  "related_order_id": "ord_001",
  "source_event_id": "evt_001",
  "owner_id": "user_followup_01",
  "suggestion": "确认工厂恢复时间并评估交期影响"
}
```

响应样例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "exception_id": "ex_001",
    "exception_status": "已发现"
  }
}
```

### 7.2 查询异常列表

`GET /api/exceptions?level=P1&status=处理中`

响应样例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "items": [
      {
        "exception_id": "ex_001",
        "exception_type": "交付异常",
        "exception_level": "P1",
        "related_order_id": "ord_001",
        "exception_status": "处理中"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 20
  }
}
```

## 8. 事件中心接口样例

### 8.1 写入标准事件

`POST /api/events`

请求样例：

```json
{
  "event_id": "evt_001",
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

响应样例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "event_id": "evt_001",
    "accepted": true
  }
}
```

### 8.2 查询事件列表

`GET /api/events?order_id=ord_001`

响应样例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "items": [
      {
        "event_id": "evt_001",
        "event_type": "production.milestone_delayed",
        "event_time": "2026-04-01T10:30:00+08:00",
        "priority": "P1"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 20
  }
}
```

## 9. 跟单员 Agent 接口样例

### 9.1 调用跟单员 Agent

`POST /api/agents/follow-up/run`

请求样例：

```json
{
  "trigger_event": {
    "event_id": "evt_001",
    "event_type": "production.milestone_delayed",
    "event_time": "2026-04-01T10:30:00+08:00",
    "source_system": "kingdee_k3cloud",
    "biz_object_type": "order",
    "biz_object_id": "ord_001"
  },
  "order_context": {
    "order_id": "ord_001",
    "order_no": "SO-2026-0001",
    "current_status": "执行中",
    "sub_status": "生产中",
    "risk_level": "medium",
    "planned_delivery_date": "2026-04-10",
    "payment_status": "待回款"
  },
  "customer_context": {
    "customer_id": "cus_001",
    "customer_name": "华东重点客户A",
    "customer_level": "重点客户",
    "business_type": "内销",
    "owner_id": "user_sales_01"
  },
  "fulfillment_context": {
    "milestones": [
      {
        "milestone_type": "生产完成",
        "planned_time": "2026-04-05T18:00:00+08:00",
        "actual_time": null,
        "milestone_status": "delayed",
        "is_overdue": true
      }
    ],
    "latest_logistics_status": null,
    "document_status": "not_required",
    "customs_status": null,
    "exceptions": []
  },
  "payment_context": {
    "receivable_amount": 128000.0,
    "received_amount": 0.0,
    "due_date": "2026-04-30",
    "overdue_days": 0
  }
}
```

响应样例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "summary": "订单 SO-2026-0001 当前处于执行中阶段，生产里程碑超时，存在交付延期风险。",
    "risk_assessment": {
      "level": "high",
      "risk_type": "delivery_delay",
      "reason": "生产里程碑超时，订单存在交付延期风险"
    },
    "recommended_actions": [
      "联系工厂确认恢复时间并回填最新预计完成时间",
      "同步销售负责人评估是否需要提前告知客户"
    ],
    "task_drafts": [
      {
        "title": "确认工厂恢复时间",
        "assignee_role": "跟单员",
        "priority": "high",
        "due_hint": "2小时内"
      }
    ],
    "exception_marks": [
      {
        "exception_type": "交付异常",
        "exception_level": "P1",
        "reason": "生产里程碑超时，订单存在交付延期风险"
      }
    ],
    "notification_draft": "订单 SO-2026-0001 存在交付延期风险，请尽快确认工厂恢复时间。"
  }
}
```

## 10. 通知中心接口样例

### 10.1 发送钉钉通知

`POST /api/notifications/dingtalk`

请求样例：

```json
{
  "template_code": "NTF_PROD_DELAY",
  "receiver_ids": [
    "user_followup_01",
    "user_sales_01"
  ],
  "payload": {
    "order_no": "SO-2026-0001",
    "customer_name": "华东重点客户A",
    "risk_level": "P1",
    "message": "生产里程碑超时，请尽快确认恢复时间"
  }
}
```

响应样例：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "sent": true,
    "channel": "dingtalk"
  }
}
```

## 11. 第一阶段建议优先实现的接口

建议优先实现以下接口：

- `GET /api/orders`
- `GET /api/orders/{id}`
- `POST /api/orders/{id}/status`
- `POST /api/events`
- `POST /api/tasks`
- `GET /api/tasks`
- `POST /api/exceptions`
- `GET /api/exceptions`
- `POST /api/agents/follow-up/run`
- `POST /api/notifications/dingtalk`

## 12. 文档结论

API 请求 / 响应样例清单，是从架构设计走向接口开发的重要桥梁。

它可以直接为后续前端页面联调、后端接口实现和 Agent 编排调用提供统一参考。
