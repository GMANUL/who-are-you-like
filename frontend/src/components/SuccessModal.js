import React from 'react';
import './SuccessModal.css';

export default function SuccessModal({ message, onClose }) {
  if (!message) return null;

  return (
    <div className="success-modal">
      <div className="success-content">
        <p>{message}</p>
        <button onClick={onClose}>Закрыть</button>
      </div>
    </div>
  );
}