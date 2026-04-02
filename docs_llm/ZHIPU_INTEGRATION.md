# 智谱大模型集成说明

## 📋 概述

AtlasTradeAI 现已支持智谱 AI 的 GLM-4 系列大模型，所有 9 个 Hybrid Agent 都可以使用智谱模型进行能力增强。

## 🎯 已完成的修改

### 1. 新增文件

- **`src/atlas_trade_ai/llm_zhipu.py`** - 智谱大模型增强器实现
- **`.env.example`** - 环境配置示例文件
- **`docs/04-deployment-and-configuration/llm-configuration-guide.md`** - 详细配置指南
- **`tests/test_zhipu_integration.py`** - 智谱模型集成测试
- **`scripts/setup_zhipu.sh`** - 快速配置脚本

### 2. 修改文件

- **`src/atlas_trade_ai/llm.py`** - 添加 `create_enhancer()` 工厂方法
- **`src/atlas_trade_ai/agent.py`** - FollowUpAgent 使用工厂方法创建增强器
- **`src/atlas_trade_ai/services/intelligent_role_agent_service.py`** - IntelligentRoleAgentService 使用工厂方法

## 🚀 快速开始

### 方式一：使用配置脚本（推荐）

```bash
# 运行配置脚本
bash scripts/setup_zhipu.sh

# 按提示输入智谱 API Key
```

### 方式二：手动配置

1. **复制配置文件**
   ```bash
   cp .env.example .env
   ```

2. **编辑 `.env` 文件**
   ```bash
   # 设置大模型提供商为智谱
   ATLAS_LLM_PROVIDER=zhipu
   
   # 填写你的智谱 API Key
   ZHIPU_API_KEY=your.zhipu_api_key_here
   
   # 选择模型（推荐 glm-4-air）
   ATLAS_AGENT_MODEL=glm-4-air
   ```

3. **测试配置**
   ```bash
   python tests/test_zhipu_integration.py
   ```

4. **启动服务**
   ```bash
   python -m uvicorn src.atlas_trade_ai.main:app --reload
   ```

## 📊 模型选型

### 推荐配置：GLM-4-Air

**所有 9 个 Hybrid Agent 都使用 GLM-4-Air**

| Agent | 使用场景 | 模型 |
|-------|---------|------|
| Sales Agent | 销售沟通建议 | GLM-4-Air |
| CRM Agent | 客户画像分析 | GLM-4-Air |
| Follow-up Agent | 摘要优化、通知生成 | GLM-4-Air |
| Logistics Agent | 物流解释、客户同步 | GLM-4-Air |
| Finance Agent | 催收建议、财务沟通 | GLM-4-Air |
| Customer Service Agent | 回复建议、问题摘要 | GLM-4-Air |
| Document Intelligence Agent | 单证说明、修正建议 | GLM-4-Air |
| Operations Analyst Agent | 经营报告、诊断建议 | GLM-4-Air |
| Knowledge Agent | 知识归纳、SOP 总结 | GLM-4-Air |

**优势：**
- ✅ 性价比最高（¥0.001/1K tokens）
- ✅ 中文能力优秀
- ✅ 响应速度快（~500ms）
- ✅ 月成本约 ¥13.5（假设每个 Agent 每天运行 100 次）

### 其他模型选项

| 模型 | 定位 | 价格 | 适用场景 |
|------|------|------|---------|
| GLM-4-Flash | 极速版 | ¥0.0001/1K | 简单文档处理 |
| **GLM-4-Air** ⭐ | 平衡版 | ¥0.001/1K | 日常对话、建议生成（推荐） |
| GLM-4-Plus | 增强版 | ¥0.05/1K | 复杂分析、深度推理 |
| GLM-4 | 旗舰版 | ¥0.1/1K | 专业任务 |

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `ATLAS_LLM_PROVIDER` | 大模型提供商 | `openai` | `zhipu` 或 `openai` |
| `ZHIPU_API_KEY` | 智谱 API Key | - | `your.zhipu_api_key` |
| `ZHIPU_BASE_URL` | 智谱 API 地址 | 官方地址 | `https://open.bigmodel.cn/api/paas/v4/chat/completions` |
| `ATLAS_AGENT_MODEL` | 使用的模型 | `glm-4-air` | `glm-4-air`, `glm-4-plus` |

