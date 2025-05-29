import React, { useState, useEffect, useCallback } from 'react';
import './CelebritySearch.css';

export default function CelebritySearch({ onError }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [names, setNames] = useState([]);
  const [loading, setLoading] = useState(false);
  const API_URL = 'http://localhost:8000';

  const handleSearch = useCallback(async (query) => {
    if (!query.trim()) {
      setNames([]);
      return;
    }

    setLoading(true);
    onError(null);

    try {
      const apiUrl = `${API_URL}/search/${encodeURIComponent(query)}`;
      const response = await fetch(apiUrl);
      
      if (!response.ok) {
        throw new Error(`Ошибка поиска: ${response.status}`);
      }

      const data = await response.json();
      setNames(data.names || []);
    } catch (err) {
      onError(err.message);
      setNames([]);
    } finally {
      setLoading(false);
    }
  }, [onError]);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      handleSearch(searchQuery);
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [searchQuery, handleSearch]);

  const handleInputChange = (e) => {
    setSearchQuery(e.target.value);
  };

  return (
    <div className="search-form">
      <h2>Поиск похожих имен</h2>
      
      <div className="search-section">
        <input
          type="text"
          placeholder="Введите имя для поиска..."
          value={searchQuery}
          onChange={handleInputChange}
          className="search-input"
        />
        
        {loading && <div className="loading">Поиск...</div>}
      </div>

      <div className="results-section">
        {names.length > 0 && (
          <div className="names-list">
            <h3>Найденные имена:</h3>
            <ul>
              {names.map((name, index) => (
                <li key={index} className="name-item">
                  {name}
                </li>
              ))}
            </ul>
          </div>
        )}
        
        {searchQuery && !loading && names.length === 0 && (
          <div className="no-results">
            По запросу "{searchQuery}" ничего не найдено
          </div>
        )}
      </div>
    </div>
  );
}