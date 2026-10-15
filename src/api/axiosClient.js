import axios from 'axios';

const apiBaseUrl = (import.meta.env.VITE_API_URL ?? '').replace(/\/+$/, '');

const axiosClient = axios.create({
  baseURL: apiBaseUrl,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

axiosClient.interceptors.request.use((config) => {
  let token = null;
  try {
    token = window.localStorage.getItem('token');
  } catch {
    // El navegador puede bloquear el storage en contextos restringidos.
  }
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export function unwrapResponse(response) {
  const body = response?.data;
  return body && typeof body === 'object' && 'data' in body ? body.data : body;
}

export function getApiError(error) {
  return error?.response?.data?.message || error?.response?.data?.Message || error?.message || 'No fue posible conectar con el servidor.';
}

export default axiosClient;
