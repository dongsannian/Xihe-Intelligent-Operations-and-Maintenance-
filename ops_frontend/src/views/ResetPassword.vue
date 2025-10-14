<template>
  <div class="reset-password">
    <h2>重置密码</h2>
    <input v-model.trim="phone" placeholder="手机号" />
    <input v-model="newPassword" type="password" placeholder="新密码" />
    <button :disabled="loading" @click="doReset">{{ loading ? '提交中…' : '确定' }}</button>
    <router-link to="/">返回登录</router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const phone = ref('')
const newPassword = ref('')
const router = useRouter()

async function doReset() {
  try {
    await api.resetPassword({ phone: phone.value, new_password: newPassword.value })
    alert('重置成功')
    router.push('/')
  } catch (e) {
    alert(e?.response?.data?.detail || '重置失败')
  }
}
</script>


<style scoped>
/* 可继续复用你现有样式 */
</style>

