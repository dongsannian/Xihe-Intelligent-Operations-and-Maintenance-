<template>
  <div class="poll-page">
    <!-- 顶部：面包屑 + 操作 -->
    <div class="page-header">
      <div class="left">
        <div class="title">硬件监控中心</div>
        <div class="filters">
          <label>时间范围</label>
          <select v-model="filters.time_range" @change="reload">
            <option value="7d">最近7天</option>
            <option value="30d">最近30天</option>
          </select>

          <label>硬件类型</label>
          <select v-model="filters.hw_type" @change="reload">
            <option>全部</option>
            <option>CPU</option>
            <option>GPU</option>
            <option>硬盘</option>
            <option>内存</option>
          </select>

          <label>区域</label>
          <select v-model="filters.zone" @change="reload">
            <option>全部</option>
            <option>华北</option>
            <option>华东</option>
            <option>华南</option>
          </select>

          <label>状态</label>
          <select v-model="filters.status" @change="reload">
            <option>全部</option>
            <option>已完成</option>
            <option>运行中</option>
            <option>已停止</option>
          </select>

          <button class="btn" @click="reload">搜索</button>
          <button class="btn ghost" @click="resetFilters">重置</button>
        </div>
      </div>

      <div class="right">
        <button class="btn primary">新建巡检任务</button>
        <button class="btn ghost">导出</button>
      </div>
    </div>

    <!-- KPI 卡片 -->
    <div class="kpi-grid">
      <KpiCard title="CPU使用率" :percent="summary.cpu.percent" :spark="summary.cpu.spark" />
      <KpiCard title="GPU使用率" :percent="summary.gpu.percent" :spark="summary.gpu.spark" />
      <KpiCard title="硬盘占用" :percent="summary.disk.percent" :spark="summary.disk.spark" />
      <KpiCard title="内存使用" :percent="summary.memory.percent" :spark="summary.memory.spark" />
    </div>

    <!-- 表格 -->
    <div class="table-wrap">
      <div class="table-title">硬件监控记录</div>
      <table class="table">
        <thead>
          <tr>
            <th>任务号</th>
            <!-- 新增：轮巡周期（位置在任务号与任务名称之间） -->
            <th>轮巡周期</th>
            <th>任务名称</th>
            <th>硬件类型</th>
            <th>设备/指标</th>
            <th>开始时间</th>
            <th>结束时间</th>
            <th>状态</th>
            <th style="width:120px;">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in records" :key="row.code">
            <td>{{ row.code }}</td>

            <!-- 新增：按硬件类型给出不同选项 -->
            <td>
              <select
                class="cycle-select"
                v-model="row.poll_cycle"
                @change="updateCycle(row)"
                :disabled="row.status === '已完成'"
                :title="`当前：${row.poll_cycle}`"
              >
                <option v-for="opt in getCycleOptions(row.hw_type)" :key="opt" :value="opt">
                  {{ opt }}
                </option>
              </select>
            </td>

            <td>{{ row.task_name }}</td>
            <td>{{ row.hw_type }}</td>
            <td>{{ row.device }} / {{ row.metric }}</td>
            <td>{{ row.start_time }}</td>
            <td>{{ row.end_time }}</td>
            <td>
              <span class="tag" :class="statusClass(row.status)">{{ row.status }}</span>
            </td>
            <td class="ops">
              <a href="javascript:;" @click="showDetail(row)">详情</a>
              <a href="javascript:;">导出</a>
              <a href="javascript:;" v-if="row.status === '运行中'">终止</a>
            </td>
          </tr>
          <tr v-if="!records.length">
            <td colspan="9" style="text-align:center;color:#999;">无数据</td>
          </tr>
        </tbody>
      </table>

      <!-- 分页 -->
      <div class="pager">
        <button class="btn ghost" :disabled="page<=1" @click="toPage(page-1)">上一页</button>
        <span class="pnum">第 {{ page }} / {{ totalPages }} 页</span>
        <button class="btn ghost" :disabled="page>=totalPages" @click="toPage(page+1)">下一页</button>
      </div>
    </div>

    <!-- 趋势 -->
    <div class="trend">
      <div class="trend-title">
        硬件性能趋势
        <div class="range">
          <button class="btn ghost" :class="{active: rangeDays===7}" @click="changeRange(7)">日</button>
          <button class="btn ghost" :class="{active: rangeDays===14}" @click="changeRange(14)">周</button>
          <button class="btn ghost" :class="{active: rangeDays===30}" @click="changeRange(30)">月</button>
        </div>
      </div>
      <canvas ref="trendCanvas" width="1200" height="280"></canvas>
      <div class="legend">
        <span class="dot cpu"></span>CPU
        <span class="dot gpu"></span>GPU
        <span class="dot mem"></span>内存
        <span class="dot disk"></span>硬盘
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import axios from 'axios'

