import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    cors: {
      origin: [
        'http://localhost:5173',
        'https://72da959561a7.ngrok-free.app'
      ],
      credentials: true
    },
    allowedHosts: [
      'localhost',
      '72da959561a7.ngrok-free.app'
    ]
  }
})
