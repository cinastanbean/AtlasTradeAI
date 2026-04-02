#!/usr/bin/env python3
"""测试智谱大模型集成。"""

import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from atlas_trade_ai.llm import create_enhancer


def test_zhipu_enhancer():
    """测试智谱大模型增强器。"""
    print("=" * 60)
    print("智谱大模型集成测试")
    print("=" * 60)
    
    # 检查环境变量
    provider = os.getenv("ATLAS_LLM_PROVIDER", "openai")
    api_key = os.getenv("ZHIPU_API_KEY")
    model = os.getenv("ATLAS_AGENT_MODEL", "glm-4-air")
    
    print(f"\n当前配置:")
    print(f"  大模型提供商：{provider}")
    print(f"  模型：{model}")
    print(f"  API Key 已配置：{'是' if api_key else '否'}")
    
    if provider != "zhipu":
        print("\n⚠️  警告：当前未使用智谱模型，请设置 ATLAS_LLM_PROVIDER=zhipu")
        return False
    
    if not api_key:
        print("\n❌ 错误：ZHIPU_API_KEY 未配置")
        print("\n请在 .env 文件中配置:")
        print("  ATLAS_LLM_PROVIDER=zhipu")
        print("  ZHIPU_API_KEY=your_api_key")
        return False
    
    # 创建增强器
    print("\n创建增强器...")
    enhancer = create_enhancer()
    print(f"  增强器类型：{type(enhancer).__name__}")
    print(f"  启用状态：{'是' if enhancer.is_enabled() else '否'}")
    
    if not enhancer.is_enabled():
        print("\n❌ 增强器未启用，请检查 API Key 配置")
        return False
    
    # 测试增强功能
    print("\n测试增强功能...")
    test_prompt = """
你是贸易公司的跟单经理，请优化以下通知：

订单号：PO20240101
客户：ABC 公司
事件：生产延期
当前状态：生产中/延期

请只返回 JSON：
{
  "summary": "string",
  "recommended_actions": ["string"],
  "notification_draft": "string"
}
"""
    
    print("  发送请求到智谱 API...")
    result = enhancer.enhance(test_prompt)
    
    if result:
        print("\n✅ 测试成功！")
        print(f"\n返回结果:")
        print(f"  摘要：{result.get('summary', 'N/A')[:50]}...")
        print(f"  建议数量：{len(result.get('recommended_actions', []))}")
        print(f"  通知草稿：{result.get('notification_draft', 'N/A')[:50]}...")
        return True
    else:
        print("\n❌ 测试失败：未收到有效响应")
        print("\n可能原因:")
        print("  1. API Key 无效")
        print("  2. 网络连接问题")
        print("  3. API 服务暂时不可用")
        print("  4. 请求格式错误")
        return False


def test_openai_enhancer():
    """测试 OpenAI 大模型增强器（对比测试）。"""
    print("\n" + "=" * 60)
    print("OpenAI 大模型集成测试（对比）")
    print("=" * 60)
    
    provider = os.getenv("ATLAS_LLM_PROVIDER", "openai")
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("ATLAS_AGENT_MODEL", "gpt-5-mini")
    
    print(f"\n当前配置:")
    print(f"  大模型提供商：{provider}")
    print(f"  模型：{model}")
    print(f"  API Key 已配置：{'是' if api_key else '否'}")
    
    if not api_key:
        print("\n⚠️  OpenAI API Key 未配置，跳过测试")
        return None
    
    enhancer = create_enhancer()
    print(f"\n  增强器类型：{type(enhancer).__name__}")
    print(f"  启用状态：{'是' if enhancer.is_enabled() else '否'}")
    
    return enhancer.is_enabled()


if __name__ == "__main__":
    print("\n🚀 开始测试大模型集成...\n")
    
    # 测试智谱
    zhipu_success = test_zhipu_enhancer()
    
    # 测试 OpenAI（可选）
    openai_success = test_openai_enhancer()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"智谱模型：{'✅ 通过' if zhipu_success else '❌ 失败'}")
    print(f"OpenAI 模型：{'✅ 通过' if openai_success else '⚠️  未测试' if openai_success is None else '❌ 失败'}")
    
    if zhipu_success:
        print("\n🎉 智谱大模型集成成功！可以开始使用 GLM-4-Air。")
        sys.exit(0)
    else:
        print("\n❌ 智谱大模型集成失败，请检查配置。")
        sys.exit(1)
