import React, { useState } from 'react';
import './CelebrityAddForm.css';

export default function CelebrityAddForm({ onError, onSuccess }) {
  const [showForm, setShowForm] = useState(false);
  const [celebName, setCelebName] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [confirmationData, setConfirmationData] = useState(null);
  const API_URL = 'http://localhost:8000';

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
  };

  const validateForm = () => {
    if (!celebName.trim()) {
      onError('Введите имя знаменитости');
      return false;
    }
    
    if (celebName.trim().length < 3) {
      onError('Имя должно содержать минимум 3 символа');
      return false;
    }
    
    if (celebName.trim().length > 25) {
      onError('Имя не должно превышать 25 символов');
      return false;
    }

    if (!selectedFile) {
      onError('Выберите фото знаменитости');
      return false;
    }

    return true;
  };

  const createFormData = (force = false) => {
    const formData = new FormData();
    formData.append('celeb_name', celebName.trim());
    formData.append('file', selectedFile);
    formData.append('force', force.toString());
    return formData;
  };

  const submitCelebrity = async (force = false) => {
    if (!force && !validateForm()) {
      return;
    }

    setLoading(true);
    onError(null);

    try {
      const formData = createFormData(force);

      const response = await fetch(`${API_URL}/new_celebrity`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        
        // Проверяем, является ли ответ ConfirmationResponse
        if (data && data.status === 'confirmation_required') {
          setConfirmationData(data);
          setShowConfirmation(true);
        } else {
          // Успешное создание
          onSuccess('Знаменитость успешно добавлена!');
          resetForm();
        }
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Ошибка: ${response.status}`);
      }

    } catch (err) {
      onError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await submitCelebrity(false);
  };

  const handleConfirmationYes = async () => {
    setShowConfirmation(false);
    await submitCelebrity(true); // Отправляем с force=true
  };

  const handleConfirmationNo = () => {
    setShowConfirmation(false);
    setConfirmationData(null);
  };

  const resetForm = () => {
    setCelebName('');
    setSelectedFile(null);
    setShowForm(false);
    setShowConfirmation(false);
    setConfirmationData(null);
    
    const fileInput = document.getElementById('file-input');
    if (fileInput) {
      fileInput.value = '';
    }
  };

  const handleCancel = () => {
    resetForm();
    onError(null);
  };

  return (
    <div className="celebrity-form-container">
      <h2>Добавление знаменитости</h2>
      
      {!showForm ? (
        <div className="button-section">
          <button 
            className="add-button"
            onClick={() => setShowForm(true)}
          >
            Добавить знаменитость
          </button>
        </div>
      ) : (
        <div className="form-section">
          <div className="celebrity-form">
            <div className="form-group">
              <label htmlFor="celeb-name">Имя знаменитости:</label>
              <input
                id="celeb-name"
                type="text"
                value={celebName}
                onChange={(e) => setCelebName(e.target.value)}
                placeholder="Введите имя (3-25 символов)"
                minLength={3}
                maxLength={25}
                className="name-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="file-input">Фото знаменитости:</label>
              <input
                id="file-input"
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                className="file-input"
              />
              {selectedFile && (
                <div className="file-info">
                  Выбранный файл: {selectedFile.name}
                </div>
              )}
            </div>

            <div className="form-buttons">
              <button 
                type="button"
                onClick={handleSubmit}
                disabled={loading}
                className="submit-button"
              >
                {loading ? 'Добавление...' : 'Добавить'}
              </button>
              <button 
                type="button" 
                onClick={handleCancel}
                disabled={loading}
                className="cancel-button"
              >
                Отмена
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Confirmation Modal */}
      {showConfirmation && confirmationData && (
        <div className="confirmation-overlay">
          <div className="confirmation-modal">
            <div className="confirmation-header">
              <h3>Подтверждение действия</h3>
              <button 
                className="close-button"
                onClick={handleConfirmationNo}
                aria-label="Закрыть"
              >
                ×
              </button>
            </div>

            <div className="confirmation-content">
              <p className="confirmation-message">{confirmationData.message}</p>
              
              {confirmationData.similar_names && confirmationData.similar_names.length > 0 && (
                <div className="similar-names-section">
                  <p className="similar-names-title">Похожие имена:</p>
                  <ul className="similar-names-list">
                    {confirmationData.similar_names.map((name, index) => (
                      <li key={index}>{name}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <div className="confirmation-buttons">
              <button
                onClick={handleConfirmationNo}
                className="confirmation-cancel-button"
              >
                Нет, отменить
              </button>
              <button
                onClick={handleConfirmationYes}
                className="confirmation-confirm-button"
              >
                Да, добавить
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}