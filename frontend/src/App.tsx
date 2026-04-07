import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from './pages/LoginPage';
import { LogsPage } from './pages/LogsPage';
import { DashboardPage } from './pages/DashboardPage';
import { MainLayout } from './layouts/MainLayout';

function App() {
  const baseUrl = import.meta.env.BASE_URL || '/';
  const routerBaseName = baseUrl !== '/' && baseUrl.endsWith('/')
    ? baseUrl.slice(0, -1)
    : baseUrl;

  return (
    <BrowserRouter basename={routerBaseName}>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/logs"
          element={
            <MainLayout>
              <LogsPage />
            </MainLayout>
          }
        />
        <Route
          path="/dashboard"
          element={
            <MainLayout>
              <DashboardPage />
            </MainLayout>
          }
        />
        <Route path="/" element={<Navigate to="/logs" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
