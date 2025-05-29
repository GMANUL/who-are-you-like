import React, { useState } from 'react';
import SearchForm from '../components/CelebritySearch';
import CelebrityForm from '../components/CelebrityAddForm';
import SuccessModal from '../components/SuccessModal';
import ErrorDisplay from '../components/ErrorDisplay';
import './CelebrityPage.css';

export default function CelebsPage() {
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const clearError = () => {
    setError(null);
  };

  const clearSuccess = () => {
    setSuccessMessage(null);
  };

  return (
    <div className="celebs-page">
      <div className="page-header">
        <h1>Управление знаменитостями</h1>
      </div>
      
      <div className="page-content">
        <div className="section">
          <SearchForm onError={setError} />
        </div>
        
        <div className="section">
          <CelebrityForm 
            onError={setError} 
            onSuccess={setSuccessMessage} 
          />
        </div>
      </div>

      <SuccessModal message={successMessage} onClose={clearSuccess} />
      <ErrorDisplay error={error} onClose={clearError} />
    </div>
  );
}