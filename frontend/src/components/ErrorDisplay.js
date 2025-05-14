import React from 'react';
import './ErrorDisplay.css';

export default function ErrorDisplay({ error, onClose }) {
  if (!error) return null;

  return (
    <div className="error-display">
      <div className="error-content">
        <p>{error}</p>
        <button onClick={onClose}>Закрыть</button>
      </div>
    </div>
  );
}