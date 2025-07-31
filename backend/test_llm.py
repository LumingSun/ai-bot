#!/usr/bin/env python3
"""
LLM集成测试脚本
"""

import asyncio
import requests
import json
from llm_client import LLMClient, PersonalityType

def test_llm_client():
    """测试LLM客户端"""
    print("=== 测试LLM客户端 ===")
    
    # 初始化客户端
    client = LLMClient()
    
    # 检查服务状态
    print(f"LLM服务可用: {client.is_available()}")
    print(f"DeepSeek API密钥: {'已配置' if client.deepseek_api_key else '未配置'}")
    print(f"OpenAI API密钥: {'已配置' if client.openai_api_key else '未配置'}")
    
    # 测试不同性格的响应
    test_inputs = [
        "你好",
        "摸摸头",
        "今天开心吗",
        "我想你了"
    ]
    
    for personality in PersonalityType:
        print(f"\n--- 测试{personality.value}性格 ---")
        for user_input in test_inputs:
            response = client.generate_response(user_input, personality)
            print(f"用户: {user_input}")
            print(f"宠物: {response}")
            print()

def test_api_endpoints():
    """测试API端点"""
    print("\n=== 测试API端点 ===")
    
    base_url = "http://127.0.0.1:8000"
    
    # 测试LLM状态
    try:
        response = requests.get(f"{base_url}/llm/status")
        print(f"LLM状态: {response.json()}")
    except Exception as e:
        print(f"无法连接到API: {e}")
        return
    
    # 测试发送消息
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

if __name__ == "__main__":
    print("开始LLM集成测试...")
    
    # 测试LLM客户端
    test_llm_client()
    
    # 测试API端点
    test_api_endpoints()
    
    print("测试完成！") 