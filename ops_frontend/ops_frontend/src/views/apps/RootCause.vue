<template>
  <div class="p-6 space-y-6">
    <!-- 根因诊断 -->
    <div class="bg-white p-4 rounded-2xl shadow">
      <h1 class="text-2xl font-bold mb-4">🩺 根因分析与修复</h1>

      <div class="flex space-x-2 mb-4">
        <input
          v-model="service"
          placeholder="请输入服务名称（如 nginx、mysql）"
          class="border p-2 rounded w-1/2"
        />
        <button
          @click="analyzeRootCause"
          class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        >
          分析根因
        </button>
        <button
          @click="repairService"
          class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
        >
          一键修复
        </button>
      </div>

      <div v-if="loading" class="text-gray-500">正在分析，请稍候...</div>

      <div v-else-if="result" class="mt-4">
        <p><strong>服务名称：</strong>{{ result.service }}</p>
        <p><strong>根因诊断：</strong>{{ result.root_cause }}</p>
      </div>

      <div v-else class="text-gray-400">尚未分析，请输入服务名称。</div>

      <div
        v-if="repairResult"
        class="bg-green-50 border border-green-300 text-green-700 p-4 rounded-2xl mt-4"
      >
        <p><strong>修复结果：</strong>{{ repairResult.repair_action }}</p>
      </div>
    </div>

    <!-- 传播路径图 -->
    <div class="bg-white p-4 rounded-2xl shadow">
      <h2 class="text-lg font-semibold mb-3">📊 服务依赖与传播路径</h2>
      <div ref="chartRef" style="width: 100%; height: 500px;"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import * as echarts from "echarts";

const service = ref("");
const result = ref(null);
const repairResult = ref(null);
const loading = ref(false);
const chartRef = ref(null);
let chart;

// 根因分析
const analyzeRootCause = async () => {
  if (!service.value) return alert("请输入服务名称！");
  loading.value = true;
  try {
    const res = await axios.get(`http://127.0.0.1:8001/rootcause/${service.value}`);
    result.value = res.data;
  } catch (e) {
    alert("根因分析失败：" + e.message);
  } finally {
    loading.value = false;
  }
};

// 自动修复
const repairService = async () => {
  if (!service.value) return alert("请输入服务名称！");
  try {
    const res = await axios.get(`http://127.0.0.1:8001/repair/${service.value}`);
    repairResult.value = res.data;
  } catch (e) {
    alert("修复失败：" + e.message);
  }
};

// 初始化依赖图
const initChart = async () => {
  const { data } = await axios.get("http://127.0.0.1:8001/rootcause/graph");
  chart = echarts.init(chartRef.value);

  const option = {
    title: { text: "服务依赖与根因传播图", left: "center" },
    tooltip: { formatter: '{b}' },
    series: [
      {
        type: "graph",
        layout: "force",
        roam: true,
        label: { show: true },
        force: { repulsion: 200 },
        data: data.nodes.map(n => ({
          name: n.name,
          symbolSize: n.status === "abnormal" ? 60 : 40,
          itemStyle: { color: n.status === "abnormal" ? "#e74c3c" : "#1abc9c" }
        })),
        links: data.links.map(l => ({ source: l.source, target: l.target })),
      }
    ]
  };

  chart.setOption(option);
};

onMounted(initChart);
</script>

