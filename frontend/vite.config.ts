import react from '@vitejs/plugin-react'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'

const root = dirname(fileURLToPath(import.meta.url))
const apiProxyTarget = process.env.API_PROXY_TARGET ?? 'http://127.0.0.1:8000'

export default defineConfig({
  root,
  plugins: [react()],
  server: {
    host: process.env.VITE_HOST ?? '127.0.0.1',
    port: 4173,
    proxy: {
      '/api': { target: apiProxyTarget, changeOrigin: true },
    },
  },
  build: {
    outDir: resolve(root, 'dist'),
    emptyOutDir: true,
  },
})