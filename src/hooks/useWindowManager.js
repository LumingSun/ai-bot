import { useState, useEffect } from 'react';

export const useWindowManager = () => {
  const [windowInfo, setWindowInfo] = useState(null);

  useEffect(() => {
    loadWindowInfo();
  }, []);

  const loadWindowInfo = async () => {
    try {
      const info = await window.electronAPI.getWindowInfo();
      setWindowInfo(info);
    } catch (error) {
      console.error('Failed to load window info:', error);
    }
  };

  const setWindowPosition = async (x, y) => {
    try {
      await window.electronAPI.setWindowPosition(x, y);
      setWindowInfo(prev => ({ ...prev, x, y }));
    } catch (error) {
      console.error('Failed to set window position:', error);
    }
  };

  const setWindowOpacity = async (opacity) => {
    try {
      await window.electronAPI.setWindowOpacity(opacity);
      setWindowInfo(prev => ({ ...prev, opacity }));
    } catch (error) {
      console.error('Failed to set window opacity:', error);
    }
  };

  return {
    windowInfo,
    setWindowPosition,
    setWindowOpacity
  };
}; 