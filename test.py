#!/usr/bin/env python3
"""
桌面电子宠物系统测试脚本
"""

import requests
import json
import time
import sys

def test_backend():
    """测试后端 API"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 开始测试后端 API...")
    
    try:
        # 测试根路径
        print("1. 测试根路径...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ 根路径正常")
        else:
            print(f"   ❌ 根路径失败: {response.status_code}")
            return False
        
        # 测试获取宠物信息
        print("2. 测试获取宠物信息...")
        response = requests.get(f"{base_url}/pet")
        if response.status_code == 200:
            pet_data = response.json()
            print(f"   ✅ 宠物信息: {pet_data['name']} ({pet_data['type']}) - {pet_data['personality']}")
        else:
            print(f"   ❌ 获取宠物信息失败: {response.status_code}")
            return False
        
        # 测试发送消息
        print("3. 测试发送消息...")
        test_messages = ["你好", "摸摸头", "我喜欢你"]
        
        for message in test_messages:
            response = requests.post(f"{base_url}/message", 
                                  json={"message": message})
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ 消息 '{message}' -> '{data['response']}'")
            else:
                print(f"   ❌ 发送消息失败: {response.status_code}")
                return False
        
        # 测试获取对话历史
        print("4. 测试获取对话历史...")
        response = requests.get(f"{base_url}/conversations")
        if response.status_code == 200:
            history = response.json()
            print(f"   ✅ 对话历史: {len(history)} 条记录")
        else:
            print(f"   ❌ 获取对话历史失败: {response.status_code}")
            return False
        
        print("🎉 所有测试通过！")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务，请确保后端正在运行")
        return False
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False

def test_frontend():
    """测试前端功能"""
    print("\n🧪 开始测试前端功能...")
    
    try:
        # 检查必要的文件是否存在
        required_files = [
            "main.js",
            "preload.js", 
            "package.json",
            "src/App.jsx",
            "src/components/Pet.jsx",
            "src/components/ChatBubble.jsx",
            "src/components/SettingsPanel.jsx"
        ]
        
        missing_files = []
        for file in required_files:
            try:
                with open(file, 'r') as f:
                    pass
                print(f"   ✅ {file}")
            except FileNotFoundError:
                print(f"   ❌ {file} - 文件不存在")
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ 缺少 {len(missing_files)} 个文件")
            return False
        
        print("🎉 前端文件检查通过！")
        return True
        
    except Exception as e:
        print(f"❌ 前端测试过程中出现错误: {e}")
        return False

def main():
    """主测试函数"""
    print("🐾 桌面电子宠物系统测试")
    print("=" * 50)
    
    # 测试后端
    backend_ok = test_backend()
    
    # 测试前端
    frontend_ok = test_frontend()
    
    print("\n" + "=" * 50)
    if backend_ok and frontend_ok:
        print("🎉 所有测试通过！系统可以正常运行")
        print("\n启动命令:")
        print("  npm run dev")
        print("  或者")
        print("  ./start.sh")
    else:
        print("❌ 部分测试失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main() 