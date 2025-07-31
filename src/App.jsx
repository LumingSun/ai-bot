import React, { useState, useEffect } from 'react';
import Pet from './components/Pet';
import ChatBubble from './components/ChatBubble';
import SettingsPanel from './components/SettingsPanel';
import { usePetSystem } from './hooks/usePetSystem';
import { useWindowManager } from './hooks/useWindowManager';

function App() {
  const { pet, sendMessage, isLoading } = usePetSystem();
  const { isDragging, startDrag, stopDrag, windowOpacity } = useWindowManager();
  const [showSettings, setShowSettings] = useState(false);
  const [showInput, setShowInput] = useState(false);
  const [inputMessage, setInputMessage] = useState('');
  const [currentPetType, setCurrentPetType] = useState('cat');

  // 处理拖拽
  const handleMouseDown = (e) => {
    // 阻止事件冒泡
    e.stopPropagation();
    
    // 检查是否点击了不应该拖拽的元素
    if (e.target.closest('.settings-panel') || 
        e.target.closest('.message-input') ||
        e.target.closest('.chat-bubble') ||
        e.target.closest('.pet-status')) {
      return;
    }
    
    startDrag(e);
  };

  const handleMouseUp = (e) => {
    e.stopPropagation();
    stopDrag();
  };

  // 处理右键菜单
  const handleContextMenu = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setShowSettings(!showSettings);
  };

  // 处理双击
  const handleDoubleClick = (e) => {
    e.stopPropagation();
    setShowInput(!showInput);
  };

  // 处理消息发送
  const handleSendMessage = async (message) => {
    if (message.trim()) {
      // 立即隐藏输入框，不等待消息回复
      setShowInput(false);
      setInputMessage('');
      
      // 异步发送消息
      await sendMessage(message.trim());
    }
  };

  // 处理回车键
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault(); // 阻止默认行为
      handleSendMessage(inputMessage);
    }
  };

  // 处理宠物类型变更
  const handlePetTypeChange = async (type) => {
    try {
      await window.electronAPI.changePetType(type);
      setCurrentPetType(type);
    } catch (error) {
      console.error('Failed to change pet type:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="loading">
        <div>🐾 正在加载宠物...</div>
      </div>
    );
  }

  return (
    <div
      className="pet-container"
      style={{ opacity: windowOpacity }}
      onMouseDown={handleMouseDown}
      onMouseUp={handleMouseUp}
      onContextMenu={handleContextMenu}
      onDoubleClick={handleDoubleClick}
    >
      {/* 宠物图片 */}
      <Pet type={pet?.type || 'cat'} />
      
      {/* 聊天气泡 */}
      {pet?.currentMessage && (
        <ChatBubble message={pet.currentMessage} />
      )}
      
      {/* 宠物状态指示器 */}
      <div className="pet-status">
        <div 
          className={`status-indicator ${pet?.energy < 30 ? 'energy-critical' : pet?.energy < 60 ? 'energy-low' : ''}`}
          title={`精力值: ${pet?.energy || 100}`}
        />
        <div 
          className="status-indicator"
          style={{ background: pet?.mood === 'happy' ? '#4CAF50' : pet?.mood === 'sad' ? '#F44336' : '#FF9800' }}
          title={`心情: ${pet?.mood || 'neutral'}`}
        />
      </div>
      
      {/* 消息输入框 */}
      {showInput && (
        <input
          type="text"
          className="message-input show"
          placeholder="输入消息..."
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          onBlur={() => {
            // 延迟隐藏，给用户时间点击发送按钮
            setTimeout(() => setShowInput(false), 100);
          }}
          autoFocus
        />
      )}
      
      {/* 设置面板 */}
      <SettingsPanel
        show={showSettings}
        onClose={() => setShowSettings(false)}
        onPetTypeChange={handlePetTypeChange}
        currentPetType={currentPetType}
      />
      
      {/* 工具调用指示器 */}
      {isDragging && (
        <div className="tool-indicator">
          🔧 正在处理...
        </div>
      )}
    </div>
  );
}

export default App; 