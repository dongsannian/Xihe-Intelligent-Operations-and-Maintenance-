<template>
  <div class="full-layout">
    <!-- 导航栏组件 -->
    <Sidebar />
    
    <!-- 内容区域 -->
    <div class="main-content">
      <router-view /> <!-- 路由视图，显示当前页面内容 -->
    </div>
  </div>
</template>

<script setup>
// 导入导航栏组件（确保路径正确）
import Sidebar from './Sidebar.vue'
</script>

<style scoped>
.full-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
  margin: 0;
  padding: 0;
  background-color: #000;
}

.main-content {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  background-color: #000;
  color: #fff;
  height: 100vh;
  box-sizing: border-box;
  margin: 0;
}
</style>
    