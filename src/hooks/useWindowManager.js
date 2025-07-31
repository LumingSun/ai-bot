import { useState, useEffect } from 'react';

export const useWindowManager = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [windowOpacity, setWindowOpacity] = useState(1);

  // 开始拖拽
  const startDrag = (e) => {
    setIsDragging(true);
    const rect = e.currentTarget.getBoundingClientRect();
    setDragOffset({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    });
  };

  // 停止拖拽
  const stopDrag = () => {
    setIsDragging(false);
  };

  // 处理鼠标移动
  const handleMouseMove = (e) => {
    if (!isDragging) return;
    
    const newX = Math.round(e.clientX - dragOffset.x);
    const newY = Math.round(e.clientY - dragOffset.y);
    
    // 确保参数是有效的数字
    if (isNaN(newX) || isNaN(newY)) return;
    
    // 通过Electron API设置窗口位置
    try {
      window.electronAPI.setWindowPosition(newX, newY);
    } catch (error) {
      console.error('Failed to set window position:', error);
    }
  };

  // 处理鼠标抬起
  const handleMouseUp = () => {
    stopDrag();
  };

  // 设置窗口透明度
  const setOpacity = (opacity) => {
    const validOpacity = Math.max(0.1, Math.min(1, opacity));
    setWindowOpacity(validOpacity);
    try {
      window.electronAPI.setWindowOpacity(validOpacity);
    } catch (error) {
      console.error('Failed to set window opacity:', error);
    }
  };

  // 监听全局鼠标事件
  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, dragOffset]);

  return {
    isDragging,
    startDrag,
    stopDrag,
    windowOpacity,
    setOpacity
  };
}; 