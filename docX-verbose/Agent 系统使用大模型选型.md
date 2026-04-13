
## 🎯 智谱大模型选型建议

基于当前的架构和 Agent 使用场景，我为你提供智谱大模型的选型建议：

### 📊 **你的 9 个 Hybrid Agent 场景分析**

| Agent | 主要任务 | 核心能力需求 | 推荐模型 |
|-------|---------|-------------|---------|
| **Sales Agent** | 销售沟通建议、报价表达 | 中文理解、商务表达、逻辑推理 | **GLM-4-Air** |
| **CRM Agent** | 客户画像、经营建议 | 文本总结、数据分析、中文表达 | **GLM-4-Air** |
| **Follow-up Agent** | 优化摘要、建议、通知 | 中文表达、任务理解 | **GLM-4-Air** |
| **Logistics Agent** | 客户同步话术、物流解释 | 中文表达、场景理解 | **GLM-4-Air** |
| **Finance Agent** | 催收建议、财务沟通 | 商务表达、风险控制理解 | **GLM-4-Air** |
| **Customer Service Agent** | 回复建议、问题摘要 | 情感理解、沟通表达 | **GLM-4-Air** |
| **Document Intelligence Agent** | 单证说明、修正建议 | 文档理解、结构化输出 | **GLM-4-Flash** 或 **GLM-4-Air** |
| **Operations Analyst Agent** | 经营报告、诊断建议 | 数据分析、深度推理、长文本 | **GLM-4-Plus** |
| **Knowledge Agent** | 知识归纳、SOP 总结 | 长文本理解、知识抽取 | **GLM-4-Plus** |

---

### 🏆 **智谱模型推荐方案**

#### **方案一：经济实用型（推荐起步）**
**全部使用 GLM-4-Air**

**优势：**
- ✅ 性价比高（约 ¥0.001/1K tokens）
- ✅ 中文能力优秀
- ✅ 响应速度快（~500ms）
- ✅ 支持 128K 上下文
- ✅ 足够应对所有 Agent 场景

**适用场景：**
- 预算有限
- 追求性价比
- 对响应速度有要求

---

#### **方案二：分级配置型（推荐生产）**
**按 Agent 重要性分级使用不同模型**

| 模型 | 适用 Agent | 理由 | 成本估算 |
|------|-----------|------|---------|
| **GLM-4-Plus** | Operations Analyst Agent<br>Knowledge Agent | 深度推理、复杂分析、长文本理解 | ¥0.05/1K tokens |
| **GLM-4-Air** | Sales/CRM/Follow-up/Logistics/Finance/Customer Service Agent | 日常沟通、建议生成、摘要优化 | ¥0.001/1K tokens |
| **GLM-4-Flash** | Document Intelligence Agent | 快速文档处理、结构化输出 | ¥0.0001/1K tokens |

**优势：**
- ✅ 关键 Agent 使用最强模型保证质量
- ✅ 日常 Agent 使用性价比模型控制成本
- ✅ 总体成本可控

---

#### **方案三：高性能型**
**全部使用 GLM-4-Plus**

**优势：**
- ✅ 最强推理能力
- ✅ 最佳中文理解
- ✅ 复杂任务表现优秀

**劣势：**
- ❌ 成本较高（¥0.05/1K tokens）
- ❌ 响应速度稍慢（~1-2s）

**适用场景：**
- 预算充足
- 对质量要求极高
- 复杂分析场景多

---

### 🔧 **如何集成智谱模型到你的系统**

#### **方式一：使用智谱官方 API（推荐）**

**1. 修改环境变量配置：**
```bash
# .env 文件
ZHIPU_API_KEY=your_zhipu_api_key
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4/chat/completions
ATLAS_AGENT_MODEL=glm-4-air  # 或 glm-4-plus, glm-4-flash
```

**2. 创建 ZhipuEnhancer 类：**

