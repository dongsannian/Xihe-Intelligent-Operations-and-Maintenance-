// src/services/api.js
import axios from 'axios'
import router from '@/router'   // ✅ 引入你的路由实例（路径按你项目实际来）

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000',
  timeout: 15000, // 超时时间，可按需调整
})

// 请求拦截器：如果本地有 token，就带上
api.interceptors.request.use((config) => {
  const t = localStorage.getItem('token')
  if (t) config.headers.Authorization = `Bearer ${t}`
  return config
})

// ✅ 新增：响应拦截器
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err?.response?.status === 401) {
      // 清除本地 token
      localStorage.removeItem('token')
      // 获取当前路径，方便登录后跳回
      const current = router.currentRoute.value.fullPath
      // 跳转登录页，并带上 redirect 参数
      router.push({ path: '/login', query: { redirect: current } })
    }
    return Promise.reject(err)
  }
)

export default api

