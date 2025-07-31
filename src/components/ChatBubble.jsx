import React, { useState, useEffect } from 'react';

const ChatBubble = ({ message }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (message && message.trim()) {
      setIsVisible(true);
      
      // 3秒后隐藏消息
      const timer = setTimeout(() => {
        setIsVisible(false);
      }, 3000);

      return () => {
        clearTimeout(timer);
      };
    } else {
      setIsVisible(false);
    }
  }, [message]);

  if (!isVisible || !message || !message.trim()) {
    return null;
  }

  return (
    <div className="chat-bubble">
      {message}
    </div>
  );
};

export default ChatBubble; 