import React, { useState } from 'react';
import axios from 'axios';
import ImageUploader from '../components/ImageUploader';
import CelebrityCarousel from '../components/CelebrityCarousel';
import LoadingIndicator from '../components/LoadingIndicator';
import ErrorDisplay from '../components/ErrorDisplay';
import AddCelebrityPrompt from '../components/AddCelebrityPrompt';
import styles from './ComparePage.css';

function App() {
  const [matches, setMatches] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const API_URL = 'http://localhost:8000';

  const handleDrop = async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;
    
    setIsLoading(true);
    setError(null);
    setMatches([]);

    try {
      const formData = new FormData();
      formData.append('file', acceptedFiles[0]);

      const response = await axios.post(`${API_URL}/compare`, formData, {
        headers: { 
          'Content-Type': 'multipart/form-data'
        },
        transformRequest: formData => formData
      });

      if (!response.data?.matches) {
        throw new Error('Сервер вернул некорректные данные');
      }

      setMatches(response.data.matches.map(match => ({
        id: match.id,
        name: match.name,
        photoUrl: `${API_URL}/photo/${match.id}?t=${Date.now()}`
      })));

    } catch (err) {
      setError(
        err.response?.data?.detail || 
        err.response?.data?.message || 
        err.message || 
        'Произошла неизвестная ошибка'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.app}>
      <h1>Celebrity Face Matcher</h1>
      
      
      {isLoading && <LoadingIndicator />}
      
      {error && (
        <ErrorDisplay 
          error={error} 
          onClose={() => setError(null)} 
        />
      )}

      <div className="content-container">
        <ImageUploader onDrop={handleDrop} />
        <CelebrityCarousel matches={matches} isLoading={isLoading} />
      </div>
      <AddCelebrityPrompt />
    </div>
  );
}

export default App;