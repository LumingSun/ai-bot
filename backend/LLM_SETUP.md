# LLM集成配置说明

## 概述

本项目已集成大语言模型（LLM）支持，可以通过System Prompt来驱动宠物的性格表现。

## 支持的LLM提供商

### 1. DeepSeek（推荐）
- **API地址**: https://api.deepseek.com/v1
- **模型**: deepseek-chat
- **特点**: 中文支持优秀，响应速度快

### 2. OpenAI（备用）
- **API地址**: https://api.openai.com/v1
- **模型**: gpt-3.5-turbo
- **特点**: 稳定性好，功能丰富

## 配置步骤

### 1. 创建环境变量文件

在 `backend/` 目录下创建 `.env` 文件：

```bash
# DeepSeek配置（推荐）
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat

# OpenAI配置（备用）
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# 应用配置
DEBUG=true
LOG_LEVEL=INFO
```

### 2. 获取API密钥

#### DeepSeek API密钥
1. 访问 [DeepSeek官网](https://platform.deepseek.com/)
2. 注册并登录账户
3. 在控制台中创建API密钥
4. 复制密钥到 `.env` 文件

#### OpenAI API密钥（备用）
1. 访问 [OpenAI官网](https://platform.openai.com/)
2. 注册并登录账户
3. 在API Keys页面创建密钥
4. 复制密钥到 `.env` 文件

### 3. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 4. 测试配置

运行测试脚本验证配置：

```bash
cd backend
python test_llm.py
```

## 性格系统

### 性格类型

1. **高冷型 (cold)**
   - 独立自主，不依赖主人
   - 说话简洁，偶尔毒舌
   - 傲娇但内心温暖

2. **粘人型 (clingy)**
   - 极度依赖主人，害怕被抛弃
   - 说话撒娇，经常表达爱意
   - 需要持续关注和互动

3. **活泼型 (playful)**
   - 精力充沛，喜欢玩耍
   - 说话活泼，充满活力
   - 对任何活动都充满热情

4. **安静型 (quiet)**
   - 温和安静，喜欢陪伴
   - 说话温和，不善言辞
   - 默默关心主人

### System Prompt设计

每个性格都有专门的System Prompt，确保LLM始终保持相应的性格特点：

```python
PERSONALITY_PROMPTS = {
    PersonalityType.COLD: """你是一只高冷的电子宠物...""",
    PersonalityType.CLINGY: """你是一只粘人的电子宠物...""",
    PersonalityType.PLAYFUL: """你是一只活泼的电子宠物...""",
    PersonalityType.QUIET: """你是一只安静的电子宠物..."""
}
```

## API端点

### 新增端点

- `GET /llm/status` - 获取LLM服务状态
- `POST /message` - 发送消息（已升级为LLM驱动）

### 响应示例

```json
{
  "available": true,
  "provider": "deepseek"
}
```

## 故障排除

### 常见问题

1. **API密钥错误**
   - 检查 `.env` 文件中的API密钥是否正确
   - 确认API密钥有足够的额度

2. **网络连接问题**
   - 检查网络连接
   - 确认防火墙设置

3. **依赖安装失败**
   - 确保Python版本 >= 3.8
   - 尝试使用虚拟环境

4. **LLM服务不可用**
   - 系统会自动回退到规则-based响应
   - 检查日志文件获取详细错误信息

### 调试模式

设置 `DEBUG=true` 可以启用详细日志：

```bash
export DEBUG=true
python main.py
```

## 性能优化

### 对话历史管理
- 限制对话历史长度为6轮
- 避免token消耗过多

### 响应优化
- 设置max_tokens=150限制响应长度
- 使用temperature=0.8增加创造性
- 使用top_p=0.9控制输出质量

## 下一步计划

1. **LangGraph工作流集成**
   - 重构为LangGraph状态管理
   - 添加条件分支和工具调用

2. **主动互动系统**
   - 定时问候功能
   - 情境感知响应

3. **工具集成**
   - 时间工具
   - 天气工具
   - 提醒工具 