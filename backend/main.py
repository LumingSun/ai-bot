import asyncio
import json
import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
import random

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# 导入LLM客户端和LangGraph Agent
from llm_client import LLMClient, PersonalityType
from pet_agent import PetAgent

# 加载环境变量
load_dotenv()

app = FastAPI(title="Desktop Pet API", version="1.0.0")

# 数据模型
# PersonalityType 现在从 llm_client 导入

class PetType(str, Enum):
    CAT = "cat"
    DOG = "dog"
    RABBIT = "rabbit"
    HAMSTER = "hamster"

class Pet(BaseModel):
    id: int
    name: str
    type: PetType
    personality: PersonalityType
    created_at: datetime
    updated_at: datetime
    currentMessage: str = ""  # 添加当前消息字段

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str

# 数据库管理
class DatabaseManager:
    def __init__(self, db_path: str = "pet.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建宠物表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                personality TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建对话历史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pet_id INTEGER,
                user_input TEXT,
                pet_response TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (pet_id) REFERENCES pets(id)
            )
        ''')
        
        # 创建设置表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_or_create_pet(self) -> Pet:
        """获取或创建宠物"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查是否已有宠物
        cursor.execute('SELECT * FROM pets ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        
        if result:
            pet = Pet(
                id=result[0],
                name=result[1],
                type=result[2],
                personality=result[3],
                created_at=datetime.fromisoformat(result[4]),
                updated_at=datetime.fromisoformat(result[5]),
                currentMessage=""  # 初始为空
            )
        else:
            # 创建新宠物
            pet_type = random.choice(list(PetType))
            personality = random.choice(list(PersonalityType))
            name = self.get_pet_name(pet_type, personality)
            
            cursor.execute('''
                INSERT INTO pets (name, type, personality)
                VALUES (?, ?, ?)
            ''', (name, pet_type.value, personality.value))
            
            pet_id = cursor.lastrowid
            conn.commit()
            
            pet = Pet(
                id=pet_id,
                name=name,
                type=pet_type,
                personality=personality,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                currentMessage=""  # 初始为空
            )
        
        conn.close()
        return pet
    
    def get_pet_name(self, pet_type: PetType, personality: PersonalityType) -> str:
        """根据宠物类型和性格生成名字"""
        names = {
            PetType.CAT: {
                PersonalityType.COLD: ["雪球", "冰凌", "银月"],
                PersonalityType.CLINGY: ["小粘", "糖糖", "爱爱"],
                PersonalityType.PLAYFUL: ["跳跳", "皮皮", "闹闹"],
                PersonalityType.QUIET: ["静静", "默默", "安安"]
            },
            PetType.DOG: {
                PersonalityType.COLD: ["黑豹", "铁拳", "雷神"],
                PersonalityType.CLINGY: ["小乖", "贝贝", "多多"],
                PersonalityType.PLAYFUL: ["旺旺", "球球", "乐乐"],
                PersonalityType.QUIET: ["小灰", "默默", "安安"]
            },
            PetType.RABBIT: {
                PersonalityType.COLD: ["雪白", "银星", "月光"],
                PersonalityType.CLINGY: ["小绒", "毛毛", "软软"],
                PersonalityType.PLAYFUL: ["跳跳", "蹦蹦", "欢欢"],
                PersonalityType.QUIET: ["静静", "默默", "安安"]
            },
            PetType.HAMSTER: {
                PersonalityType.COLD: ["小灰", "银星", "月光"],
                PersonalityType.CLINGY: ["小绒", "毛毛", "软软"],
                PersonalityType.PLAYFUL: ["球球", "圆圆", "胖胖"],
                PersonalityType.QUIET: ["静静", "默默", "安安"]
            }
        }
        
        return random.choice(names[pet_type][personality])
    
    def save_conversation(self, pet_id: int, user_input: str, response: str):
        """保存对话记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (pet_id, user_input, pet_response)
            VALUES (?, ?, ?)
        ''', (pet_id, user_input, response))
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, pet_id: int, limit: int = 10) -> List[Dict]:
        """获取对话历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_input, pet_response, timestamp
            FROM conversations
            WHERE pet_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (pet_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "user_input": row[0],
                "pet_response": row[1],
                "timestamp": row[2]
            }
            for row in results
        ]

# 对话系统
class DialogueManager:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
    
    def generate_response(self, user_input: str, personality: PersonalityType, conversation_history: List[Dict] = None) -> str:
        """使用LLM生成性格化的对话响应"""
        return self.llm_client.generate_response(user_input, personality, conversation_history)
    
    def generate_greeting(self, personality: PersonalityType) -> str:
        """生成主动问候"""
        return self.llm_client.generate_greeting(personality)

# 全局实例
db_manager = DatabaseManager()
llm_client = LLMClient()
dialogue_manager = DialogueManager(llm_client)
pet_agent = PetAgent(llm_client)

# API 路由
@app.get("/")
async def root():
    return {"message": "Desktop Pet API"}

@app.get("/llm/status")
async def get_llm_status():
    """获取LLM服务状态"""
    return {
        "available": llm_client.is_available(),
        "provider": "deepseek" if llm_client.deepseek_api_key else "openai" if llm_client.openai_api_key else "none"
    }

@app.get("/pet/status")
async def get_pet_status():
    """获取宠物状态"""
    pet = db_manager.get_or_create_pet()
    agent_status = pet_agent.get_status()
    
    return {
        "pet_id": pet.id,
        "name": pet.name,
        "type": pet.type,
        "personality": pet.personality,
        "mood": agent_status["mood"],
        "energy": agent_status["energy"],
        "last_interaction": agent_status["last_interaction"]
    }

@app.post("/pet/greeting")
async def trigger_greeting():
    """触发主动问候"""
    pet = db_manager.get_or_create_pet()
    
    # 使用LangGraph Agent生成主动问候
    result = pet_agent.invoke("", pet.personality)  # 空消息触发主动问候
    
    # 提取AI响应
    ai_messages = [msg for msg in result["messages"] if hasattr(msg, 'content') and hasattr(msg, '__class__') and 'AIMessage' in str(msg.__class__)]
    greeting = ai_messages[-1].content if ai_messages else "主人好~"
    
    return MessageResponse(response=greeting)

@app.get("/pet", response_model=Pet)
async def get_pet():
    """获取宠物信息"""
    return db_manager.get_or_create_pet()

@app.post("/message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    """发送消息给宠物（使用LangGraph Agent）"""
    pet = db_manager.get_or_create_pet()
    
    # 使用LangGraph Agent处理消息
    result = pet_agent.invoke(request.message, pet.personality)
    
    # 提取AI响应
    ai_messages = [msg for msg in result["messages"] if hasattr(msg, 'content') and hasattr(msg, '__class__') and 'AIMessage' in str(msg.__class__)]
    response = ai_messages[-1].content if ai_messages else "嗯..."
    
    # 保存对话记录
    db_manager.save_conversation(pet.id, request.message, response)
    
    return MessageResponse(response=response)

@app.get("/conversations")
async def get_conversations(limit: int = 10):
    """获取对话历史"""
    pet = db_manager.get_or_create_pet()
    return db_manager.get_conversation_history(pet.id, limit)

@app.post("/pet/change-type")
async def change_pet_type(pet_type: PetType):
    """改变宠物类型"""
    conn = sqlite3.connect(db_manager.db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE pets 
        SET type = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = (SELECT id FROM pets ORDER BY id DESC LIMIT 1)
    ''', (pet_type.value,))
    
    conn.commit()
    conn.close()
    
    return {"message": f"宠物类型已更改为 {pet_type.value}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 