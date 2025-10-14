<template>
  <div class="sidebar">
    <div class="sidebar-header">日志管理系统</div>
    <el-menu
      default-active="3"
      class="sidebar-menu"
      mode="vertical"
      @select="handleMenuSelect"
    >
      <el-menu-item index="1">
        <i class="el-icon-menu"></i>
        <span>首页</span>
      </el-menu-item>
      <el-menu-item index="2">
        <i class="el-icon-data-line"></i>
        <span>轮巡数据</span>
      </el-menu-item>
      <el-menu-item index="3">
        <i class="el-icon-notebook-2"></i>
        <span>系统日志</span>
      </el-menu-item>
      <el-menu-item index="4">
        <i class="el-icon-bell"></i>
        <span>应用告警</span>
      </el-menu-item>
      <el-menu-item index="5">
        <i class="el-icon-question"></i>
        <span>问题解答</span>
      </el-menu-item>
      <el-menu-item index="6">
        <i class="el-icon-setting"></i>
        <span>系统设置</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// 菜单选择事件
const handleMenuSelect = (key) => {
  // 根据选择的菜单key跳转到对应的路由
  switch(key) {
    case '1':
      router.push('/home')
      break
    case '2':
      router.push('/data')
      break
    case '3':
      router.push('/logs')
      break
    case '4':
      router.push('/alerts')
      break
    case '5':
      router.push('/log-assistant')  // 问题解答页面路由
      break
    case '6':
      router.push('/settings')
      break
    default:
      break
  }
}
</script>

<style scoped>
.sidebar {
  width: 220px;
  background-color: #001529;
  color: #fff;
  height: 100vh;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
  padding: 20px;
  font-size: 18px;
  text-align: center;
  background-color: #1890ff;
  font-weight: bold;
}

.sidebar-menu {
  margin-top: 10px;
  background-color: #001529;
}

.sidebar-menu .el-menu-item {
  color: rgba(255, 255, 255, 0.7);
  height: 50px;
  line-height: 50px;
}

.sidebar-menu .el-menu-item.is-active {
  background-color: #1890ff;
  color: #fff;
}

.sidebar-menu .el-menu-item:hover {
  background-color: #1890ff20;
}
</style>
    