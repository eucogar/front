import axiosClient from '../api/axiosClient';

export const authService = {
  login: async (credentials) => (await axiosClient.post('/api/auth/login', credentials)).data,
};
