import axiosClient, { unwrapResponse } from '../api/axiosClient';

export const userService = {
  listarUsuarios: async () => unwrapResponse(await axiosClient.get('/api/usuarios')) || [],
  obtenerPorIdentificacion: async (identificacion) => unwrapResponse(await axiosClient.get(`/api/usuarios/${encodeURIComponent(identificacion)}`)),
  crearUsuario: async (userData) => unwrapResponse(await axiosClient.post('/api/usuarios', userData)),
  actualizarUsuario: async (userData) => unwrapResponse(await axiosClient.put('/api/usuarios', userData)),
};

