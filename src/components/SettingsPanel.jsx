import React, { useState } from 'react';

const SettingsPanel = ({ show, onOpacityChange, onSendMessage }) => {
  const [message, setMessage] = useState('');
  const [opacity, setOpacity] = useState(0.9);



  const handleOpacityChange = (e) => {
    const newOpacity = parseFloat(e.target.value);
    setOpacity(newOpacity);
    onOpacityChange(newOpacity);
  };

  const handleSendMessage = () => {
    if (message.trim()) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  const personalityLabels = {
    cold: '高冷',
    clingy: '粘人',
    playful: '活泼',
    quiet: '安静'
  };

  if (!show) return null;

  return (
    <div className="settings-panel show">
      <div style={{ marginBottom: '8px' }}>
        <label style={{ display: 'block', marginBottom: '4px' }}>
          透明度: {Math.round(opacity * 100)}%
        </label>
        <input
          type="range"
          min="0.1"
          max="1"
          step="0.1"
          value={opacity}
          onChange={handleOpacityChange}
          style={{ width: '100%' }}
        />
      </div>
      
      <div style={{ marginBottom: '8px' }}>
        <input
          type="text"
          placeholder="输入消息..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          style={{
            width: '100%',
            padding: '4px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '11px'
          }}
        />
      </div>
      
      <div style={{ display: 'flex', gap: '4px' }}>
        <button onClick={handleSendMessage}>
          发送
        </button>
        <button onClick={() => onSendMessage('你好')}>
          问候
        </button>
        <button onClick={() => onSendMessage('摸摸头')}>
          互动
        </button>
      </div>
    </div>
  );
};

export default SettingsPanel; 