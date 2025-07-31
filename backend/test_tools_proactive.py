#!/usr/bin/env python3
"""
工具和主动互动系统测试脚本
"""

import asyncio
import requests
import json
import time
from tools import ToolManager
from proactive_system import ProactiveSystem
from llm_client import PersonalityType

def test_tools():
    """测试工具系统"""
    print("=== 测试工具系统 ===")
    
    tool_manager = ToolManager()
    
    # 测试时间工具
    print("\n--- 测试时间工具 ---")
    time_result = tool_manager.execute_tool("get_time")
    print(f"时间工具: {time_result.message}")
    print(f"数据: {time_result.data}")
    
    # 测试天气工具
    print("\n--- 测试天气工具 ---")
    weather_result = tool_manager.execute_tool("get_weather", location="北京")
    print(f"天气工具: {weather_result.message}")
    print(f"数据: {weather_result.data}")
    
    # 测试健康工具
    print("\n--- 测试健康工具 ---")
    health_result = tool_manager.execute_tool("get_health")
    print(f"健康工具: {health_result.message}")
    print(f"数据: {health_result.data}")
    
    # 测试喂食工具
    print("\n--- 测试喂食工具 ---")
    feed_result = tool_manager.execute_tool("feed_pet")
    print(f"喂食工具: {feed_result.message}")
    print(f"数据: {feed_result.data}")
    
    # 测试玩耍工具
    print("\n--- 测试玩耍工具 ---")
    play_result = tool_manager.execute_tool("play_with_pet")
    print(f"玩耍工具: {play_result.message}")
    print(f"数据: {play_result.data}")
    
    # 测试提醒工具
    print("\n--- 测试提醒工具 ---")
    add_result = tool_manager.execute_tool("add_reminder", title="测试提醒", time="15:00", description="这是一个测试提醒")
    print(f"添加提醒: {add_result.message}")
    
    reminder_result = tool_manager.execute_tool("get_reminders")
    print(f"获取提醒: {reminder_result.message}")
    print(f"提醒数据: {reminder_result.data}")
    
    # 获取可用工具列表
    print("\n--- 可用工具列表 ---")
    available_tools = tool_manager.get_available_tools()
    print(f"可用工具: {available_tools}")

def test_proactive_system():
    """测试主动互动系统"""
    print("\n=== 测试主动互动系统 ===")
    
    tool_manager = ToolManager()
    
    # 测试不同性格的主动互动系统
    for personality in PersonalityType:
        print(f"\n--- 测试{personality.value}性格的主动互动系统 ---")
        
        proactive_system = ProactiveSystem(tool_manager, personality)
        
        # 测试各种事件
        events = ["time_greeting", "health_check", "weather_comment", "lonely_check", "energy_check"]
        
        for event_type in events:
            message = proactive_system.trigger_manual_event(event_type)
            if message:
                print(f"{event_type}: {message}")
            else:
                print(f"{event_type}: 无消息")

def test_api_endpoints():
    """测试API端点"""
    print("\n=== 测试API端点 ===")
    
    base_url = "http://127.0.0.1:8000"
    
    # 测试工具执行
    try:
        response = requests.post(f"{base_url}/tools/execute", params={"tool_name": "get_time"})
        print(f"工具执行结果: {response.json()}")
    except Exception as e:
        print(f"工具执行失败: {e}")
    
    # 测试获取可用工具
    try:
        response = requests.get(f"{base_url}/tools/available")
        print(f"可用工具: {response.json()}")
    except Exception as e:
        print(f"获取工具列表失败: {e}")
    
    # 测试主动事件触发
    try:
        response = requests.post(f"{base_url}/proactive/trigger", params={"event_type": "time_greeting"})
        print(f"主动事件触发: {response.json()}")
    except Exception as e:
        print(f"主动事件触发失败: {e}")
    
    # 测试启动主动互动系统
    try:
        response = requests.post(f"{base_url}/proactive/start")
        print(f"启动主动互动系统: {response.json()}")
    except Exception as e:
        print(f"启动主动互动系统失败: {e}")

def test_integrated_workflow():
    """测试集成工作流"""
    print("\n=== 测试集成工作流 ===")
    
    # 测试包含工具的消息处理
    test_messages = [
        "现在几点了？",
        "今天天气怎么样？",
        "我的健康状态如何？",
        "我饿了，给我点吃的",
        "陪我玩一会儿",
        "有什么提醒吗？"
    ]
    
    base_url = "http://127.0.0.1:8000"
    
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
    print("开始工具和主动互动系统测试...")
    
    # 测试工具系统
    test_tools()
    
    # 测试主动互动系统
    test_proactive_system()
    
    # 测试API端点
    test_api_endpoints()
    
    # 测试集成工作流
    test_integrated_workflow()
    
    print("测试完成！") 