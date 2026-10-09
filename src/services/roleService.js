import axiosClient, { unwrapResponse } from '../api/axiosClient';

export const roleService = {
  obtenerRoles: async () => unwrapResponse(await axiosClient.get('/api/roles')) || [],
};
