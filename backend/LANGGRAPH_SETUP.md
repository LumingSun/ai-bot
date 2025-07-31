# LangGraph集成配置说明

## 概述

本项目已集成LangGraph框架，实现了基于图工作流的宠物Agent系统。LangGraph提供了强大的状态管理、条件分支和工具调用能力。

## LangGraph架构

### 核心组件

1. **StateGraph（状态图）**
   - 管理宠物Agent的状态
   - 定义节点间的数据流
   - 支持条件分支和循环

2. **Nodes（节点）**
   - `analyze_input`: 分析用户输入
   - `generate_response`: 生成AI响应
   - `update_mood`: 更新宠物心情
   - `check_energy`: 检查精力状态
   - `proactive_greeting`: 主动问候

3. **Edges（边）**
   - **Required Edges**: 固定流程路径
   - **Conditional Edges**: 基于条件的动态路由

### 工作流程图

```
START
  ↓
analyze_input
  ↓ (条件分支)
├─ proactive_greeting (主动问候)
└─ generate_response (生成响应)
  ↓
update_mood (更新心情)
  ↓
check_energy (检查精力)
  ↓
END
```

## 状态管理

### PetState结构

```python
class PetState(TypedDict):
    messages: Annotated[list, "add_messages"]  # 对话消息
    personality: PersonalityType  # 宠物性格
    current_time: str  # 当前时间
    mood: str  # 宠物心情
    energy: int  # 宠物精力值
    last_interaction: str  # 最后互动时间
    context: dict  # 上下文信息
```

### 状态更新机制

1. **消息管理**: 使用`add_messages` reducer自动合并消息
2. **心情系统**: 基于互动历史动态调整
3. **精力系统**: 模拟真实宠物的精力消耗
4. **时间追踪**: 记录最后互动时间

## 节点功能详解

### 1. analyze_input节点

**功能**: 分析用户输入，提取意图和上下文

**处理逻辑**:
- 分类用户输入（问候、互动、情感、告别等）
- 提取用户意图
- 更新上下文信息

**输入类型分类**:
- `greeting`: 问候类
- `physical_interaction`: 身体互动
- `emotional`: 情感表达
- `farewell`: 告别类
- `general`: 一般对话

### 2. generate_response节点

**功能**: 使用LLM生成性格化响应

**处理逻辑**:
- 获取用户输入
- 调用LLM生成响应
- 更新互动时间
- 添加AI消息到状态

### 3. update_mood节点

**功能**: 基于互动更新宠物心情和精力

**心情更新规则**:
- 积极互动（摸摸、抱抱、喜欢）→ 心情提升
- 消极互动 → 根据性格调整心情
- 粘人型宠物更容易感到孤独

**精力系统**:
- 积极互动 → 精力+5~10
- 消极互动 → 精力-1~5
- 精力<30时触发休息提醒

### 4. check_energy节点

**功能**: 检查精力状态，必要时提醒休息

**处理逻辑**:
- 检查精力值
- 精力过低时生成休息提醒
- 根据性格调整提醒风格

### 5. proactive_greeting节点

**功能**: 生成主动问候

**触发条件**:
- 超过5分钟没有互动
- 用户主动触发问候

## 条件分支系统

### should_greet_condition

**功能**: 判断是否应该主动问候

**决策逻辑**:
1. 检查是否有用户消息
2. 计算距离上次互动的时间
3. 超过5分钟触发主动问候

**返回值**:
- `"proactive_greeting"`: 需要主动问候
- `"generate_response"`: 正常响应

## API端点

### 新增端点

1. **GET /pet/status**
   - 获取宠物完整状态
   - 包括心情、精力、最后互动时间

2. **POST /pet/greeting**
   - 触发主动问候
   - 返回问候消息

3. **POST /message** (升级)
   - 使用LangGraph Agent处理消息
   - 支持状态管理和条件分支

## 测试和调试

### 运行测试

```bash
cd backend
python test_langgraph.py
```

### 测试内容

1. **Agent功能测试**
   - 不同性格的响应测试
   - 状态管理测试
   - 工作流执行测试

2. **API端点测试**
   - 宠物状态查询
   - 主动问候触发
   - 消息发送处理

3. **工作流组件测试**
   - 状态键验证
   - 消息数量检查
   - 心情和精力更新

## 性能优化

### 状态管理优化

1. **消息限制**: 保留最近6轮对话
2. **状态缓存**: 避免重复计算
3. **异步处理**: 支持并发请求

### 内存管理

1. **状态清理**: 定期清理过期状态
2. **消息压缩**: 压缩历史消息
3. **资源回收**: 及时释放不需要的资源

## 扩展功能

### 计划中的扩展

1. **工具集成**
   - 时间工具：获取当前时间
   - 天气工具：查询天气信息
   - 提醒工具：设置和管理提醒

2. **多Agent系统**
   - 监督者Agent：管理多个专业Agent
   - 专业Agent：处理特定任务
   - 协作机制：Agent间协作

3. **高级工作流**
   - 循环工作流：支持重复任务
   - 并行处理：同时执行多个节点
   - 错误恢复：自动错误处理和恢复

## 故障排除

### 常见问题

1. **依赖冲突**
   - 确保LangGraph版本兼容
   - 检查Python版本要求

2. **状态错误**
   - 验证状态结构
   - 检查reducer配置

3. **工作流卡住**
   - 检查条件分支逻辑
   - 验证节点返回值

### 调试技巧

1. **启用详细日志**
2. **使用LangGraph Studio可视化**
3. **逐步执行工作流**
4. **检查状态变化**

## 下一步计划

1. **工具集成**
   - 实现基础工具（时间、天气）
   - 集成MCP Server
   - 添加自定义工具

2. **主动互动系统**
   - 定时问候功能
   - 情境感知响应
   - 个性化提醒

3. **高级功能**
   - 多模态交互
   - 情感识别
   - 学习能力 