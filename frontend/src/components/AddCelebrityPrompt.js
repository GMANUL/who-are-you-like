import React from 'react';
import { useNavigate } from 'react-router-dom';
import './AddCelebrityPrompt.css'; // Создайте этот файл для стилей

const AddCelebrityPrompt = () => {
  const navigate = useNavigate();

  const handleAddCelebrity = () => {
    navigate('/add_person');
  };

  return (
    <div className="add-celebrity-prompt">
      <p className="prompt-text">Кажется, что кого-то не хватает?</p>
      <button 
        className="add-button"
        onClick={handleAddCelebrity}
      >
        Добавить знаменитость
      </button>
    </div>
  );
};

export default AddCelebrityPrompt;