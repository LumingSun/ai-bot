import React from 'react';

const SettingsPanel = ({ show, onClose, onPetTypeChange, currentPetType }) => {
  const petTypes = [
    { value: 'cat', label: '🐱 猫咪' },
    { value: 'dog', label: '🐕 小狗' },
    { value: 'rabbit', label: '🐰 兔子' },
    { value: 'hamster', label: '🐹 仓鼠' }
  ];

  const handlePetTypeChange = (type) => {
    onPetTypeChange(type);
  };

  if (!show) return null;

  return (
    <div className="settings-panel show">
      <div style={{ marginBottom: '12px', fontWeight: '600', color: '#667eea' }}>
        🎨 设置
      </div>
      
      {/* 宠物类型选择器 */}
      <div className="pet-type-selector">
        {petTypes.map((pet) => (
          <button
            key={pet.value}
            className={`pet-type-btn ${currentPetType === pet.value ? 'active' : ''}`}
            onClick={() => handlePetTypeChange(pet.value)}
            title={`选择${pet.label}`}
          >
            {pet.label}
          </button>
        ))}
      </div>
      
      {/* 功能按钮 */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
        <button 
          onClick={() => window.electronAPI.changePetType('cat')}
          title="切换到猫咪"
        >
          🐱 切换猫咪
        </button>
        <button 
          onClick={() => window.electronAPI.changePetType('dog')}
          title="切换到小狗"
        >
          🐕 切换小狗
        </button>
        <button 
          onClick={() => window.electronAPI.changePetType('rabbit')}
          title="切换到兔子"
        >
          🐰 切换兔子
        </button>
        <button 
          onClick={() => window.electronAPI.changePetType('hamster')}
          title="切换到仓鼠"
        >
          🐹 切换仓鼠
        </button>
        <button 
          onClick={onClose}
          style={{ 
            background: 'linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%)',
            marginTop: '8px'
          }}
          title="关闭设置"
        >
          ❌ 关闭
        </button>
      </div>
    </div>
  );
};

export default SettingsPanel; 