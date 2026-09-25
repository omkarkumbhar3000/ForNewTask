import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Port 5174 so it can run at the same time as the API dashboard (which uses 5173).
export default defineConfig({
  plugins: [react()],
  server: { port: 5174, open: true },
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          react: ['react', 'react-dom'],
          charts: ['recharts'],
        },
      },
    },
  },
})
