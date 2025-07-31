#!/bin/bash

# 桌面电子宠物系统启动脚本

echo "🐾 启动桌面电子宠物系统..."

# 检查 Node.js 版本
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js，请先安装 Node.js 18+"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ 错误: Node.js 版本过低，需要 18+ 版本"
    exit 1
fi

# 检查 Python 版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3，请先安装 Python 3.8+"
    exit 1
fi

# 检查依赖是否安装
if [ ! -d "node_modules" ]; then
    echo "📦 安装前端依赖..."
    npm install
fi

if [ ! -d "backend/__pycache__" ] && [ ! -f "backend/pet.db" ]; then
    echo "🐍 安装后端依赖..."
    cd backend
    pip3 install -r requirements.txt
    cd ..
fi

# 检查资源文件
if [ ! -f "assets/cat.png" ]; then
    echo "⚠️  警告: 未找到宠物图片文件，请将图片文件放置在 assets/ 目录中"
    echo "   需要的文件: cat.png, dog.png, rabbit.png, hamster.png"
fi

echo "🚀 启动应用..."

# 启动 Python 后端
echo "🐍 启动 Python 后端..."
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 3

# 启动前端
echo "⚛️  启动前端..."
npm run dev

# 清理进程
kill $BACKEND_PID 2>/dev/null 