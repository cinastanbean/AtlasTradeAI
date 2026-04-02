#!/bin/bash
# 智谱大模型快速配置脚本

echo "======================================"
echo "AtlasTradeAI 智谱大模型快速配置"
echo "======================================"
echo ""

# 检查 .env 文件是否存在
if [ ! -f .env ]; then
    echo "📋 未找到 .env 文件，正在创建..."
    cp .env.example .env
    echo "✅ 已创建 .env 文件"
    echo ""
fi

# 显示当前配置
echo "🔍 当前配置:"
echo ""
grep -E "^ATLAS_LLM_PROVIDER=|^ZHIPU_API_KEY=|^ATLAS_AGENT_MODEL=" .env 2>/dev/null || echo "  未配置相关变量"
echo ""

# 询问用户选择
echo "请选择大模型配置:"
echo "  1. 配置智谱 GLM-4-Air（推荐）"
echo "  2. 配置 OpenAI"
echo "  3. 查看当前配置并退出"
echo "  4. 退出"
echo ""
read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🤖 配置智谱 GLM-4-Air"
        echo ""
        read -p "请输入你的智谱 API Key: " zhipu_key
        
        if [ -z "$zhipu_key" ]; then
            echo "❌ API Key 不能为空"
            exit 1
        fi
        
        # 备份原文件
        cp .env .env.backup
        
        # 更新配置
        # 移除旧配置
        grep -v "^ATLAS_LLM_PROVIDER=" .env | grep -v "^ZHIPU_API_KEY=" | grep -v "^ZHIPU_BASE_URL=" | grep -v "^ATLAS_AGENT_MODEL=" > .env.tmp
        
        # 添加新配置
        cat >> .env.tmp << EOF

# 智谱大模型配置
ATLAS_LLM_PROVIDER=zhipu
ZHIPU_API_KEY=$zhipu_key
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4/chat/completions
ATLAS_AGENT_MODEL=glm-4-air
EOF
        
        mv .env.tmp .env
        echo ""
        echo "✅ 智谱配置已保存"
        echo ""
        echo "📝 配置详情:"
        grep -E "^ATLAS_LLM_PROVIDER=|^ZHIPU_API_KEY=|^ZHIPU_BASE_URL=|^ATLAS_AGENT_MODEL=" .env
        echo ""
        echo "💡 下一步:"
        echo "  1. 运行测试：python tests/test_zhipu_integration.py"
        echo "  2. 启动服务：python -m uvicorn src.atlas_trade_ai.main:app --reload"
        echo "  3. 访问监控：http://localhost:8000/ui/agents.html"
        echo ""
        ;;
        
    2)
        echo ""
        echo "🤖 配置 OpenAI"
        echo ""
        read -p "请输入你的 OpenAI API Key: " openai_key
        
        if [ -z "$openai_key" ]; then
            echo "❌ API Key 不能为空"
            exit 1
        fi
        
        # 备份原文件
        cp .env .env.backup
        
        # 更新配置
        grep -v "^ATLAS_LLM_PROVIDER=" .env | grep -v "^OPENAI_API_KEY=" | grep -v "^OPENAI_BASE_URL=" | grep -v "^ATLAS_AGENT_MODEL=" > .env.tmp
        
        cat >> .env.tmp << EOF

# OpenAI 大模型配置
ATLAS_LLM_PROVIDER=openai
OPENAI_API_KEY=$openai_key
OPENAI_BASE_URL=https://api.openai.com/v1/responses
ATLAS_AGENT_MODEL=gpt-5-mini
EOF
        
        mv .env.tmp .env
        echo ""
        echo "✅ OpenAI 配置已保存"
        echo ""
        echo "📝 配置详情:"
        grep -E "^ATLAS_LLM_PROVIDER=|^OPENAI_API_KEY=|^OPENAI_BASE_URL=|^ATLAS_AGENT_MODEL=" .env
        echo ""
        ;;
        
    3)
        echo ""
        echo "📋 当前配置:"
        echo ""
        cat .env | grep -E "^ATLAS_LLM_PROVIDER=|^ZHIPU_|^OPENAI_|^ATLAS_AGENT_MODEL=" || echo "  未配置相关变量"
        echo ""
        ;;
        
    4)
        echo "👋 退出"
        exit 0
        ;;
        
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo "======================================"
echo "配置完成！"
echo "======================================"
