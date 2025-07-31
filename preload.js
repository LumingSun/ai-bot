const { contextBridge, ipcRenderer } = require('electron');

// 暴露安全的 API 到渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
  // 窗口管理
  getWindowInfo: () => ipcRenderer.invoke('get-window-info'),
  setWindowPosition: (x, y) => ipcRenderer.invoke('set-window-position', x, y),
  setWindowOpacity: (opacity) => ipcRenderer.invoke('set-window-opacity', opacity),
  minimizeWindow: () => ipcRenderer.invoke('minimize-window'),
  hideWindow: () => ipcRenderer.invoke('hide-window'),
  showWindow: () => ipcRenderer.invoke('show-window'),
  
  // 宠物相关
  getPetInfo: () => ipcRenderer.invoke('get-pet-info'),
  updatePetInfo: (petInfo) => ipcRenderer.invoke('update-pet-info', petInfo),
  changePetType: (type) => ipcRenderer.invoke('change-pet-type', type),
  
  // 对话相关
  sendMessage: (message) => ipcRenderer.invoke('send-message', message),
  getConversationHistory: () => ipcRenderer.invoke('get-conversation-history'),
  
  // 设置相关
  getSettings: () => ipcRenderer.invoke('get-settings'),
  updateSettings: (settings) => ipcRenderer.invoke('update-settings', settings),
  resetSettings: () => ipcRenderer.invoke('reset-settings'),
  
  // 监听事件
  onPetMessage: (callback) => ipcRenderer.on('pet-message', callback),
  onPetAnimation: (callback) => ipcRenderer.on('pet-animation', callback),
  onPetGreeting: (callback) => ipcRenderer.on('pet-greeting', callback),
  
  // 移除监听器
  removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel)
}); 