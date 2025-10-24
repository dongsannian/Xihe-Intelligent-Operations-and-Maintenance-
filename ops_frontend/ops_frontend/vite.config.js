// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      'vue': 'vue/dist/vue.esm-bundler.js'  // ✅ 支持运行时模板编译（解决 runtime compilation 警告）
    }
  },
  server: {
    host: '0.0.0.0', // ✅ 允许局域网访问（192.168.192.129）
    port: 5173,       // 可改成 5178，如果 5173 被占用
    open: true,       // 启动后自动打开浏览器
    proxy: {
      // 后端 API 路径代理
      '/api': {
        target: 'http://127.0.0.1:8001',
        changeOrigin: true,
      },
      '/overview': {
        target: 'http://127.0.0.1:8001',
        changeOrigin: true,
      },
      '/bridge': {
        target: 'http://127.0.0.1:8001',
        changeOrigin: true,
      }
    }
  }
})

