import React from 'react';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import MainPage from './pages/ComparePage';
import CelebrityPage from './pages/CelebrityPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/add_person" element={<CelebrityPage />} /> 
      </Routes>
    </Router>
  );
}

export default App;