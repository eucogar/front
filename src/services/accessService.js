import axiosClient, { unwrapResponse } from '../api/axiosClient';

export const accessService = {
  registrarAcceso: async (accessData) => unwrapResponse(await axiosClient.post('/api/acceso/registrar', accessData)),
  detectarYRegistrar: async (formData) => unwrapResponse(await axiosClient.post('/api/acceso/detectar-registrar', formData, { timeout: 90000, headers: { 'Content-Type': undefined } })),
  consultarFiltros: async (filtros) => {
    const data = unwrapResponse(await axiosClient.post('/api/acceso/consultar-filtros', filtros));
    return Array.isArray(data) ? data : data ? [data] : [];
  },
  consultarAnalitica: async (fechaInicio, fechaFin) => unwrapResponse(await axiosClient.get('/api/acceso/analitica', { params: { fechaInicio, fechaFin } })),
};
