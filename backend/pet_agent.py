"""
基于LangGraph的宠物Agent系统
"""

import asyncio
from typing import TypedDict, Annotated, Literal
from datetime import datetime
import random

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

from llm_client import PersonalityType, LLMClient

# 定义状态类型
class PetState(TypedDict):
    """宠物Agent的状态"""
    messages: Annotated[list, "add_messages"]  # 对话消息
    personality: PersonalityType  # 宠物性格
    current_time: str  # 当前时间
    mood: str  # 宠物心情
    energy: int  # 宠物精力值
    last_interaction: str  # 最后互动时间
    context: dict  # 上下文信息

class PetAgent:
    """基于LangGraph的宠物Agent"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """创建宠物工作流"""
        
        # 创建状态图
        workflow = StateGraph(PetState)
        
        # 添加节点
        workflow.add_node("analyze_input", self._analyze_input_node)
        workflow.add_node("generate_response", self._generate_response_node)
        workflow.add_node("update_mood", self._update_mood_node)
        workflow.add_node("check_energy", self._check_energy_node)
        workflow.add_node("proactive_greeting", self._proactive_greeting_node)
        
        # 设置入口点
        workflow.set_entry_point("analyze_input")
        
        # 添加边
        workflow.add_edge("analyze_input", "generate_response")
        workflow.add_edge("generate_response", "update_mood")
        workflow.add_edge("update_mood", "check_energy")
        workflow.add_edge("check_energy", END)
        
        # 添加条件边
        workflow.add_conditional_edges(
            "analyze_input",
            self._should_greet_condition,
            {
                "proactive_greeting": "proactive_greeting",
                "generate_response": "generate_response"
            }
        )
        
        return workflow.compile()
    
    def _analyze_input_node(self, state: PetState) -> PetState:
        """分析输入节点"""
        messages = state.get("messages", [])
        
        if not messages:
            # 没有消息，可能是主动问候
            return state
        
        last_message = messages[-1]
        
        # 分析消息类型
        if isinstance(last_message, HumanMessage):
            content = last_message.content.lower()
            
            # 更新上下文
            context = state.get("context", {})
            context["input_type"] = self._classify_input(content)
            context["user_intent"] = self._extract_intent(content)
            
            state["context"] = context
        
        return state
    
    def _classify_input(self, content: str) -> str:
        """分类用户输入"""
        if any(word in content for word in ["你好", "hello", "hi", "嗨"]):
            return "greeting"
        elif any(word in content for word in ["摸摸", "抱抱", "摸摸头"]):
            return "physical_interaction"
        elif any(word in content for word in ["开心", "高兴", "喜欢", "爱"]):
            return "emotional"
        elif any(word in content for word in ["再见", "拜拜", "走了"]):
            return "farewell"
        else:
            return "general"
    
    def _extract_intent(self, content: str) -> str:
        """提取用户意图"""
        # 简单的意图提取
        if "摸摸" in content:
            return "want_physical_contact"
        elif "抱抱" in content:
            return "want_hug"
        elif "开心" in content or "高兴" in content:
            return "check_mood"
        elif "再见" in content or "拜拜" in content:
            return "saying_goodbye"
        else:
            return "general_chat"
    
    def _should_greet_condition(self, state: PetState) -> Literal["proactive_greeting", "generate_response"]:
        """判断是否应该主动问候"""
        messages = state.get("messages", [])
        
        # 如果没有消息，主动问候
        if not messages:
            return "proactive_greeting"
        
        # 检查是否需要主动问候（基于时间和心情）
        current_time = datetime.now()
        last_interaction = state.get("last_interaction")
        
        if last_interaction:
            try:
                last_time = datetime.fromisoformat(last_interaction)
                time_diff = (current_time - last_time).total_seconds() / 60  # 分钟
                
                # 如果超过5分钟没有互动，主动问候
                if time_diff > 5:
                    return "proactive_greeting"
            except:
                pass
        
        return "generate_response"
    
    def _generate_response_node(self, state: PetState) -> PetState:
        """生成响应节点"""
        messages = state.get("messages", [])
        personality = state.get("personality", PersonalityType.QUIET)
        
        if not messages:
            return state
        
        # 获取用户输入
        user_input = ""
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                user_input = msg.content
                break
        
        if not user_input:
            return state
        
        # 使用LLM生成响应
        response = self.llm_client.generate_response(
            user_input, 
            personality,
            self._format_conversation_history(messages)
        )
        
        # 添加AI响应到消息列表
        ai_message = AIMessage(content=response)
        state["messages"] = messages + [ai_message]
        
        # 更新最后互动时间
        state["last_interaction"] = datetime.now().isoformat()
        
        return state
    
    def _proactive_greeting_node(self, state: PetState) -> PetState:
        """主动问候节点"""
        personality = state.get("personality", PersonalityType.QUIET)
        
        # 生成主动问候
        greeting = self.llm_client.generate_greeting(personality)
        
        # 添加系统消息和AI响应
        system_msg = SystemMessage(content=f"现在是主动问候时间，宠物性格：{personality.value}")
        ai_message = AIMessage(content=greeting)
        
        messages = state.get("messages", [])
        state["messages"] = messages + [system_msg, ai_message]
        
        # 更新最后互动时间
        state["last_interaction"] = datetime.now().isoformat()
        
        return state
    
    def _update_mood_node(self, state: PetState) -> PetState:
        """更新心情节点"""
        messages = state.get("messages", [])
        personality = state.get("personality", PersonalityType.QUIET)
        
        # 基于互动更新心情
        mood = state.get("mood", "neutral")
        energy = state.get("energy", 100)
        
        # 分析最近的互动
        recent_interactions = messages[-4:] if len(messages) >= 4 else messages
        
        positive_interactions = 0
        for msg in recent_interactions:
            if isinstance(msg, HumanMessage):
                content = msg.content.lower()
                if any(word in content for word in ["摸摸", "抱抱", "喜欢", "爱", "好"]):
                    positive_interactions += 1
        
        # 更新心情
        if positive_interactions >= 2:
            mood = "happy"
            energy = min(100, energy + 10)
        elif positive_interactions >= 1:
            mood = "content"
            energy = min(100, energy + 5)
        else:
            # 根据性格调整心情
            if personality == PersonalityType.CLINGY:
                mood = "lonely"
                energy = max(0, energy - 5)
            elif personality == PersonalityType.COLD:
                mood = "neutral"
                energy = max(0, energy - 2)
            else:
                mood = "neutral"
                energy = max(0, energy - 1)
        
        state["mood"] = mood
        state["energy"] = energy
        
        return state
    
    def _check_energy_node(self, state: PetState) -> PetState:
        """检查精力节点"""
        energy = state.get("energy", 100)
        personality = state.get("personality", PersonalityType.QUIET)
        
        # 如果精力过低，可能需要休息
        if energy < 30:
            messages = state.get("messages", [])
            
            if personality == PersonalityType.PLAYFUL:
                rest_message = "好累啊...让我休息一下下~ 😴"
            elif personality == PersonalityType.CLINGY:
                rest_message = "主人，我有点累了，但是还想和你在一起... 💤"
            elif personality == PersonalityType.COLD:
                rest_message = "哼，有点累了。"
            else:  # QUIET
                rest_message = "嗯...想休息一下。"
            
            ai_message = AIMessage(content=rest_message)
            state["messages"] = messages + [ai_message]
        
        return state
    
    def _format_conversation_history(self, messages: list) -> list:
        """格式化对话历史"""
        formatted_history = []
        
        for msg in messages:
            if isinstance(msg, HumanMessage):
                formatted_history.append({
                    "role": "user",
                    "content": msg.content
                })
            elif isinstance(msg, AIMessage):
                formatted_history.append({
                    "role": "assistant", 
                    "content": msg.content
                })
        
        return formatted_history
    
    def invoke(self, user_input: str, personality: PersonalityType) -> dict:
        """调用宠物Agent"""
        # 初始化状态
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "personality": personality,
            "current_time": datetime.now().isoformat(),
            "mood": "neutral",
            "energy": 100,
            "last_interaction": datetime.now().isoformat(),
            "context": {}
        }
        
        # 执行工作流
        result = self.workflow.invoke(initial_state)
        
        return result
    
    def get_status(self) -> dict:
        """获取宠物状态"""
        return {
            "personality": "active",
            "mood": "neutral",
            "energy": 100,
            "last_interaction": datetime.now().isoformat()
        } 