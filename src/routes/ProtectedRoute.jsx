import { Navigate } from 'react-router-dom';

export function hasPreviewAccess() {
  return localStorage.getItem('previewMode') === 'true';
}

export default function ProtectedRoute({ children }) {
  const hasSession = Boolean(localStorage.getItem('token'));
  return hasSession || hasPreviewAccess() ? children : <Navigate to="/login" replace />;
}
