import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from './pages/LoginPage';
import { LogsPage } from './pages/LogsPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/logs" element={<LogsPage />} />
        <Route path="/" element={<Navigate to="/logs" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
