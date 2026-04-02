# 大模型配置快速参考

## 🚀 30 秒快速配置智谱 GLM-4-Air

### 步骤 1：获取 API Key

访问 [智谱 AI 开放平台](https://open.bigmodel.cn/) → API 密钥管理 → 创建 API Key

### 步骤 2：配置环境变量

编辑 `.env` 文件：

```bash
# 设置大模型提供商为智谱
ATLAS_LLM_PROVIDER=zhipu

# 填写你的智谱 API Key
ZHIPU_API_KEY=your.zhipu_api_key_here

# 使用 GLM-4-Air 模型（推荐）
ATLAS_AGENT_MODEL=glm-4-air
```

### 步骤 3：重启服务

```bash
python -m uvicorn src.atlas_trade_ai.main:app --reload
```

### ✅ 完成！

访问 Agent 监控页面验证：`http://localhost:8000/ui/agents.html`

---

## 📊 模型推荐

**全部 9 个 Hybrid Agent 使用 GLM-4-Air**

| 模型 | 价格 | 速度 | 推荐度 |
|------|------|------|--------|
| **GLM-4-Air** ⭐ | ¥0.001/1K | 500ms | ⭐⭐⭐⭐⭐ |
| GLM-4-Flash | ¥0.0001/1K | 200ms | ⭐⭐⭐ |
| GLM-4-Plus | ¥0.05/1K | 1-2s | ⭐⭐⭐⭐ |

---

## 💰 成本对比

| 方案 | 月成本 | 年成本 |
|------|--------|--------|
| **智谱 GLM-4-Air** | ¥13.5 | ¥164 |
| OpenAI GPT-5-mini | ¥54 | ¥657 |

**节省 75% 成本！** 💰

---

## 🔧 常用命令

```bash
# 测试智谱集成
python tests/test_zhipu_integration.py

# 启动服务
python -m uvicorn src.atlas_trade_ai.main:app --reload

# 查看 Agent 监控
curl http://localhost:8000/api/agents/monitor
```

---

## 📋 完整配置示例

```bash
# .env 文件

# ========== 大模型配置 ==========
ATLAS_LLM_PROVIDER=zhipu
ZHIPU_API_KEY=your.zhipu_api_key
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4/chat/completions
ATLAS_AGENT_MODEL=glm-4-air

# ========== Agent 运行模式 ==========
ATLAS_AGENT_MODE=hybrid

# ========== 数据库 ==========
ATLAS_DB_PATH=data/atlas.db

# ========== 服务器 ==========
HOST=0.0.0.0
PORT=8000
```

---

## 🆘 故障排查

### 大模型未启用

检查 `.env` 文件：
```bash
# 确保配置了这些变量
ATLAS_LLM_PROVIDER=zhipu
ZHIPU_API_KEY=your_key_here
```

### 切换回 OpenAI

```bash
# 修改 .env
ATLAS_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your_key
ATLAS_AGENT_MODEL=gpt-5-mini

# 重启服务
```

---

## 📚 详细文档

- [完整配置指南](./docs/04-deployment-and-configuration/llm-configuration-guide.md)
- [智谱集成说明](./ZHIPU_INTEGRATION.md)
- [环境配置示例](./.env.example)

---

**推荐使用：智谱 GLM-4-Air** 🌟
- ✅ 性价比最高
- ✅ 中文能力优秀
- ✅ 响应速度快
- ✅ 月成本仅 ¥13.5
