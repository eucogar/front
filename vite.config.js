import { defineConfig } from 'vite';
import { networkInterfaces } from 'node:os';
import react from '@vitejs/plugin-react';
import basicSsl from '@vitejs/plugin-basic-ssl';

const lanAddresses = Object.values(networkInterfaces())
  .flatMap(interfaces => interfaces || [])
  .filter(address => address.family === 'IPv4' && !address.internal)
  .map(address => address.address);

export default defineConfig({
  plugins: [react(), { ...basicSsl({ domains: ['localhost', '127.0.0.1', ...lanAddresses] }), apply: 'serve' }],
  server: {
    host: '0.0.0.0',
    proxy: {
      '/api': { target: 'http://127.0.0.1:5028', changeOrigin: true },
      '/vision-api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/vision-api/, ''),
      },
    },
  },
});