```python
# src/atlas_trade_ai/llm_zhipu.py
from __future__ import annotations

import json
import os
from typing import Any
from urllib import error, request


class ZhipuEnhancer:
    def __init__(self) -> None:
        self.api_key = os.getenv("ZHIPU_API_KEY")
        self.base_url = os.getenv(
            "ZHIPU_BASE_URL",
            "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        )
        self.model = os.getenv("ATLAS_AGENT_MODEL", "glm-4-air")

    def is_enabled(self) -> bool:
        return bool(self.api_key)

    def enhance(self, prompt: str) -> dict[str, Any] | None:
        if not self.api_key:
            return None

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "top_p": 0.9,
        }
        
        req = request.Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        
        try:
            with request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except (TimeoutError, error.URLError, error.HTTPError, json.JSONDecodeError):
            return None

        output_text = self._extract_text(data)
        if not output_text:
            return None
        
        try:
            return json.loads(output_text)
        except json.JSONDecodeError:
            return None

    def _extract_text(self, payload: dict[str, Any]) -> str | None:
        choices = payload.get("choices", [])
        if not choices:
            return None
        return choices[0].get("message", {}).get("content")
```

**3. 修改容器配置：**

```python
# src/atlas_trade_ai/container.py
def get_llm_enhancer():
    provider = os.getenv("ATLAS_LLM_PROVIDER", "openai")
    if provider == "zhipu":
        from atlas_trade_ai.llm_zhipu import ZhipuEnhancer
        return ZhipuEnhancer()
    else:
        from atlas_trade_ai.llm import OpenAIEnhancer
        return OpenAIEnhancer()
```

---

#### **方式二：使用 OpenAI 兼容接口（更简单）**

智谱支持 OpenAI 兼容格式，只需修改配置：

```bash
# .env 文件
OPENAI_API_KEY=your_zhipu_api_key
OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/chat/completions
ATLAS_AGENT_MODEL=glm-4-air
```

**无需修改代码**，直接使用现有的 `OpenAIEnhancer` 类即可！

---

### 📈 **智谱模型详细对比**

| 特性 | GLM-4-Flash | GLM-4-Air | GLM-4-Plus | GLM-4 |
|------|------------|-----------|------------|-------|
| **定位** | 极速版 | 平衡版 | 增强版 | 旗舰版 |
| **智能水平** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **响应速度** | 200ms | 500ms | 1-2s | 1-2s |
| **上下文** | 128K | 128K | 128K | 128K |
| **价格** | ¥0.0001/1K | ¥0.001/1K | ¥0.05/1K | ¥0.1/1K |
| **适合场景** | 简单抽取 | 日常对话 | 复杂推理 | 专业任务 |
| **中文能力** | 优秀 | 优秀 | 卓越 | 卓越 |

---

### 💡 **针对你系统的最佳推荐**

#### **推荐配置：分级方案**

```bash
# .env 文件

# 默认使用 GLM-4-Air（性价比最高）
ATLAS_LLM_PROVIDER=zhipu
ZHIPU_API_KEY=your_api_key
ATLAS_AGENT_MODEL=glm-4-air

# 为特定 Agent 配置不同模型（可选）
ATLAS_AGENT_MODEL_OPERATIONS_ANALYST=glm-4-plus
ATLAS_AGENT_MODEL_KNOWLEDGE=glm-4-plus
ATLAS_AGENT_MODEL_DOCUMENT=glm-4-flash
```

#### **理由：**
1. **9 个 Agent 中 7 个使用 GLM-4-Air**：性价比最优，中文表达优秀
2. **Operations Analyst 和 Knowledge 使用 GLM-4-Plus**：保证复杂分析质量
3. **Document Intelligence 使用 GLM-4-Flash**：文档处理追求速度

---

### 🎯 **迁移步骤**

1. **注册智谱账号**：https://open.bigmodel.cn/
2. **获取 API Key**
3. **修改 .env 配置**（使用 OpenAI 兼容接口方式最简单）
4. **测试单个 Agent**（建议先测试 Follow-up Agent）
5. **观察监控**：通过 `/api/agents/monitor` 查看大模型调用情况
6. **逐步切换所有 Agent**

---

### 📊 **成本估算**

假设每个 Agent 每天运行 100 次，每次平均 500 tokens：

| 方案 | 日成本 | 月成本 | 年成本 |
|------|--------|--------|--------|
| **全用 GLM-4-Air** | ¥0.45 | ¥13.5 | ¥164 |
| **分级配置** | ¥0.6 | ¥18 | ¥219 |
| **全用 GLM-4-Plus** | ¥22.5 | ¥675 | ¥8,212 |

**推荐分级配置方案**，性价比最高！

需要我帮你实现智谱模型的集成代码吗？