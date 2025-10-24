<template>
  <div class="login-container">
    <div class="header">
      <span class="title">羲和智维</span>
    </div>

    <div class="content">
      <div class="left">
        <p class="slogan">让运维更简单，让部署更智能</p>
      </div>

      <div class="right">
        <h2 class="welcome">欢迎登录</h2>
        <div class="register-link">没有账户？<a href="/register">点此注册</a></div>

        <input
          v-model="username"
          type="text"
          placeholder="请输入用户名"
          class="input"
          @keyup.enter="doLogin"
        />
        <input
          v-model="password"
          type="password"
          placeholder="请输入密码"
          class="input"
          @keyup.enter="doLogin"
        />

        <div class="remember-box">
          <input type="checkbox" id="remember" v-model="rememberMe" />
          <label for="remember">记住密码</label>
        </div>

        <button class="login-button" @click="doLogin" :disabled="loading">
          {{ loading ? '登录中…' : '登录' }}
        </button>

        <div class="forgot-password">已有账号，忘记密码？</div>
      </div>
    </div>

    <footer class="footer">
      © 2025 智能运维管家，保留所有权利
    </footer>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
const router = useRouter()
const username = ref(localStorage.getItem('remember_username') || '')
const password = ref(localStorage.getItem('remember_password') || '')
const rememberMe = ref(!!localStorage.getItem('remember_username'))
const loading = ref(false)

async function doLogin() {
  if (loading.value) return
  loading.value = true
  try {
    // 用环境变量里的 API 地址


const { data } = await axios.post('http://127.0.0.1:8001/api/auth/login', {
  username: username.value.trim(),
  password: password.value
})


    if (data?.message !== '登录成功') {
      throw new Error(data?.message || '登录失败')
    }

    // 后端没返回 token，这里自己写一个假 token 保证路由守卫能放行
    localStorage.setItem('token', 'dummy-token')
    localStorage.setItem('username', username.value)

    if (rememberMe.value) {
      localStorage.setItem('remember_username', username.value)
      localStorage.setItem('remember_password', password.value)
    } else {
      localStorage.removeItem('remember_username')
      localStorage.removeItem('remember_password')
    }

    const redirect = router.currentRoute.value.query.redirect || '/home'
    await router.replace(redirect)
  } catch (e) {
    alert(e?.response?.data?.detail || e?.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>






<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  height: 60px;
  padding: 0 20px;
  border-bottom: 1px solid #eee;
}

.title {
  font-size: 18px;
  font-weight: bold;
}

.content {
  display: flex;
  flex: 1;
  padding: 40px 80px;
  justify-content: space-between;
}

.left {
  text-align: center;
}

.slogan {
  margin-top: 20px;
  font-size: 18px;
  color: #555;
}

.right {
  width: 320px;
}

.welcome {
  font-size: 20px;
  margin-bottom: 10px;
}

.register-link {
  font-size: 14px;
  margin-bottom: 20px;
  text-align: right;
}

.input {
  width: 100%;
  padding: 10px 12px;
  margin-bottom: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}

.remember-box {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  font-size: 14px;
}

.login-button {
  width: 100%;
  background-color: #1677ff;
  color: white;
  padding: 10px 0;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
}

.login-button:hover {
  background-color: #0958d9;
}

.login-button:disabled {
  opacity: .6;
  cursor: not-allowed;
}

.forgot-password {
  margin-top: 16px;
  font-size: 13px;
  color: #666;
  text-align: right;
}

.footer {
  text-align: center;
  font-size: 12px;
  color: #aaa;
  padding: 20px 0;
}
</style>

