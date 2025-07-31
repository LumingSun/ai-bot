# 手动启动指南

由于自动启动脚本可能遇到依赖问题，这里提供手动启动的步骤：

## 方法一：分步启动

### 1. 安装依赖
```bash
# 安装前端依赖
npm install

# 安装后端依赖
cd backend
pip3 install -r requirements.txt
cd ..
```

### 2. 启动后端
```bash
# 在项目根目录执行
cd backend
python3 main.py
```
保持这个终端窗口打开，后端服务会在 http://127.0.0.1:8000 运行

### 3. 启动前端（新开一个终端）
```bash
# 在项目根目录执行
npm run dev
```

### 4. 启动 Electron 应用（再开一个终端）
```bash
# 在项目根目录执行
npm run dev:electron
```

## 方法二：使用简化脚本

如果上面的方法不行，可以尝试：

```bash
./start-simple.sh
```

## 方法三：直接启动 Electron

如果 Vite 开发服务器有问题，可以直接启动 Electron：

```bash
npm start
```

## 故障排除

### 问题 1: npm install 失败
```bash
# 清除 npm 缓存
npm cache clean --force

# 删除 node_modules 重新安装
rm -rf node_modules package-lock.json
npm install
```

### 问题 2: Python 依赖安装失败
```bash
# 升级 pip
pip3 install --upgrade pip

# 使用国内镜像
pip3 install -r backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 问题 3: 端口被占用
```bash
# 检查端口占用
lsof -i :8000  # 检查后端端口
lsof -i :5173  # 检查前端端口

# 杀死占用进程
kill -9 <PID>
```

### 问题 4: Electron 无法启动
```bash
# 检查 Electron 是否正确安装
npx electron --version

# 重新安装 Electron
npm install electron --save-dev
```

## 验证系统是否正常

### 1. 测试后端 API
```bash
# 测试后端是否响应
curl http://127.0.0.1:8000/

# 测试获取宠物信息
curl http://127.0.0.1:8000/pet
```

### 2. 测试前端
```bash
# 启动 Vite 开发服务器
npm run dev

# 在浏览器中访问 http://localhost:5173
```

### 3. 测试 Electron
```bash
# 启动 Electron
npm run dev:electron
```

## 预期结果

成功启动后，您应该看到：
1. 后端服务在 http://127.0.0.1:8000 运行
2. 前端开发服务器在 http://localhost:5173 运行
3. Electron 应用窗口显示桌面宠物

## 如果仍然有问题

1. 检查 Node.js 版本：`node --version` (需要 18+)
2. 检查 Python 版本：`python3 --version` (需要 3.8+)
3. 查看错误日志
4. 尝试重启终端或重启电脑

## 快速测试

运行测试脚本检查系统状态：
```bash
python3 test.py
``` 