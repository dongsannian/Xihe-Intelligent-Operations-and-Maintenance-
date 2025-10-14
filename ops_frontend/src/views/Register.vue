<template>
  <div class="register-container">
    <div class="form-box">
      <h2>注册账号</h2>
      <input v-model="username" type="text" placeholder="请输入用户名" class="input" />
      <input v-model="password" type="password" placeholder="请输入密码" class="input" />
      <input v-model="confirmPassword" type="password" placeholder="请再次输入密码" class="input" />

      <button @click="handleRegister" class="register-button">注册</button>

      <div class="login-link">
        已有账号？<a href="/login">点此登录</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const router = useRouter()

async function handleRegister() {
  if (!username.value || !password.value || !confirmPassword.value) {
    alert('请填写完整信息')
    return
  }

  if (password.value !== confirmPassword.value) {
    alert('两次密码不一致')
    return
  }

  try {
    await api.register({ username: username.value, password: password.value })
    alert('注册成功，请登录')
    router.push('/login')
  } catch (e) {
    alert(e?.response?.data?.detail || '注册失败')
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.form-box {
  width: 360px;
  padding: 30px;
  border: 1px solid #ddd;
  border-radius: 8px;
  text-align: center;
  background-color: white;
}

.input {
  width: 100%;
  padding: 10px 12px;
  margin-bottom: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}

.register-button {
  width: 100%;
  background-color: #1677ff;
  color: white;
  padding: 10px 0;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
}

.register-button:hover {
  background-color: #0958d9;
}

.login-link {
  margin-top: 16px;
  font-size: 14px;
}
</style>

