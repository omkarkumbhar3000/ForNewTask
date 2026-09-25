import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// No recharts here: the Control Center is a decision surface, not a chart surface.
// Its job is to present state and collect approvals, so the bundle stays small.
// base:'./' because control_center.py serves dist/ from its own root.
export default defineConfig({
  plugins: [react()],
  base: './',
  server: { port: 5175 },
  build: { outDir: 'dist', sourcemap: false },
})
