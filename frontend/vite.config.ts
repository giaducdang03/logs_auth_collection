import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

const normalizeBasePath = (value?: string): string => {
  const raw = (value || '/').trim()
  if (!raw || raw === '/') {
    return '/'
  }

  const withLeadingSlash = raw.startsWith('/') ? raw : `/${raw}`
  return withLeadingSlash.endsWith('/') ? withLeadingSlash : `${withLeadingSlash}/`
}

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '.', '')
  const basePath = normalizeBasePath(env.VITE_BASE_PATH)

  return {
    base: basePath,
    plugins: [react()],
    server: {
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
        }
      }
    }
  }
})
