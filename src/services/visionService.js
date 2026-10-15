import axios from 'axios';

const visionClient = axios.create({
  baseURL: import.meta.env.VITE_VISION_API_URL || '/vision-api',
  timeout: 90000,
});

export const visionService = {
  async detectarPlaca(imagen) {
    const payload = new FormData();
    payload.append('imagen', imagen, imagen.name || 'captura.jpg');
    const response = await visionClient.post('/detectar', payload, {
      headers: { 'Content-Type': undefined },
    });
    return response.data?.placa || '';
  },
};
