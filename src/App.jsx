import React, { useState, useEffect, useRef } from 'react';
import Pet from './components/Pet';
import ChatBubble from './components/ChatBubble';
import SettingsPanel from './components/SettingsPanel';
import { usePetSystem } from './hooks/usePetSystem';
import { useWindowManager } from './hooks/useWindowManager';

function App() {
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [showSettings, setShowSettings] = useState(false);
  const containerRef = useRef(null);

  const { pet, sendMessage, isLoading } = usePetSystem();
  const { windowInfo, setWindowPosition, setWindowOpacity } = useWindowManager();

  // 拖拽处理
  const handleMouseDown = (e) => {
    if (e.target.closest('.settings-panel')) return;
    
    setIsDragging(true);
    const rect = containerRef.current.getBoundingClientRect();
    setDragOffset({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    });
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    
    const newX = e.clientX - dragOffset.x;
    const newY = e.clientY - dragOffset.y;
    setWindowPosition(newX, newY);
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // 双击显示设置面板
  const handleDoubleClick = () => {
    setShowSettings(!showSettings);
  };

  // 右键菜单
  const handleContextMenu = (e) => {
    e.preventDefault();
    setShowSettings(!showSettings);
  };

  useEffect(() => {
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, dragOffset]);

  if (isLoading) {
    return (
      <div className="loading">
        正在加载电子宠物...
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className="pet-container"
      onMouseDown={handleMouseDown}
      onDoubleClick={handleDoubleClick}
      onContextMenu={handleContextMenu}
    >
      <Pet pet={pet} />
      <ChatBubble message={pet?.currentMessage || ''} />
      <SettingsPanel 
        show={showSettings}
        onOpacityChange={setWindowOpacity}
        onSendMessage={sendMessage}
      />
    </div>
  );
}

export default App; 