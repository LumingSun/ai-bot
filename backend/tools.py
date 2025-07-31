"""
宠物Agent的工具系统
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import random

@dataclass
class ToolResult:
    """工具执行结果"""
    success: bool
    data: Dict
    message: str

class TimeTool:
    """时间工具"""
    
    def get_current_time(self) -> ToolResult:
        """获取当前时间"""
        now = datetime.now()
        return ToolResult(
            success=True,
            data={
                "hour": now.hour,
                "minute": now.minute,
                "weekday": now.strftime("%A"),
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M"),
                "is_morning": 6 <= now.hour < 12,
                "is_afternoon": 12 <= now.hour < 18,
                "is_evening": 18 <= now.hour < 22,
                "is_night": 22 <= now.hour or now.hour < 6
            },
            message=f"现在是{now.strftime('%H:%M')}，{now.strftime('%A')}"
        )
    
    def get_time_greeting(self) -> str:
        """根据时间生成问候语"""
        now = datetime.now()
        hour = now.hour
        
        if 6 <= hour < 12:
            return "早上好"
        elif 12 <= hour < 18:
            return "下午好"
        elif 18 <= hour < 22:
            return "晚上好"
        else:
            return "夜深了"

class WeatherTool:
    """天气工具（模拟）"""
    
    def get_weather(self, location: str = "北京") -> ToolResult:
        """获取天气信息（模拟数据）"""
        # 模拟天气数据
        weather_data = {
            "北京": {"temp": 22, "condition": "晴天", "humidity": 45},
            "上海": {"temp": 25, "condition": "多云", "humidity": 60},
            "深圳": {"temp": 28, "condition": "小雨", "humidity": 75},
            "杭州": {"temp": 24, "condition": "晴天", "humidity": 50}
        }
        
        weather = weather_data.get(location, {"temp": 20, "condition": "晴天", "humidity": 50})
        
        return ToolResult(
            success=True,
            data=weather,
            message=f"{location}今天{weather['condition']}，温度{weather['temp']}°C，湿度{weather['humidity']}%"
        )
    
    def get_weather_mood(self, weather_data: Dict) -> str:
        """根据天气生成心情描述"""
        condition = weather_data.get("condition", "晴天")
        temp = weather_data.get("temp", 20)
        
        if condition == "晴天":
            return "天气真好，心情也不错"
        elif condition == "多云":
            return "天气温和，很舒服"
        elif condition == "小雨":
            return "下雨天，有点安静"
        else:
            return "天气一般"

class ReminderTool:
    """提醒工具"""
    
    def __init__(self):
        self.reminders = []
    
    def add_reminder(self, title: str, time: str, description: str = "") -> ToolResult:
        """添加提醒"""
        reminder = {
            "id": len(self.reminders) + 1,
            "title": title,
            "time": time,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "completed": False
        }
        
        self.reminders.append(reminder)
        
        return ToolResult(
            success=True,
            data=reminder,
            message=f"已添加提醒：{title}，时间：{time}"
        )
    
    def get_reminders(self) -> ToolResult:
        """获取所有提醒"""
        active_reminders = [r for r in self.reminders if not r["completed"]]
        
        return ToolResult(
            success=True,
            data={"reminders": active_reminders},
            message=f"您有{len(active_reminders)}个待办提醒"
        )
    
    def complete_reminder(self, reminder_id: int) -> ToolResult:
        """完成提醒"""
        for reminder in self.reminders:
            if reminder["id"] == reminder_id:
                reminder["completed"] = True
                return ToolResult(
                    success=True,
                    data=reminder,
                    message=f"已完成提醒：{reminder['title']}"
                )
        
        return ToolResult(
            success=False,
            data={},
            message="未找到指定提醒"
        )

class HealthTool:
    """健康工具"""
    
    def __init__(self):
        self.health_status = {
            "hunger": 100,
            "thirst": 100,
            "happiness": 100,
            "energy": 100,
            "last_feed": None,
            "last_play": None
        }
    
    def get_health_status(self) -> ToolResult:
        """获取健康状态"""
        return ToolResult(
            success=True,
            data=self.health_status,
            message=f"健康状态：饥饿{self.health_status['hunger']}%，口渴{self.health_status['thirst']}%，快乐{self.health_status['happiness']}%，精力{self.health_status['energy']}%"
        )
    
    def feed_pet(self) -> ToolResult:
        """喂食宠物"""
        self.health_status["hunger"] = min(100, self.health_status["hunger"] + 30)
        self.health_status["happiness"] = min(100, self.health_status["happiness"] + 10)
        self.health_status["last_feed"] = datetime.now().isoformat()
        
        return ToolResult(
            success=True,
            data=self.health_status,
            message="宠物吃饱了，很开心！"
        )
    
    def play_with_pet(self) -> ToolResult:
        """和宠物玩耍"""
        self.health_status["happiness"] = min(100, self.health_status["happiness"] + 20)
        self.health_status["energy"] = max(0, self.health_status["energy"] - 10)
        self.health_status["last_play"] = datetime.now().isoformat()
        
        return ToolResult(
            success=True,
            data=self.health_status,
            message="和宠物玩耍很开心！"
        )
    
    def update_health(self):
        """更新健康状态（随时间衰减）"""
        now = datetime.now()
        
        # 饥饿度随时间增加
        if self.health_status["hunger"] < 100:
            self.health_status["hunger"] = min(100, self.health_status["hunger"] + 1)
        
        # 口渴度随时间增加
        if self.health_status["thirst"] < 100:
            self.health_status["thirst"] = min(100, self.health_status["thirst"] + 1)
        
        # 快乐度随时间减少
        if self.health_status["happiness"] > 0:
            self.health_status["happiness"] = max(0, self.health_status["happiness"] - 0.5)
        
        # 精力随时间恢复
        if self.health_status["energy"] < 100:
            self.health_status["energy"] = min(100, self.health_status["energy"] + 0.5)

class ToolManager:
    """工具管理器"""
    
    def __init__(self):
        self.time_tool = TimeTool()
        self.weather_tool = WeatherTool()
        self.reminder_tool = ReminderTool()
        self.health_tool = HealthTool()
        
        self.tools = {
            "get_time": self.time_tool.get_current_time,
            "get_weather": self.weather_tool.get_weather,
            "add_reminder": self.reminder_tool.add_reminder,
            "get_reminders": self.reminder_tool.get_reminders,
            "complete_reminder": self.reminder_tool.complete_reminder,
            "get_health": self.health_tool.get_health_status,
            "feed_pet": self.health_tool.feed_pet,
            "play_with_pet": self.health_tool.play_with_pet
        }
    
    def execute_tool(self, tool_name: str, **kwargs) -> ToolResult:
        """执行工具"""
        if tool_name not in self.tools:
            return ToolResult(
                success=False,
                data={},
                message=f"未知工具：{tool_name}"
            )
        
        try:
            result = self.tools[tool_name](**kwargs)
            return result
        except Exception as e:
            return ToolResult(
                success=False,
                data={},
                message=f"工具执行失败：{str(e)}"
            )
    
    def get_available_tools(self) -> List[str]:
        """获取可用工具列表"""
        return list(self.tools.keys())
    
    def update_health_status(self):
        """更新健康状态"""
        self.health_tool.update_health() 