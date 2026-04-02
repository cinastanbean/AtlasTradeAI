# 大模型配置指南

本文档说明如何配置和使用不同的大模型提供商（OpenAI / 智谱 AI）。

## 📋 目录

- [快速开始](#快速开始)
- [配置智谱 GLM-4-Air](#配置智谱-glm-4-air)
- [配置 OpenAI](#配置-openai)
- [模型选型建议](#模型选型建议)
- [常见问题](#常见问题)

---

## 🚀 快速开始

### 1. 复制配置文件

```bash
cp .env.example .env
```

### 2. 编辑 `.env` 文件

选择一个大模型提供商进行配置。

### 3. 重启服务

```bash
python -m uvicorn src.atlas_trade_ai.main:app --reload
```

---

## 🤖 配置智谱 GLM-4-Air（推荐）

### 1. 获取智谱 API Key

1. 访问 [智谱 AI 开放平台](https://open.bigmodel.cn/)
2. 注册/登录账号
3. 进入「API 密钥管理」
4. 创建新的 API Key
5. 复制 API Key 到配置文件

### 2. 编辑 `.env` 文件

```bash
# 设置大模型提供商为智谱
ATLAS_LLM_PROVIDER=zhipu

# 填写你的智谱 API Key
ZHIPU_API_KEY=your.zhipu_api_key_here

# 智谱 API 地址（默认配置，无需修改）
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4/chat/completions

# 选择模型（推荐 glm-4-air）
ATLAS_AGENT_MODEL=glm-4-air
```

### 3. 验证配置

访问 Agent 监控页面：`http://localhost:8000/ui/agents.html`

查看 Agent 运行记录，确认 `engine.provider` 显示为 `zhipu`。

---

## 🤖 配置 OpenAI

### 1. 获取 OpenAI API Key

1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 登录账号
3. 创建 API Key
4. 复制 API Key 到配置文件

### 2. 编辑 `.env` 文件

```bash
# 设置大模型提供商为 OpenAI（或不配置，默认为 openai）
ATLAS_LLM_PROVIDER=openai

# 填写你的 OpenAI API Key
OPENAI_API_KEY=sk-your_openai_api_key_here

# OpenAI API 地址（默认配置，无需修改）
OPENAI_BASE_URL=https://api.openai.com/v1/responses

# 选择模型（默认 gpt-5-mini）
ATLAS_AGENT_MODEL=gpt-5-mini
```

### 3. 验证配置

访问 Agent 监控页面：`http://localhost:8000/ui/agents.html`

查看 Agent 运行记录，确认 `engine.provider` 显示为 `openai`。

---

## 📊 模型选型建议

### 智谱 GLM-4 系列对比

| 模型 | 定位 | 智能水平 | 响应速度 | 上下文 | 价格 | 推荐场景 |
|------|------|---------|---------|--------|------|---------|
| **GLM-4-Flash** | 极速版 | ⭐⭐⭐ | 200ms | 128K | ¥0.0001/1K | 简单文档处理、快速抽取 |
| **GLM-4-Air** ⭐ | 平衡版 | ⭐⭐⭐⭐ | 500ms | 128K | ¥0.001/1K | 日常对话、建议生成、摘要优化 |
| **GLM-4-Plus** | 增强版 | ⭐⭐⭐⭐⭐ | 1-2s | 128K | ¥0.05/1K | 复杂分析、深度推理、经营报告 |
| **GLM-4** | 旗舰版 | ⭐⭐⭐⭐⭐ | 1-2s | 128K | ¥0.1/1K | 专业任务、最高质量要求 |

### 针对你的 Agent 系统推荐

#### 经济实用型（全部使用 GLM-4-Air）

**配置：**
```bash
ATLAS_LLM_PROVIDER=zhipu
ATLAS_AGENT_MODEL=glm-4-air
```

**优势：**
- ✅ 性价比最高（约 ¥0.001/1K tokens）
- ✅ 中文能力优秀
- ✅ 响应速度快（~500ms）
- ✅ 适合所有 9 个 Hybrid Agent

**适用场景：**
- 预算有限
- 追求性价比
- 对响应速度有要求

#### 分级配置型（推荐生产环境）

**配置：**
```bash
# 默认使用 GLM-4-Air
ATLAS_LLM_PROVIDER=zhipu
ATLAS_AGENT_MODEL=glm-4-air

# 为特定 Agent 配置不同模型（需要修改代码）
# ATLAS_AGENT_MODEL_OPERATIONS_ANALYST=glm-4-plus
# ATLAS_AGENT_MODEL_KNOWLEDGE=glm-4-plus
```

**模型分配：**
- **GLM-4-Plus**: Operations Analyst Agent, Knowledge Agent（复杂分析）
- **GLM-4-Air**: Sales/CRM/Follow-up/Logistics/Finance/Customer Service Agent（日常任务）
- **GLM-4-Flash**: Document Intelligence Agent（快速文档处理）

**优势：**
- ✅ 关键 Agent 使用最强模型保证质量
- ✅ 日常 Agent 使用性价比模型控制成本
- ✅ 总体成本可控

**月成本估算：** 约 ¥18-30（假设每个 Agent 每天运行 100 次）

---

## 💰 成本估算

假设每个 Agent 每天运行 100 次，每次平均 500 tokens：

| 配置方案 | 日成本 | 月成本 | 年成本 |
|---------|--------|--------|--------|
| **全用 GLM-4-Air** | ¥0.45 | ¥13.5 | ¥164 |
| **分级配置** | ¥0.6 | ¥18 | ¥219 |
| **全用 GLM-4-Plus** | ¥22.5 | ¥675 | ¥8,212 |
| **全用 GPT-5-mini** | ¥1.8 | ¥54 | ¥657 |

**推荐：GLM-4-Air 性价比最高！**

---

## 🔧 常见问题

### Q1: 如何切换大模型提供商？

只需修改 `.env` 文件中的 `ATLAS_LLM_PROVIDER`，然后重启服务：

```bash
# 切换到智谱
ATLAS_LLM_PROVIDER=zhipu

# 切换到 OpenAI
ATLAS_LLM_PROVIDER=openai
```

### Q2: 同时配置 OpenAI 和智谱会怎样？

系统会根据 `ATLAS_LLM_PROVIDER` 的值选择使用哪个提供商，另一个会被忽略。

### Q3: 如何验证大模型是否正常工作？

1. 访问 Agent 监控页面：`http://localhost:8000/ui/agents.html`
2. 触发一个 Agent 运行（如创建一个订单）
3. 查看运行记录中的 `engine` 字段：
   - `provider`: 显示使用的提供商（`zhipu` 或 `openai`）
   - `llm_used`: 显示是否使用了大模型（`true` 或 `false`）
   - `model`: 显示使用的具体模型

### Q4: 大模型调用失败会怎样？

系统会自动降级到纯规则模式，不会影响业务运行。`engine.fallback_reason` 会说明降级原因。

### Q5: 如何查看大模型调用日志？

查看 Agent 运行记录：

```bash
GET /api/agents/monitor
```

返回结果中包含每次运行的详细信息。

### Q6: 智谱 API Key 在哪里获取？

访问 [智谱 AI 开放平台](https://open.bigmodel.cn/) → API 密钥管理 → 创建 API Key。

### Q7: 如何优化大模型使用成本？

1. **使用 GLM-4-Air**：性价比最高
2. **调整 Agent 运行频率**：非关键事件减少触发
3. **使用 Rules 模式**：对不需要大模型的 Agent 设置为 `rules` 模式
4. **优化 Prompt**：减少不必要的 tokens 消耗

---

## 📚 相关文档

- [Agent 架构设计](./03-agent-architecture/intelligence-capabilities-and-agent-evolution.md)
- [Agent 监控中台](./03-agent-architecture/agent-monitoring-center-and-new-agents.md)
- [环境配置说明](../.env.example)

---

## 🎯 总结

- ✅ **支持双提供商**：OpenAI 和智谱 AI
- ✅ **配置简单**：只需修改 `.env` 文件
- ✅ **自动降级**：大模型失败时自动切换到规则模式
- ✅ **成本可控**：推荐使用 GLM-4-Air，月成本约 ¥18
- ✅ **灵活切换**：无需修改代码，重启即可生效

**推荐配置：智谱 GLM-4-Air** 🌟
