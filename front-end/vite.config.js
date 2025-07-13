import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    allowedHosts: ['219fe11570f2.ngrok-free.app'], // ✅ exact ngrok domain
    proxy: {
      '/ws': {
        target: 'ws://localhost:8765',
        ws: true,
      },
    },
  },
});
