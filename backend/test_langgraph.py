#!/usr/bin/env python3
"""
LangGraph集成测试脚本
"""

import asyncio
import requests
import json
from pet_agent import PetAgent
from llm_client import LLMClient, PersonalityType

def test_pet_agent():
    """测试宠物Agent"""
    print("=== 测试宠物Agent ===")
    
    # 初始化LLM客户端和Agent
    llm_client = LLMClient()
    pet_agent = PetAgent(llm_client)
    
    # 测试不同性格的响应
    test_inputs = [
        "你好",
        "摸摸头",
        "今天开心吗",
        "我想你了"
    ]
    
    for personality in PersonalityType:
        print(f"\n--- 测试{personality.value}性格的LangGraph Agent ---")
        for user_input in test_inputs:
            result = pet_agent.invoke(user_input, personality)
            
            # 提取AI响应
            ai_messages = [msg for msg in result["messages"] if hasattr(msg, 'content') and hasattr(msg, '__class__') and 'AIMessage' in str(msg.__class__)]
            response = ai_messages[-1].content if ai_messages else "无响应"
            
            print(f"用户: {user_input}")
            print(f"宠物: {response}")
            print(f"心情: {result.get('mood', 'unknown')}")
            print(f"精力: {result.get('energy', 'unknown')}")
            print()

def test_api_endpoints():
    """测试API端点"""
    print("\n=== 测试API端点 ===")
    
    base_url = "http://127.0.0.1:8000"
    
    # 测试宠物状态
    try:
        response = requests.get(f"{base_url}/pet/status")
        print(f"宠物状态: {response.json()}")
    except Exception as e:
        print(f"无法获取宠物状态: {e}")
        return
    
    # 测试主动问候
    try:
        response = requests.post(f"{base_url}/pet/greeting")
        result = response.json()
        print(f"主动问候: {result['response']}")
    except Exception as e:
        print(f"无法触发主动问候: {e}")
    
    # 测试消息发送
    test_messages = [
        "你好",
        "摸摸头",
        "今天开心吗"
    ]
    
    for message in test_messages:
        try:
            response = requests.post(
                f"{base_url}/message",
                json={"message": message}
            )
            result = response.json()
            print(f"用户: {message}")
            print(f"宠物: {result['response']}")
            print()
        except Exception as e:
            print(f"发送消息失败: {e}")

def test_workflow_components():
    """测试工作流组件"""
    print("\n=== 测试工作流组件 ===")
    
    llm_client = LLMClient()
    pet_agent = PetAgent(llm_client)
    
    # 测试状态管理
    print("测试状态管理...")
    result = pet_agent.invoke("你好", PersonalityType.PLAYFUL)
    
    print(f"状态键: {list(result.keys())}")
    print(f"消息数量: {len(result.get('messages', []))}")
    print(f"心情: {result.get('mood', 'unknown')}")
    print(f"精力: {result.get('energy', 'unknown')}")
    print(f"性格: {result.get('personality', 'unknown')}")

if __name__ == "__main__":
    print("开始LangGraph集成测试...")
    
    # 测试宠物Agent
    test_pet_agent()
    
    # 测试工作流组件
    test_workflow_components()
    
    # 测试API端点
    test_api_endpoints()
    
    print("测试完成！") 