/* 简易 KPI 卡片 */
const KpiCard = {
  props: { title: String, percent: Number, spark: Array },
  template: `
    <div class="kpi-card" :title="title+' '+percent+'%'">
      <div class="kpi-top">
        <div class="kpi-title">{{ title }}</div>
        <div class="kpi-pct">{{ (percent ?? 0).toFixed(1) }}%</div>
      </div>
      <div class="spark">
        <div v-for="(v,i) in (spark || [])" :key="i" class="bar" :style="{height: (v || 0) + '%'}"></div>
      </div>
    </div>
  `
}

const baseURL = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
const http = axios.create({ baseURL, timeout: 15000 })

const filters = reactive({
  time_range: '7d',
  hw_type: '全部',
  zone: '全部',
  status: '全部',
})
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

const summary = reactive({
  cpu: { percent: 0, spark: [] },
  gpu: { percent: 0, spark: [] },
  disk: { percent: 0, spark: [] },
  memory: { percent: 0, spark: [] },
})

const records = ref([])
const rangeDays = ref(7)
const trend = reactive({ x: [], cpu: [], gpu: [], memory: [], disk: [] })
const trendCanvas = ref(null)

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))

function statusClass(s) {
  return {
    done: s === '已完成',
    running: s === '运行中',
    stop: s === '已停止'
  }
}

/** 周期选项：按硬件类型返回不同候选 */
function getCycleOptions(hw) {
  const t = String(hw || '').toLowerCase()
  if (t.includes('cpu')) return ['30s', '1min', '5min']
  if (t.includes('gpu')) return ['30s', '1min', '5min']
  if (t.includes('内存') || t.includes('mem')) return ['1min', '2min', '5min']
  if (t.includes('硬盘') || t.includes('disk')) return ['30min', '1h', '2h']
  // 兜底
  return ['1min', '5min', '30min']
}

/** 默认值：每条记录初始化一个 poll_cycle（若后端未给） */
function ensureCycle(row) {
  if (!row.poll_cycle) {
    const opts = getCycleOptions(row.hw_type)
    row.poll_cycle = opts[0]
  }
}

async function fetchSummary() {
  const { data } = await http.get('/poll/summary')
  summary.cpu = data.cpu
  summary.gpu = data.gpu
  summary.disk = data.disk
  summary.memory = data.memory
}

async function fetchRecords() {
  const { data } = await http.get('/poll/records', {
    params: {
      time_range: filters.time_range,
      hw_type: filters.hw_type,
      zone: filters.zone,
      status: filters.status,
      page: page.value,
      page_size: pageSize.value,
    }
  })
  const list = data.list || []
  list.forEach(ensureCycle) // 给每条记录补上默认轮巡周期
  records.value = list
  total.value = data.total || 0
}

/** 保存用户更改的轮巡周期（若后端已提供接口则会调用） */
async function updateCycle(row) {
  try {
    // 如果你后端有此接口，请在 routers/poll.py 实现
    await http.post('/poll/update_cycle', {
      code: row.code,
      cycle: row.poll_cycle
    })
    // 成功提示可自行加 Toast；这里控制台提示一下
    console.log('周期已更新：', row.code, row.poll_cycle)
  } catch (e) {
    console.warn('更新周期失败（可能后端未实现 /poll/update_cycle）：', e?.response?.data || e.message)
  }
}

async function fetchTrend() {
  const { data } = await http.get('/poll/trend', { params: { range_days: rangeDays.value } })
  trend.x = data.x
  trend.cpu = data.cpu
  trend.gpu = data.gpu
  trend.memory = data.memory
  trend.disk = data.disk
  await nextTick()
  drawTrend()
}

// 画简单折线图（不引第三方库）
function drawTrend() {
  const cvs = trendCanvas.value
  if (!cvs) return
  const ctx = cvs.getContext('2d')
  const W = cvs.width, H = cvs.height
  ctx.clearRect(0, 0, W, H)

  // 坐标
  const padding = { l: 50, r: 20, t: 20, b: 40 }
  const chartW = W - padding.l - padding.r
  const chartH = H - padding.t - padding.b

  // y 轴：0~100
  ctx.strokeStyle = '#eee'
  ctx.beginPath()
  for (let i = 0; i <= 5; i++) {
    const y = padding.t + (chartH / 5) * i
    ctx.moveTo(padding.l, y)
    ctx.lineTo(W - padding.r, y)
  }
  ctx.stroke()

  // x 轴刻度
  ctx.fillStyle = '#999'
  ctx.font = '12px system-ui'
  const xs = trend.x || []
  const stepX = chartW / Math.max(1, xs.length - 1)
  for (let i = 0; i < xs.length; i += Math.ceil(xs.length / 6)) {
    const x = padding.l + stepX * i
    ctx.fillText(xs[i], x - 12, H - 12)
  }

  function drawLine(arr, colorClass) {
    if (!arr?.length) return
    const colorMap = {
      cpu: '#1677ff',
      gpu: '#22c55e',
      mem: '#eab308',
      disk: '#8b5cf6',
    }
    const color = colorMap[colorClass]
    ctx.strokeStyle = color
    ctx.lineWidth = 2
    ctx.beginPath()
    arr.forEach((v, i) => {
      const x = padding.l + i * stepX
      const y = padding.t + chartH * (1 - (v / 100))
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    })
    ctx.stroke()
  }

  drawLine(trend.cpu, 'cpu')
  drawLine(trend.gpu, 'gpu')
  drawLine(trend.memory, 'mem')
  drawLine(trend.disk, 'disk')
}

