"""
主动互动系统
"""

import asyncio
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
import random

from tools import ToolManager
from llm_client import PersonalityType

@dataclass
class ProactiveEvent:
    """主动事件"""
    event_type: str
    message: str
    priority: int  # 1-5，5最高
    conditions: Dict
    cooldown: int  # 冷却时间（秒）

class ProactiveSystem:
    """主动互动系统"""
    
    def __init__(self, tool_manager: ToolManager, personality: PersonalityType):
        self.tool_manager = tool_manager
        self.personality = personality
        self.last_events = {}  # 记录上次事件时间
        self.event_handlers = {}  # 事件处理器
        self.is_running = False
        self.thread = None
        
        # 初始化事件处理器
        self._init_event_handlers()
    
    def _init_event_handlers(self):
        """初始化事件处理器"""
        self.event_handlers = {
            "time_greeting": self._handle_time_greeting,
            "health_check": self._handle_health_check,
            "weather_comment": self._handle_weather_comment,
            "reminder_check": self._handle_reminder_check,
            "lonely_check": self._handle_lonely_check,
            "energy_check": self._handle_energy_check
        }
    
    def start(self):
        """启动主动互动系统"""
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()
            print("主动互动系统已启动")
    
    def stop(self):
        """停止主动互动系统"""
        self.is_running = False
        if self.thread:
            self.thread.join()
        print("主动互动系统已停止")
    
    def _run_loop(self):
        """运行主循环"""
        while self.is_running:
            try:
                # 检查各种事件
                events = self._check_events()
                
                # 处理事件
                for event in events:
                    self._process_event(event)
                
                # 等待一段时间
                time.sleep(30)  # 每30秒检查一次
                
            except Exception as e:
                print(f"主动互动系统错误: {e}")
                time.sleep(60)  # 出错时等待更长时间
    
    def _check_events(self) -> List[ProactiveEvent]:
        """检查需要触发的事件"""
        events = []
        now = datetime.now()
        
        # 时间问候检查
        if self._should_time_greeting(now):
            events.append(ProactiveEvent(
                event_type="time_greeting",
                message="时间问候",
                priority=3,
                conditions={"time": now},
                cooldown=3600  # 1小时冷却
            ))
        
        # 健康检查
        if self._should_health_check(now):
            events.append(ProactiveEvent(
                event_type="health_check",
                message="健康检查",
                priority=4,
                conditions={"time": now},
                cooldown=1800  # 30分钟冷却
            ))
        
        # 天气评论
        if self._should_weather_comment(now):
            events.append(ProactiveEvent(
                event_type="weather_comment",
                message="天气评论",
                priority=2,
                conditions={"time": now},
                cooldown=7200  # 2小时冷却
            ))
        
        # 提醒检查
        if self._should_reminder_check(now):
            events.append(ProactiveEvent(
                event_type="reminder_check",
                message="提醒检查",
                priority=5,
                conditions={"time": now},
                cooldown=900  # 15分钟冷却
            ))
        
        # 孤独检查（根据性格）
        if self._should_lonely_check(now):
            events.append(ProactiveEvent(
                event_type="lonely_check",
                message="孤独检查",
                priority=4,
                conditions={"time": now, "personality": self.personality},
                cooldown=1800  # 30分钟冷却
            ))
        
        # 精力检查
        if self._should_energy_check(now):
            events.append(ProactiveEvent(
                event_type="energy_check",
                message="精力检查",
                priority=3,
                conditions={"time": now},
                cooldown=1200  # 20分钟冷却
            ))
        
        return events
    
    def _should_time_greeting(self, now: datetime) -> bool:
        """检查是否应该进行时间问候"""
        last_time = self.last_events.get("time_greeting")
        if last_time and (now - last_time).total_seconds() < 3600:
            return False
        
        # 在特定时间点问候
        hour = now.hour
        return hour in [8, 12, 18, 22]  # 早上8点，中午12点，晚上6点，晚上10点
    
    def _should_health_check(self, now: datetime) -> bool:
        """检查是否应该进行健康检查"""
        last_time = self.last_events.get("health_check")
        if last_time and (now - last_time).total_seconds() < 1800:
            return False
        
        # 每30分钟检查一次健康状态
        return True
    
    def _should_weather_comment(self, now: datetime) -> bool:
        """检查是否应该评论天气"""
        last_time = self.last_events.get("weather_comment")
        if last_time and (now - last_time).total_seconds() < 7200:
            return False
        
        # 在早上和晚上评论天气
        hour = now.hour
        return hour in [7, 19]
    
    def _should_reminder_check(self, now: datetime) -> bool:
        """检查是否应该检查提醒"""
        last_time = self.last_events.get("reminder_check")
        if last_time and (now - last_time).total_seconds() < 900:
            return False
        
        # 每15分钟检查一次提醒
        return True
    
    def _should_lonely_check(self, now: datetime) -> bool:
        """检查是否应该进行孤独检查"""
        last_time = self.last_events.get("lonely_check")
        if last_time and (now - last_time).total_seconds() < 1800:
            return False
        
        # 根据性格调整孤独检查频率
        if self.personality == PersonalityType.CLINGY:
            return True  # 粘人型经常检查
        elif self.personality == PersonalityType.COLD:
            return random.random() < 0.3  # 高冷型很少检查
        else:
            return random.random() < 0.6  # 其他性格中等频率
    
    def _should_energy_check(self, now: datetime) -> bool:
        """检查是否应该进行精力检查"""
        last_time = self.last_events.get("energy_check")
        if last_time and (now - last_time).total_seconds() < 1200:
            return False
        
        # 每20分钟检查一次精力
        return True
    
    def _process_event(self, event: ProactiveEvent):
        """处理事件"""
        handler = self.event_handlers.get(event.event_type)
        if handler:
            try:
                message = handler(event.conditions)
                if message:
                    # 这里可以调用回调函数发送消息
                    print(f"主动事件 [{event.event_type}]: {message}")
                
                # 更新最后事件时间
                self.last_events[event.event_type] = datetime.now()
                
            except Exception as e:
                print(f"处理事件 {event.event_type} 时出错: {e}")
    
    def _handle_time_greeting(self, conditions: Dict) -> Optional[str]:
        """处理时间问候"""
        time_tool = self.tool_manager.time_tool
        greeting = time_tool.get_time_greeting()
        
        # 根据性格调整问候语
        if self.personality == PersonalityType.CLINGY:
            return f"{greeting}主人！想死你了~"
        elif self.personality == PersonalityType.COLD:
            return f"{greeting}，你来了。"
        elif self.personality == PersonalityType.PLAYFUL:
            return f"{greeting}主人！新的一天开始啦！✨"
        else:  # QUIET
            return f"{greeting}..."
    
    def _handle_health_check(self, conditions: Dict) -> Optional[str]:
        """处理健康检查"""
        health_result = self.tool_manager.execute_tool("get_health")
        if not health_result.success:
            return None
        
        health_data = health_result.data
        hunger = health_data.get("hunger", 100)
        happiness = health_data.get("happiness", 100)
        
        # 根据健康状态生成消息
        if hunger > 80:
            if self.personality == PersonalityType.CLINGY:
                return "主人，我有点饿了，能给我点吃的吗？"
            elif self.personality == PersonalityType.COLD:
                return "哼，有点饿了。"
            else:
                return "我有点饿了..."
        
        if happiness < 50:
            if self.personality == PersonalityType.CLINGY:
                return "主人，我有点不开心，能陪陪我吗？"
            elif self.personality == PersonalityType.PLAYFUL:
                return "好无聊啊，想和主人一起玩！"
            else:
                return "心情不太好..."
        
        return None
    
    def _handle_weather_comment(self, conditions: Dict) -> Optional[str]:
        """处理天气评论"""
        weather_result = self.tool_manager.execute_tool("get_weather")
        if not weather_result.success:
            return None
        
        weather_data = weather_result.data
        condition = weather_data.get("condition", "晴天")
        
        # 根据天气和性格生成评论
        if condition == "晴天":
            if self.personality == PersonalityType.PLAYFUL:
                return "今天天气真好！想和主人一起出去玩！"
            else:
                return "天气不错。"
        elif condition == "小雨":
            if self.personality == PersonalityType.QUIET:
                return "下雨天，很安静。"
            else:
                return "下雨了，有点潮湿。"
        else:
            return "天气一般。"
    
    def _handle_reminder_check(self, conditions: Dict) -> Optional[str]:
        """处理提醒检查"""
        reminder_result = self.tool_manager.execute_tool("get_reminders")
        if not reminder_result.success:
            return None
        
        reminders = reminder_result.data.get("reminders", [])
        if reminders:
            if self.personality == PersonalityType.CLINGY:
                return f"主人，您还有{len(reminders)}个提醒没有完成哦~"
            else:
                return f"您有{len(reminders)}个待办提醒。"
        
        return None
    
    def _handle_lonely_check(self, conditions: Dict) -> Optional[str]:
        """处理孤独检查"""
        if self.personality == PersonalityType.CLINGY:
            return "主人，我好想你啊，什么时候来看我？"
        elif self.personality == PersonalityType.COLD:
            return random.choice(["哼", "嗯", "..."])
        elif self.personality == PersonalityType.PLAYFUL:
            return "好无聊啊，想和主人一起玩！"
        else:  # QUIET
            return "主人..."
    
    def _handle_energy_check(self, conditions: Dict) -> Optional[str]:
        """处理精力检查"""
        health_result = self.tool_manager.execute_tool("get_health")
        if not health_result.success:
            return None
        
        energy = health_result.data.get("energy", 100)
        
        if energy < 30:
            if self.personality == PersonalityType.PLAYFUL:
                return "好累啊...让我休息一下下~ 😴"
            elif self.personality == PersonalityType.CLINGY:
                return "主人，我有点累了，但是还想和你在一起... 💤"
            else:
                return "有点累了。"
        
        return None
    
    def trigger_manual_event(self, event_type: str) -> Optional[str]:
        """手动触发事件"""
        if event_type in self.event_handlers:
            conditions = {"time": datetime.now()}
            return self.event_handlers[event_type](conditions)
        return None 