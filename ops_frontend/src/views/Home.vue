<template>
  <div class="container">
    <!-- 侧边栏 -->
    <div class="sidebar">
      <div class="logo">羲和智维</div>
<ul>
  <li
    v-for="item in menuItems"
    :key="item.name"
    :class="{ active: item.name === currentPage }"
    @click="navigateTo(item)"
  >
    {{ item.name }}
  </li>
</ul>

    </div>

    <!-- 主体 -->
    <div class="main">
      <!-- 时间选择 -->
      <div class="time-selector">
        <button
          v-for="option in timeOptions"
          :key="option"
          :class="{ active: selectedTime === option }"
          @click="selectTime(option)"
        >
          {{ option }} 分钟
        </button>
      </div>

      <!-- 卡片区域 -->
      <div class="card-grid">
        <div
          v-for="card in cards"
          :key="card.title"
          class="card"
          @mouseover="hoverCard = card.title"
          @mouseleave="hoverCard = ''"
        >
          <h3>{{ card.title }}</h3>
          <p>{{ card.value }}</p>
          <transition name="fade">
            <div v-if="hoverCard === card.title" class="tooltip">
              <ul>
                <li v-for="(info, index) in card.tooltip" :key="index">{{ info }}</li>
              </ul>
            </div>
          </transition>
        </div>

        <!-- 添加模块卡片 -->
        <div class="card add-card" @click="handleAddModule">
          <div class="add-symbol">＋</div>
          <div class="add-label">添加模块</div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
import { useRouter } from 'vue-router'

export default {
  name: 'Home',
  setup() {
    const router = useRouter()

    const menuItems = [
      { name: '首页', path: '/home' },
      { name: '轮询日记', path: '/poll' },
      { name: '系统日志', path: '/bridge' },
      { name: '应用告警', path: '/apps/alerts' }, // ✅ 新增可跳转的菜单
      { name: '问题解答', path: '/qa' },
      { name: '系统设置', path: '/settings' }
    ]

    // 当前选中项
    let currentPage = '首页'

    const navigateTo = (item) => {
      currentPage = item.name
      router.push(item.path)
    }

    const timeOptions = [5, 10, 15]
    let selectedTime = 5
    let hoverCard = ''
    let cards = [
      { title: 'CPU', value: '', tooltip: [] },
      { title: '内存', value: '', tooltip: [] },
      { title: '磁盘', value: '', tooltip: [] },
      { title: '网络', value: '', tooltip: [] }
    ]
    let intervalId = null

    const selectTime = (min) => {
      selectedTime = min
      clearInterval(intervalId)
      setupAutoRefresh()
      fetchData()
    }

    const setupAutoRefresh = () => {
      intervalId = setInterval(fetchData, selectedTime * 60 * 1000)
    }

    const fetchData = async () => {
      try {
        const { data } = await axios.get('/overview/status')
        cards[0].value = data.cpu.total_usage + '%'
        cards[0].tooltip = [
          `CPU 总体使用率：${data.cpu.total_usage}%`,
          `每核使用率：${data.cpu.per_core.join('% / ')}%`,
          `用户空间占用：${data.cpu.user}%`,
          `内核空间占用：${data.cpu.system}%`,
          `IO等待占用：${data.cpu.iowait}%`
        ]

        cards[1].value = `${data.memory.used} / ${data.memory.total}`
        cards[1].tooltip = [
          `总内存：${data.memory.total}`,
          `已用内存：${data.memory.used}`,
          `空闲内存：${data.memory.free}`,
          `缓存内存：${data.memory.cached}`,
          `Swap：${data.memory.swap_used} / ${data.memory.swap_total}`
        ]

        cards[2].value = `${data.disk.usage_percent}%`
        cards[2].tooltip = [
          `读取速率：${data.disk.read_speed}`,
          `写入速率：${data.disk.write_speed}`,
          `I/O 等待时间：${data.disk.io_wait}`,
          `使用率：${data.disk.usage_percent}%`,
          `剩余空间：${data.disk.free_space}`
        ]

        cards[3].value = `${data.network.upload} ↑ / ${data.network.download} ↓`
        cards[3].tooltip = [
          `上传速率：${data.network.upload}`,
          `下载速率：${data.network.download}`,
          `丢包率：${data.network.packet_loss}%`,
          `延迟：${data.network.latency}`
        ]
      } catch (err) {
        console.error('获取系统状态失败：', err)
      }
    }

    const handleAddModule = () => {
      alert('你点击了添加模块！可在这里弹出表单或跳转页面')
    }

    // 页面加载时执行
    fetchData()
    setupAutoRefresh()

    return {
      menuItems,
      currentPage,
      navigateTo,
      timeOptions,
      selectedTime,
      hoverCard,
      cards,
      selectTime,
      handleAddModule
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
  height: 100vh;
  font-family: 'Segoe UI', sans-serif;
}

.sidebar {
  width: 200px;
  background: #2c3e50;
  color: white;
  padding: 20px 10px;
}

.sidebar .logo {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 30px;
  text-align: center;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  padding: 10px 20px;
  cursor: pointer;
  transition: background 0.2s;
}

.sidebar li:hover,
.sidebar li.active {
  background-color: #1abc9c;
}

.main {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.time-selector {
  margin-bottom: 20px;
}

.time-selector button {
  margin-right: 10px;
  padding: 8px 16px;
  background-color: #eee;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.time-selector button.active {
  background-color: #409eff;
  color: #fff;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

.card {
  position: relative;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 16px;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.2s;
}

.card:hover {
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.15);
}

.card h3 {
  margin-bottom: 10px;
}

.tooltip {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background: #f7f7f7;
  border: 1px solid #ccc;
  border-radius: 6px;
  padding: 10px;
  margin-top: 10px;
  font-size: 14px;
  z-index: 10;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 添加模块卡片样式 */
.add-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #aaa;
  border: 2px dashed #ccc;
  cursor: pointer;
}

.add-symbol {
  font-size: 40px;
  font-weight: bold;
}

.add-label {
  margin-top: 8px;
  font-size: 14px;
}
</style>

