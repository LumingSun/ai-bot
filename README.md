# 桌面电子宠物系统

一个基于 Electron + Python 的智能桌面电子宠物系统，支持个性化性格和智能对话。

## 功能特性

### 第一阶段 (MVP)
- ✅ 桌面悬浮窗口
- ✅ 静态宠物图片显示
- ✅ 简单对话功能
- ✅ 基础性格系统
- ✅ 拖拽移动
- ✅ 透明度调节
- ✅ 设置面板

### 计划功能
- 🔄 3D 动画效果
- 🔄 大模型集成
- 🔄 主动互动系统
- 🔄 LangGraph 框架集成
- 🔄 MCP Server 支持

## 技术栈

### 前端
- **Electron**: 桌面应用框架
- **React**: 用户界面
- **Vite**: 构建工具

### 后端
- **Python**: 业务逻辑
- **FastAPI**: Web API 框架
- **SQLite**: 数据存储
- **LangGraph**: 工作流管理

## 安装和运行

### 环境要求
- Node.js 18+
- Python 3.8+
- macOS 10.15+

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd desktop-pet
```

2. **安装前端依赖**
```bash
npm install
```

3. **安装后端依赖**
```bash
cd backend
pip install -r requirements.txt
cd ..
```

4. **启动开发环境**
```bash
npm run dev
```

### 构建生产版本
```bash
npm run build
npm run dist
```

## 使用说明

### 基本操作
- **拖拽**: 点击并拖拽宠物移动位置
- **双击**: 显示/隐藏设置面板
- **右键**: 显示设置面板

### 设置面板功能
- **透明度调节**: 调整窗口透明度
- **消息输入**: 与宠物对话
- **快捷按钮**: 快速发送常用消息

### 宠物性格
系统支持四种性格类型：
- **高冷型**: 独立、优雅、偶尔互动
- **粘人型**: 依赖性强、频繁互动、需要关注
- **活泼型**: 精力充沛、爱玩、积极互动
- **安静型**: 温和、安静、喜欢陪伴

## 项目结构

```
desktop-pet/
├── main.js                 # Electron 主进程
├── preload.js             # 预加载脚本
├── package.json           # 前端依赖配置
├── vite.config.js         # Vite 配置
├── index.html             # HTML 入口
├── src/                   # 前端源码
│   ├── main.jsx          # React 入口
│   ├── App.jsx           # 主应用组件
│   ├── components/       # 组件目录
│   └── hooks/           # 自定义 Hooks
├── backend/              # 后端源码
│   ├── main.py          # FastAPI 应用
│   └── requirements.txt  # Python 依赖
└── assets/              # 静态资源
    ├── cat.png          # 猫咪图片
    ├── dog.png          # 狗狗图片
    ├── rabbit.png       # 兔子图片
    └── hamster.png      # 仓鼠图片
```

## 开发指南

### 添加新的宠物类型
1. 在 `backend/main.py` 中添加新的 `PetType`
2. 在 `src/components/Pet.jsx` 中添加对应的图片路径
3. 在 `backend/main.py` 的 `get_pet_name` 方法中添加名字映射

### 扩展性格系统
1. 在 `backend/main.py` 中添加新的 `PersonalityType`
2. 在 `DialogueManager` 中添加对应的响应模板
3. 在前端组件中添加对应的样式处理

### 集成大模型
1. 在 `backend/main.py` 中添加 OpenAI/Claude API 集成
2. 修改 `DialogueManager` 使用大模型生成响应
3. 添加错误处理和重试机制

## 配置说明

### 环境变量
创建 `.env` 文件：
```env
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 应用配置
主要配置项在 `backend/main.py` 中：
- 数据库路径
- API 端口
- 宠物类型和性格
- 对话响应模板

## 故障排除

### 常见问题

1. **Python 后端启动失败**
   - 检查 Python 版本 (需要 3.8+)
   - 确认依赖安装完整
   - 检查端口 8000 是否被占用

2. **Electron 应用无法启动**
   - 检查 Node.js 版本 (需要 18+)
   - 确认前端依赖安装完整
   - 检查端口 5173 是否被占用

3. **宠物图片不显示**
   - 确认 `assets` 目录下有对应的图片文件
   - 检查图片文件权限

4. **对话功能异常**
   - 确认 Python 后端正常运行
   - 检查网络连接
   - 查看控制台错误信息

### 调试模式
```bash
# 启动调试模式
npm run dev
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 更新日志

### v1.0.0 (MVP)
- 基础桌面悬浮窗口
- 静态宠物图片显示
- 简单对话功能
- 基础性格系统
- 拖拽和透明度控制
- 设置面板 