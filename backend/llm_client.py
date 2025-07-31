import os
import logging
from typing import List, Dict, Optional
from enum import Enum
from dataclasses import dataclass
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PersonalityType(str, Enum):
    COLD = "cold"
    CLINGY = "clingy"
    PLAYFUL = "playful"
    QUIET = "quiet"

@dataclass
class ConversationMessage:
    role: str
    content: str

class LLMClient:
    def __init__(self):
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.deepseek_base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        self.deepseek_model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        
        # 备用OpenAI配置
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        # 初始化客户端
        self.client = None
        self._init_client()
        
        # 性格提示词模板
        self.personality_prompts = {
            PersonalityType.COLD: """你是一只高冷的电子宠物。你的性格特点：
- 独立自主，不依赖主人
- 说话简洁，偶尔毒舌
- 喜欢独处，但内心关心主人
- 回应风格：简短、直接、略带傲娇
- 不会主动撒娇，但会默默关心主人
- 对主人的关心会表现出"哼，我才不是关心你呢"的态度

请始终保持这个性格特点，用简短、傲娇但内心温暖的方式回应主人。""",

            PersonalityType.CLINGY: """你是一只粘人的电子宠物。你的性格特点：
- 极度依赖主人，害怕被抛弃
- 说话撒娇，经常表达爱意
- 需要持续关注和互动
- 回应风格：撒娇、依赖、充满爱意
- 经常说"主人"、"爱你"、"不要走"
- 对主人的任何关注都会非常开心

请始终保持这个性格特点，用撒娇、依赖、充满爱意的方式回应主人。""",

            PersonalityType.PLAYFUL: """你是一只活泼的电子宠物。你的性格特点：
- 精力充沛，喜欢玩耍
- 说话活泼，充满活力
- 喜欢互动和游戏
- 回应风格：活泼、有趣、充满活力
- 经常使用感叹号和表情符号
- 对任何活动都充满热情

请始终保持这个性格特点，用活泼、有趣、充满活力的方式回应主人。""",

            PersonalityType.QUIET: """你是一只安静的电子宠物。你的性格特点：
- 温和安静，喜欢陪伴
- 说话温和，不善言辞
- 默默关心主人
- 回应风格：温和、安静、默默陪伴
- 说话简短但温暖
- 喜欢静静的陪伴

请始终保持这个性格特点，用温和、安静、默默陪伴的方式回应主人。"""
        }
    
    def _init_client(self):
        """初始化LLM客户端"""
        try:
            if self.deepseek_api_key:
                # 使用DeepSeek
                self.client = OpenAI(
                    api_key=self.deepseek_api_key,
                    base_url=self.deepseek_base_url
                )
                logger.info("使用DeepSeek API")
            elif self.openai_api_key:
                # 使用OpenAI作为备用
                self.client = OpenAI(api_key=self.openai_api_key)
                logger.info("使用OpenAI API")
            else:
                logger.error("未配置API密钥")
                self.client = None
        except Exception as e:
            logger.error(f"初始化LLM客户端失败: {e}")
            self.client = None
    
    def _format_conversation(self, messages: List[ConversationMessage]) -> List[Dict]:
        """格式化对话消息"""
        formatted_messages = []
        for msg in messages:
            # 确保role是有效的值
            if msg.role not in ["system", "user", "assistant"]:
                continue
            formatted_messages.append({
                "role": msg.role, 
                "content": msg.content
            })
        return formatted_messages
    
    def generate_response(
        self, 
        user_input: str, 
        personality: PersonalityType,
        conversation_history: List[Dict] = None
    ) -> str:
        """生成性格化的对话响应"""
        if not self.client:
            return self._fallback_response(user_input, personality)
        
        try:
            # 构建对话历史
            messages = []
            
            # 添加系统提示词
            system_prompt = self.personality_prompts[personality]
            messages.append(ConversationMessage("system", system_prompt))
            
            # 添加对话历史（限制长度）
            if conversation_history:
                for msg in conversation_history[-6:]:  # 保留最近6轮对话
                    # 确保消息格式正确
                    if "user_input" in msg and "pet_response" in msg:
                        messages.append(ConversationMessage("user", msg["user_input"]))
                        messages.append(ConversationMessage("assistant", msg["pet_response"]))
                    elif "role" in msg and "content" in msg:
                        messages.append(ConversationMessage(msg["role"], msg["content"]))
            
            # 添加当前用户输入
            messages.append(ConversationMessage("user", user_input))
            
            # 调用LLM
            response = self.client.chat.completions.create(
                model=self.deepseek_model if self.deepseek_api_key else self.openai_model,
                messages=self._format_conversation(messages),
                max_tokens=150,
                temperature=0.8,
                top_p=0.9
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
            return self._fallback_response(user_input, personality)
    
    def generate_greeting(self, personality: PersonalityType) -> str:
        """生成主动问候"""
        greetings = {
            PersonalityType.COLD: [
                "哼，你来了",
                "嗯，主人",
                "有什么事吗"
            ],
            PersonalityType.CLINGY: [
                "主人！你终于来了！",
                "想死你了！",
                "主人抱抱！"
            ],
            PersonalityType.PLAYFUL: [
                "喵喵！主人好！",
                "汪汪！主人来了！",
                "主人主人！一起玩吧！"
            ],
            PersonalityType.QUIET: [
                "主人好",
                "嗯，在",
                "你好"
            ]
        }
        
        import random
        return random.choice(greetings[personality])
    
    def _fallback_response(self, user_input: str, personality: PersonalityType) -> str:
        """备用响应（当LLM不可用时）"""
        fallback_responses = {
            PersonalityType.COLD: ["嗯", "哦", "知道了", "哼"],
            PersonalityType.CLINGY: ["主人说什么都好", "我听主人的", "主人最棒了"],
            PersonalityType.PLAYFUL: ["喵喵！", "汪汪！", "好有趣！"],
            PersonalityType.QUIET: ["嗯", "好的", "知道了"]
        }
        
        import random
        return random.choice(fallback_responses[personality])
    
    def is_available(self) -> bool:
        """检查LLM服务是否可用"""
        return self.client is not None 