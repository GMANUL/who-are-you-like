import React, { useState } from 'react';
import './CelebrityAddForm.css';

export default function CelebrityAddForm({ onError, onSuccess }) {
  const [showForm, setShowForm] = useState(false);
  const [celebName, setCelebName] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const API_URL = 'http://localhost:8000';

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!celebName.trim()) {
      onError('Введите имя знаменитости');
      return;
    }
    
    if (celebName.trim().length < 3) {
      onError('Имя должно содержать минимум 3 символа');
      return;
    }
    
    if (celebName.trim().length > 25) {
      onError('Имя не должно превышать 25 символов');
      return;
    }

    if (!selectedFile) {
      onError('Выберите фото знаменитости');
      return;
    }

    setLoading(true);
    onError(null);

    try {
      const formData = new FormData();
      formData.append('celeb_name', celebName.trim());
      formData.append('file', selectedFile);

      const response = await fetch(`${API_URL}/new_celebrity`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Ошибка: ${response.status}`);
      }

      onSuccess('Знаменитость успешно добавлена!');
      resetForm();

    } catch (err) {
      onError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setCelebName('');
    setSelectedFile(null);
    setShowForm(false);
    
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
          <form onSubmit={handleSubmit} className="celebrity-form">
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
                type="submit" 
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
          </form>
        </div>
      )}
    </div>
  );
}