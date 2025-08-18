import path from 'node:path'
import vue from '@vitejs/plugin-vue'
import frappeui from 'frappe-ui/vite'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [
    frappeui({
    //   frappeProxy: {
    //     target: 'http://127.0.0.1:8002', // your frappe backend
    //   },
      frappeProxy: true,
      jinjaBootData: true,
      lucideIcons: true,
      buildConfig: {
        indexHtmlPath: '../linklite/www/links.html',
        emptyOutDir: true,
        sourcemap: true,
      },
    }),
    vue(),
  ],
  build: {
    chunkSizeWarningLimit: 1500,
    outDir: '../linklite/public/frontend',
    emptyOutDir: true,
    target: 'es2015',
    sourcemap: true,
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      'tailwind.config.js': path.resolve(__dirname, 'tailwind.config.js'),
    },
    extensions: ['.vue', '.ts', '.js', '.json'],
  },
  optimizeDeps: {
    include: ['frappe-ui > feather-icons', 'showdown', "engine.io-client",'highlight.js/lib/core', 'interactjs'],
  },
  server: {
    port: 8002,
    host: '127.0.0.1',
    allowedHosts: true,
  },
})
