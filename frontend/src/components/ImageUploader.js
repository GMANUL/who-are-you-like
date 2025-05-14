import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import './ImageUploader.css'; // Создадим отдельный CSS файл

const ImageUploader = ({ onDrop }) => {
  const [preview, setPreview] = useState(null);

  const onDropHandler = useCallback((acceptedFiles) => {
    if (acceptedFiles.length === 0) return;
    
    const file = acceptedFiles[0];
    const reader = new FileReader();
    
    reader.onload = () => {
      setPreview(reader.result);
      onDrop(acceptedFiles);
    };
    
    reader.readAsDataURL(file);
  }, [onDrop]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {'image/*': ['.jpeg', '.jpg', '.png']},
    maxFiles: 1,
    onDrop: onDropHandler
  });

  return (
    <div {...getRootProps()} className={`upload-container ${isDragActive ? 'drag-active' : ''}`}>
      <input {...getInputProps()} />
      
      {preview ? (
        <div className="preview-wrapper">
          <img src={preview} alt="Ваше фото" className="uploaded-image" />
          <div className="hover-overlay">
            <span>Нажмите для изменения</span>
          </div>
        </div>
      ) : (
        <div className="upload-placeholder">
          <div className="upload-icon">↑</div>
          <p className="upload-text">Перетащите фото сюда</p>
          <p className="upload-subtext">или нажмите для выбора</p>
          <p className="file-requirements">JPG, PNG до 5MB</p>
        </div>
      )}
    </div>
  );
};

export default ImageUploader;