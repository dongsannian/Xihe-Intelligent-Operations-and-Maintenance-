<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">📡 应用告警中心</h1>

    <div class="bg-white p-4 rounded-2xl shadow">
      <table class="min-w-full">
        <thead>
          <tr class="border-b text-left">
            <th class="p-2">ID</th>
            <th class="p-2">告警标题</th>
            <th class="p-2">级别</th>
            <th class="p-2">时间</th>
            <th class="p-2 text-center">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="alert in alerts"
            :key="alert.id"
            class="hover:bg-gray-50 border-b"
          >
            <td class="p-2">{{ alert.id }}</td>
            <td class="p-2">{{ alert.message }}</td>
            <td class="p-2">{{ alert.level }}</td>
            <td class="p-2">{{ alert.timestamp }}</td>
            <td class="p-2 text-center">
              <button
                class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded"
                @click="analyzeAlert(alert)"
              >
                根因分析
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="analysis" class="mt-6 p-4 bg-gray-100 rounded-xl">
        <h2 class="font-semibold text-lg mb-2">🤖 根因分析结果</h2>
        <p class="text-gray-700 whitespace-pre-wrap">{{ analysis }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const alerts = ref([]);
const analysis = ref(null);

const backendURL = "http://192.168.192.129:8000"; // ✅ 修改为你后端实际 IP 或端口

async function loadAlerts() {
  try {
    const res = await axios.get(`${backendURL}/api/logs?keyword=告警`);
    alerts.value = res.data;
  } catch (err) {
    console.error("加载告警失败:", err);
  }
}

async function analyzeAlert(alert) {
  analysis.value = "正在分析中，请稍候...";
  try {
    const res = await axios.post(`${backendURL}/api/analyze`, {
      log_content: alert.message,
    });
    analysis.value = res.data.analysis;
  } catch (err) {
    analysis.value = "分析失败：" + err.message;
  }
}

onMounted(loadAlerts);
</script>

<style scoped>
table {
  border-collapse: collapse;
  width: 100%;
}
th {
  background-color: #f9fafb;
}
</style>

