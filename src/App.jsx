import { Navigate, Route, Routes } from 'react-router-dom';
import ProtectedRoute from './routes/ProtectedRoute';
import DashboardLayout from './layouts/DashboardLayout';
import LoginPage from './pages/auth/LoginPage';
import OverviewPage from './pages/dashboard/OverviewPage';
import UsersPage from './pages/users/UsersPage';
import RolesPage from './pages/roles/RolesPage';
import AccessHistoryPage from './pages/access/AccessHistoryPage';
import RegisterAccessPage from './pages/access/RegisterAccessPage';
import AnalyticsPage from './pages/dashboard/AnalyticsPage';
import AppErrorBoundary from './components/common/AppErrorBoundary';

function readHasAccess() {
  try {
    return Boolean(window.localStorage.getItem('token')) || window.localStorage.getItem('previewMode') === 'true';
  } catch (error) {
    console.error('No se pudo leer el almacenamiento local:', error);
    return false;
  }
}

function AppRoutes() {
  const hasAccess = readHasAccess();
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/dashboard" element={<ProtectedRoute><DashboardLayout /></ProtectedRoute>}>
        <Route index element={<OverviewPage />} />
        <Route path="analitica" element={<AnalyticsPage />} />
        <Route path="usuarios" element={<UsersPage />} />
        <Route path="roles" element={<RolesPage />} />
        <Route path="accesos" element={<AccessHistoryPage />} />
        <Route path="registrar" element={<RegisterAccessPage />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Route>
      <Route path="*" element={<Navigate to={hasAccess ? '/dashboard' : '/login'} replace />} />
    </Routes>
  );
}

export function App() {
  return (
    <AppErrorBoundary>
      <AppRoutes />
    </AppErrorBoundary>
  );
}

export default App;
