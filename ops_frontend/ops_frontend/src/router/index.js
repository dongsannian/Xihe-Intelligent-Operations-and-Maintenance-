// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import Poll from '../views/Poll.vue'
import Bridge from '../views/Bridge.vue'

// 路由表
const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: () => import('@/views/Register.vue') },
  { path: '/reset-password', component: () => import('@/views/ResetPassword.vue') },
  { path: '/home', component: Home },
  { path: '/poll', component: Poll },
  { path: '/bridge', component: Bridge },

  // ✅ 应用告警：直接跳 Prometheus
  {
    path: '/apps/alerts',
    name: 'AppAlerts',
    beforeEnter() {
      window.open('http://127.0.0.1:9090/rules#app_alerts', '_blank')
    },
    meta: { title: '应用告警' }
  },

{
  path: '/root-cause',
  name: 'RootCause',
  component: () => import('@/views/apps/RootCause.vue'),
  meta: { title: '根因分析' }
},


  // 通配符路由（404 回登录）
  { path: '/:pathMatch(.*)*', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  // 可选：每次切换页面返回顶部
  scrollBehavior() {
    return { top: 0 }
  }
})

// ✅ 登录态路由守卫（最小侵入）
const PUBLIC_PATHS = new Set([
  '/login',
  '/register',
  '/reset-password'
])

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const isPublic = PUBLIC_PATHS.has(to.path)

  // 未登录：禁止进入受保护页面，跳去登录页并带 redirect
  if (!token && !isPublic) {
    return next({ path: '/login', query: { redirect: to.fullPath } })
  }

  // 已登录：访问登录页则跳回首页
  if (token && to.path === '/login') {
    const redirect = (to.query && to.query.redirect) ? String(to.query.redirect) : '/home'
    return next(redirect)
  }

  next()
})

export default router
