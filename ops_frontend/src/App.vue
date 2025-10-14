<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function handleLogout() {
  if (!confirm('确定要退出当前账号吗？')) return
  try {
    // 如果后端有接口，可调用：
    // await fetch('/api/auth/logout', { method: 'POST', credentials: 'include' })
  } finally {
    localStorage.removeItem('token') // 清理本地token
    router.push('/login')            // 跳转登录页
  }
}
</script>

<template>
  <div class="app-container">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <h2 class="logo">运维管家</h2>
      <nav>
        <router-link to="/home" class="sidebar-link">首页</router-link>
        <router-link to="/poll" class="sidebar-link">轮询日志</router-link>
        <router-link to="/settings" class="sidebar-link">系统设置</router-link>
        <router-link to="/bridge" class="sidebar-link">子系统页面</router-link>

        <!-- 新增：退出账号按钮 -->
        <button class="sidebar-link" @click="handleLogout">退出账号</button>
      </nav>
    </aside>

    <!-- 主体内容区域 -->
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  font-family: sans-serif;
}

.sidebar {
  width: 200px;
  background-color: #001529;
  color: #fff;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.logo {
  font-size: 20px;
  margin-bottom: 30px;
  color: #fff;
}

.sidebar-link {
  display: block;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 4px;
  color: white;
  text-decoration: none;
  transition: background-color 0.2s;
  text-align: left;
  width: 100%;
}

.sidebar-link:hover,
.router-link-exact-active {
  background-color: #1890ff;
}

.main {
  flex: 1;
  padding: 20px;
  background-color: #f0f2f5;
}

/* 让退出按钮的样式和 router-link 一致 */
button.sidebar-link {
  background: none;
  border: none;
  cursor: pointer;
}
</style>

