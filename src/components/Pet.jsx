import React from 'react';

const Pet = ({ pet }) => {
  if (!pet) return null;

  const getPetImage = (type) => {
    const petImages = {
      cat: '/assets/cat.png',
      dog: '/assets/dog.png',
      rabbit: '/assets/rabbit.png',
      hamster: '/assets/hamster.png'
    };
    return petImages[type] || petImages.cat;
  };

  return (
    <div className="pet-wrapper">
      <img
        src={getPetImage(pet.type)}
        alt={`${pet.name} (${pet.personality})`}
        className="pet-image"
        style={{
          filter: pet.personality === 'cold' ? 'grayscale(0.3)' : 'none',
          transform: pet.personality === 'playful' ? 'scale(1.05)' : 'scale(1)'
        }}
      />
    </div>
  );
};

export default Pet; 