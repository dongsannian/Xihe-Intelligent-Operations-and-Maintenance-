// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import axios from 'axios'
window.axios = axios

// ✅ 不要带 /api，这里就是 http://127.0.0.1:8000
// src/main.js
axios.defaults.baseURL = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

axios.defaults.timeout = 15000

axios.interceptors.request.use((config) => {
  const t = localStorage.getItem('token')
  if (t) config.headers.Authorization = `Bearer ${t}`
  return config
})

axios.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err?.response?.status === 401) {
      try { localStorage.removeItem('token') } catch {}
      const current = window.location.pathname + window.location.search
      if (!current.startsWith('/login')) {
        const redirect = encodeURIComponent(current)
        window.location.href = `/login?redirect=${redirect}`
      }
    }
    return Promise.reject(err)
  }
)

createApp(App).use(router).mount('#app')

