import React from 'react';

const Pet = ({ type = 'cat' }) => {
  const getPetImage = (petType) => {
    switch (petType) {
      case 'cat':
        return '/assets/cat.png';
      case 'dog':
        return '/assets/dog.png';
      case 'rabbit':
        return '/assets/rabbit.png';
      case 'hamster':
        return '/assets/hamster.png';
      default:
        return '/assets/cat.png';
    }
  };

  const getPetEmoji = (petType) => {
    switch (petType) {
      case 'cat':
        return '🐱';
      case 'dog':
        return '🐕';
      case 'rabbit':
        return '🐰';
      case 'hamster':
        return '🐹';
      default:
        return '🐱';
    }
  };

  return (
    <div className="pet-image-container">
      <img
        src={getPetImage(type)}
        alt={`${type} pet`}
        className="pet-image"
        onError={(e) => {
          // 如果图片加载失败，显示emoji
          e.target.style.display = 'none';
          const emojiDiv = document.createElement('div');
          emojiDiv.style.cssText = `
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 80px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            color: white;
          `;
          emojiDiv.textContent = getPetEmoji(type);
          e.target.parentNode.appendChild(emojiDiv);
        }}
      />
    </div>
  );
};

export default Pet; 