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
        'https://b7be4e1f8a74.ngrok-free.app'
      ],
      credentials: true
    },
    allowedHosts: [
      'localhost',
      'b7be4e1f8a74.ngrok-free.app'
    ]
  }
})
