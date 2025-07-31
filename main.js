const { app, BrowserWindow, ipcMain, screen } = require('electron');
const path = require('path');
const isDev = !app.isPackaged;

let mainWindow;

function createWindow() {
  // 获取主显示器的尺寸
  const primaryDisplay = screen.getPrimaryDisplay();
  const { width, height } = primaryDisplay.workAreaSize;

  // 创建悬浮窗口
  mainWindow = new BrowserWindow({
    width: 300,
    height: 500, // 增加高度以容纳气泡
    x: width - 350,
    y: height - 550,
    frame: false, // 无边框
    transparent: true, // 透明背景
    alwaysOnTop: true, // 置顶
    resizable: false, // 不可调整大小
    skipTaskbar: true, // 不在任务栏显示
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  // 加载应用
  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, 'dist', 'index.html'));
  }

  // 窗口关闭时退出应用
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // 防止窗口被关闭
  mainWindow.on('close', (event) => {
    event.preventDefault();
    mainWindow.hide();
  });
}

// 应用准备就绪时创建窗口
app.whenReady().then(createWindow);

// 所有窗口关闭时退出应用
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// IPC 通信处理
ipcMain.handle('get-window-info', () => {
  const bounds = mainWindow.getBounds();
  return {
    x: bounds.x,
    y: bounds.y,
    width: bounds.width,
    height: bounds.height
  };
});

ipcMain.handle('set-window-position', (event, x, y) => {
  mainWindow.setPosition(x, y);
});

ipcMain.handle('set-window-opacity', (event, opacity) => {
  mainWindow.setOpacity(opacity);
});

ipcMain.handle('minimize-window', () => {
  mainWindow.minimize();
});

ipcMain.handle('hide-window', () => {
  mainWindow.hide();
});

ipcMain.handle('show-window', () => {
  mainWindow.show();
});

// 宠物相关 API
ipcMain.handle('get-pet-info', async () => {
  try {
    const response = await fetch('http://127.0.0.1:8001/pet');
    return await response.json();
  } catch (error) {
    console.error('Failed to get pet info:', error);
    return null;
  }
});

ipcMain.handle('send-message', async (event, message) => {
  try {
    const response = await fetch('http://127.0.0.1:8001/message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message })
    });
    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error('Failed to send message:', error);
    return '抱歉，我现在无法回应...';
  }
});

ipcMain.handle('get-conversation-history', async () => {
  try {
    const response = await fetch('http://127.0.0.1:8001/conversations');
    return await response.json();
  } catch (error) {
    console.error('Failed to get conversation history:', error);
    return [];
  }
});

ipcMain.handle('change-pet-type', async (event, type) => {
  try {
    const response = await fetch('http://127.0.0.1:8001/pet/change-type', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ pet_type: type })
    });
    return await response.json();
  } catch (error) {
    console.error('Failed to change pet type:', error);
    return { error: 'Failed to change pet type' };
  }
});

// 设置相关 API
ipcMain.handle('get-settings', () => {
  // 从本地存储获取设置
  return {
    opacity: 0.9,
    greetingInterval: 300,
    enableProactiveInteraction: true
  };
});

ipcMain.handle('update-settings', (event, settings) => {
  // 保存设置到本地存储
  return { success: true };
});

ipcMain.handle('reset-settings', () => {
  // 重置设置
  return { success: true };
});

// 启动 Python 后端服务
const { spawn } = require('child_process');
let pythonProcess;

function startPythonBackend() {
  const pythonPath = path.join(__dirname, 'backend', 'main.py');
  pythonProcess = spawn('python3', [pythonPath], {
    stdio: ['pipe', 'pipe', 'pipe']
  });

  pythonProcess.stdout.on('data', (data) => {
    console.log('Python backend:', data.toString());
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error('Python backend error:', data.toString());
  });

  pythonProcess.on('close', (code) => {
    console.log('Python backend closed with code:', code);
  });
}

// 应用启动时启动 Python 后端
app.whenReady().then(() => {
  createWindow();
  startPythonBackend();
});

// 应用退出时关闭 Python 后端
app.on('before-quit', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
}); 