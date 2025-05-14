import React, { useState } from 'react';
import './CelebrityCarousel.css';

export default function CelebrityCarousel({ matches, isLoading }) {
  const [currentIndex, setCurrentIndex] = useState(0);

  const nextCelebrity = () => {
    setCurrentIndex(prev => (prev === matches.length - 1 ? 0 : prev + 1));
  };

  const prevCelebrity = () => {
    setCurrentIndex(prev => (prev === 0 ? matches.length - 1 : prev - 1));
  };

  if (isLoading) return <div className="loading-placeholder">Загружаем совпадения...</div>;
  if (matches.length === 0) return <div className="empty-placeholder">Загрузите фото для сравнения</div>;

  return (
    <div className="carousel-wrapper">
      <div className="carousel-container">
        <button onClick={prevCelebrity} className="nav-button prev-button">‹</button>
        
        <div className="celebrity-card">
          <img 
            src={matches[currentIndex].photoUrl} 
            alt={matches[currentIndex].name}
            className="celebrity-image"
          />
          <h2 className="celebrity-name">{matches[currentIndex].name}</h2>
        </div>

        <button onClick={nextCelebrity} className="nav-button next-button">›</button>
      </div>
      
      <div className="carousel-indicator">
        {matches.map((_, index) => (
          <div 
            key={index}
            className={`indicator-dot ${index === currentIndex ? 'active' : ''}`}
            onClick={() => setCurrentIndex(index)}
          />
        ))}
      </div>
    </div>
  );
}