// src/services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000',
  timeout: 15000,
})

// 请求拦截：带 token
api.interceptors.request.use((config) => {
  const t = localStorage.getItem('token')
  if (t) config.headers.Authorization = `Bearer ${t}`
  return config
})

// 响应拦截：401 清 token + 跳登录（避免 import router 造成循环依赖）
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err?.response?.status === 401) {
      try { localStorage.removeItem('token') } catch {}
      const current = window.location.pathname + window.location.search
      const loginPath = '/login'
      // 避免在登录页重复跳转
      if (!current.startsWith(loginPath)) {
        const redirect = encodeURIComponent(current)
        window.location.href = `${loginPath}?redirect=${redirect}`
      }
    }
    return Promise.reject(err)
  }
)

export default api

