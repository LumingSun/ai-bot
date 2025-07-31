import { useState, useEffect } from 'react';

export const usePetSystem = () => {
  const [pet, setPet] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    initializePet();
  }, []);

  const initializePet = async () => {
    try {
      // 从后端获取宠物信息
      const petInfo = await window.electronAPI.getPetInfo();
      setPet(petInfo);
    } catch (error) {
      console.error('Failed to initialize pet:', error);
      // 创建默认宠物
      const defaultPet = {
        id: 1,
        name: '小猫咪',
        type: 'cat',
        personality: 'playful',
        currentMessage: '' // 初始时不显示消息
      };
      setPet(defaultPet);
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async (message) => {
    try {
      const response = await window.electronAPI.sendMessage(message);
      
      // 更新宠物的当前消息
      setPet(prev => {
        const updatedPet = {
          ...prev,
          currentMessage: response
        };
        return updatedPet;
      });
    } catch (error) {
      console.error('Failed to send message:', error);
      setPet(prev => ({
        ...prev,
        currentMessage: '抱歉，我现在无法回应...'
      }));
    }
  };

  return {
    pet,
    sendMessage,
    isLoading
  };
}; 