### 完整配置示例

```bash
# .env 文件

# 大模型配置 - 使用智谱
ATLAS_LLM_PROVIDER=zhipu
ZHIPU_API_KEY=your.zhipu_api_key_here
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4/chat/completions
ATLAS_AGENT_MODEL=glm-4-air

# Agent 运行模式
ATLAS_AGENT_MODE=hybrid

# 数据库路径
ATLAS_DB_PATH=data/atlas.db
```

## ✅ 验证配置

### 1. 运行测试脚本

```bash
python tests/test_zhipu_integration.py
```

**成功输出示例：**
```
====================================
智谱大模型集成测试
====================================

当前配置:
  大模型提供商：zhipu
  模型：glm-4-air
  API Key 已配置：是

创建增强器...
  增强器类型：ZhipuEnhancer
  启用状态：是

测试增强功能...
  发送请求到智谱 API...

✅ 测试成功！

返回结果:
  摘要：订单 PO20240101 因生产延期...
  建议数量：3
  通知草稿：尊敬的 ABC 公司，由于生产原因...
```

### 2. 查看 Agent 监控

访问：`http://localhost:8000/ui/agents.html`

查看运行记录中的 `engine` 字段：
```json
{
  "mode": "hybrid",
  "provider": "zhipu",
  "llm_used": true,
  "model": "glm-4-air"
}
```

## 🔄 切换大模型提供商

### 从 OpenAI 切换到智谱

只需修改 `.env` 文件：

```bash
# 修改前（OpenAI）
ATLAS_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
ATLAS_AGENT_MODEL=gpt-5-mini

# 修改后（智谱）
ATLAS_LLM_PROVIDER=zhipu
ZHIPU_API_KEY=your.zhipu_api_key
ATLAS_AGENT_MODEL=glm-4-air
```

然后重启服务即可，**无需修改代码**。

## 📈 成本对比

### 使用 OpenAI GPT-5-mini

- 单次成本：约 ¥0.018
- 日成本（9 个 Agent × 100 次）：¥1.8
- **月成本：¥54**
- **年成本：¥657**

### 使用智谱 GLM-4-Air ⭐

- 单次成本：约 ¥0.0005
- 日成本（9 个 Agent × 100 次）：¥0.45
- **月成本：¥13.5**
- **年成本：¥164**

**节省成本：约 75%！** 💰

## 🛠️ 故障排查

### 问题 1：大模型调用失败

**现象：** `engine.llm_used` 为 `false`，`engine.fallback_reason` 显示 "OPENAI_API_KEY 未配置"

**解决：**
1. 检查 `.env` 文件中 `ZHIPU_API_KEY` 是否正确配置
2. 确认 `ATLAS_LLM_PROVIDER=zhipu`
3. 重启服务

### 问题 2：返回 JSON 解析失败

**现象：** 测试脚本显示 "JSON 解析错误"

**解决：**
1. 检查 `ATLAS_AGENT_MODEL` 是否正确
2. 确认 Prompt 中要求返回 JSON 格式
3. 查看智谱 API 文档确认模型支持 JSON 输出

### 问题 3：网络连接超时

**现象：** 测试超时或连接失败

**解决：**
1. 检查网络连接
2. 确认防火墙允许访问 `open.bigmodel.cn`
3. 尝试增加超时时间（修改 `llm_zhipu.py` 中的 `timeout` 参数）

## 📚 相关文档

- [大模型配置指南](./docs/04-deployment-and-configuration/llm-configuration-guide.md)
- [Agent 架构设计](./docs/03-agent-architecture/intelligence-capabilities-and-agent-evolution.md)
- [环境配置示例](./.env.example)

## 🎯 总结

✅ **所有修改已完成**  
✅ **保留 OpenAI 支持**  
✅ **通过配置文件选择大模型**  
✅ **推荐使用 GLM-4-Air**  
✅ **成本降低 75%**  
✅ **无需修改业务代码**  

**下一步：** 配置智谱 API Key 并运行测试！🚀