function reload() {
  page.value = 1
  fetchSummary()
  fetchRecords()
  fetchTrend()
}

function resetFilters() {
  filters.time_range = '7d'
  filters.hw_type = '全部'
  filters.zone = '全部'
  filters.status = '全部'
  reload()
}

function toPage(p) {
  page.value = p
  fetchRecords()
}

function changeRange(d) {
  rangeDays.value = d
  fetchTrend()
}

function showDetail(row) {
  alert(`【详情】\n任务号：${row.code}\n任务：${row.task_name}\n类型：${row.hw_type}\n设备/指标：${row.device}/${row.metric}\n开始：${row.start_time}\n结束：${row.end_time}\n状态：${row.status}\n轮巡周期：${row.poll_cycle}`)
}

onMounted(() => {
  reload()
  // 简单轮询刷新 KPI（1 分钟）
  setInterval(fetchSummary, 60 * 1000)
})
</script>

<style scoped>
.poll-page { padding: 16px 20px 40px; }

.page-header{
  display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:16px;
  border-bottom:1px dashed #eee; padding-bottom:12px;
}
.page-header .title{ font-size:18px; font-weight:600; margin-bottom:10px; }
.filters{ display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
.filters label{ color:#666; }
.filters select{ height:32px; border:1px solid #d9d9d9; border-radius:6px; padding:0 8px; background:#fff; }
.btn{
  height:32px; padding:0 12px; border-radius:6px; border:1px solid #d9d9d9; background:#f5f5f5; cursor:pointer;
}
.btn.ghost{ background:#fff; }
.btn.primary{ background:#1677ff; border-color:#1677ff; color:#fff; }

.kpi-grid{
  display:grid; grid-template-columns: repeat(4, 1fr); gap:16px; margin:16px 0 20px;
}
.kpi-card{
  background:#f5faff; border:1px solid #e6f0ff; border-radius:10px; padding:14px 16px; position:relative;
}
.kpi-top{ display:flex; justify-content:space-between; align-items:center; }
.kpi-title{ color:#333; }
.kpi-pct{ font-size:22px; font-weight:700; color:#1677ff; }
.spark{ display:flex; gap:4px; margin-top:10px; height:42px; align-items:flex-end; }
.spark .bar{ width:10px; background:#1677ff; opacity:.6; border-radius:2px; }

.table-wrap{ background:#fff; border:1px solid #eee; border-radius:10px; padding:12px; }
.table-title{ font-weight:600; margin:6px 0 10px; }
.table{ width:100%; border-collapse:collapse; }
.table th, .table td{
  border-bottom:1px solid #f1f1f1; padding:10px 8px; text-align:left; font-size:14px;
}
.ops a{ margin-right:8px; color:#1677ff; text-decoration:none; }
.tag{ padding:2px 8px; border-radius:12px; font-size:12px; }
.tag.done{ background:#ecfdf5; color:#22c55e; }
.tag.running{ background:#eff6ff; color:#1677ff; }
.tag.stop{ background:#fef2f2; color:#ef4444; }

.cycle-select{
  height:28px; padding:0 8px; border:1px solid #d9d9d9; border-radius:6px; background:#fff;
}

.pager{ display:flex; align-items:center; gap:10px; padding:12px 0 4px; }
.pager .pnum{ color:#666; }

.trend{ margin-top:16px; background:#fff; border:1px solid #eee; border-radius:10px; padding:12px; }
.trend-title{ display:flex; justify-content:space-between; align-items:center; font-weight:600; margin-bottom:8px; }
.range .btn{ margin-left:6px; }
.range .btn.active{ border-color:#1677ff; color:#1677ff; }
.legend{ display:flex; gap:18px; align-items:center; margin-top:6px; color:#666; }
.dot{ display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; }
.dot.cpu{ background:#1677ff; }
.dot.gpu{ background:#22c55e; }
.dot.mem{ background:#eab308; }
.dot.disk{ background:#8b5cf6; }
</style>

