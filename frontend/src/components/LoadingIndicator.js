import React from 'react';
import './LoadingIndicator.css'; // подключаем стили

export default function LoadingIndicator() {
  return (
    <div className="loading-container">
      <div className="spinner" />
      <p>Анализируем ваше фото...</p>
    </div>
  );
}
