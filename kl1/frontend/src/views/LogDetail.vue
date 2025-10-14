<template>
  <div class="log-detail-page">
    <!-- 顶部导航栏 -->
    <div class="log-detail-breadcrumb">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item @click="goBack" style="cursor:pointer;">日志中心</el-breadcrumb-item>
        <el-breadcrumb-item>{{ getTypeName(type) }}</el-breadcrumb-item>
        <el-breadcrumb-item>查看详情</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 详情标题 -->
    <h2 class="log-detail-title" v-if="log?.level">
      {{ log.level === 'ERROR' ? '应用异常堆栈详情' : '日志详情' }}
    </h2>
    <h2 class="log-detail-title" v-else>
      日志详情
    </h2>

    <div class="log-detail-main" v-if="log">
      <!-- 左侧基本信息卡片 -->
      <div class="log-detail-card log-detail-info">
        <div class="log-detail-card-title">基本信息</div>
        <div class="log-detail-info-row"><span class="label">日志类型：</span>{{ getTypeName(type) }}</div>
        <div class="log-detail-info-row">
          <span class="label">日志级别：</span>
          <el-tag :type="levelType">{{ log.level || '-' }}</el-tag>
        </div>
        <div class="log-detail-info-row"><span class="label">事件时间：</span>{{ log.time || '-' }}</div>
        <div class="log-detail-info-row"><span class="label">关联用户ID：</span>{{ log.userId || '-' }}</div>
        <div class="log-detail-info-row"><span class="label">服务实例ID：</span>{{ log.instanceId || '-' }}</div>
        <div class="log-detail-info-row"><span class="label">请求ID：</span>{{ log.requestId || '-' }}</div>
      </div>

      <!-- 右侧事件描述卡片 -->
      <div class="log-detail-card log-detail-desc">
        <div class="log-detail-card-title">事件描述</div>
        <div class="log-detail-info-row"><span class="label">摘要描述：</span>{{ log.desc || log.summary || '-' }}</div>
        <div class="log-detail-info-row"><span class="label">操作来源IP：</span>{{ log.ip || '-' }}</div>
        <div class="log-detail-info-row"><span class="label">关联地理位置：</span>{{ log.location || '-' }}</div>
      </div>
    </div>

    <!-- 原始日志数据区 -->
    <div class="log-detail-card log-detail-raw" v-if="log">
      <div class="log-detail-card-title" style="display:flex;align-items:center;">
        原始日志数据
        <el-button type="text" size="small" @click="expandRaw = !expandRaw" style="margin-left:8px;">
          {{ expandRaw ? '折叠' : '展开全部' }}
        </el-button>
        <el-button type="text" size="small" @click="copyRawLog" style="margin-left:8px;">复制日志内容</el-button>
      </div>
      <el-scrollbar :height="expandRaw ? 320 : 120">
        <pre class="log-raw-pre">{{ formatRawLog(log) }}</pre>
      </el-scrollbar>
    </div>

    <!-- 链路追踪区 -->
    <div v-if="log.trace" class="log-detail-card log-detail-trace">
      <div class="log-detail-card-title">链路追踪</div>
      <div class="log-detail-trace-flow">
        <template v-for="(node, idx) in log.trace" :key="node.name">
          <el-tag :type="node.type || 'info'" size="large">{{ node.name }}</el-tag>
          <span v-if="idx < log.trace.length - 1" class="log-detail-trace-arrow">→</span>
        </template>
      </div>
    </div>

    <!-- 下方操作区 -->
    <div class="log-detail-actions">
      <el-button type="primary" @click="markHandled">标记为已处理</el-button>
      <el-button type="warning" @click="addToMonitor">加入运维告警</el-button>
      <el-button type="info" @click="archiveLog">归档此日志</el-button>
      <el-button @click="goBack">返回</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElBreadcrumb, ElBreadcrumbItem, ElTag, ElButton, ElMessageBox, ElMessage, ElScrollbar } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const type = route.params.type || 'basic'
const id = route.params.id

// 防空：初始化 log 对象
const log = ref({})

// 从路由参数解析日志对象
try {
  const rawLog = route.query.log
  log.value = rawLog ? JSON.parse(decodeURIComponent(rawLog)) : {}
} catch {
  log.value = {}
}

// 面包屑类型名称映射
const typeMap = {
  basic: '基础系统日志',
  app: '应用服务日志',
  security: '安全审计日志',
  performance: '性能监控日志',
  biz: '业务操作日志',
  storage: '日志存储与查询',
  custom: '定制化日志',
  actual: '实际应用日志'
}
const getTypeName = (t) => typeMap[t] || '未知日志'

// 日志级别对应标签颜色
const levelType = ref('info')
if (log.value.level === 'ERROR') levelType.value = 'danger'
else if (log.value.level === 'WARN') levelType.value = 'warning'

const expandRaw = ref(false)
const copyRawLog = () => {
  navigator.clipboard.writeText(formatRawLog(log.value))
  ElMessage.success('日志内容已复制到剪贴板。')
}

const markHandled = () => {
  ElMessage.success('该日志已标记为已处理，将不再重复告警。')
}
const addToMonitor = () => {
  ElMessage.success('已将该日志事件添加至运维告警策略。')
}
const archiveLog = () => {
  ElMessage.success('日志已归档，可在归档管理中查看。')
}

const formatRawLog = (row) => {
  if (!row) return ''
  try {
    if (typeof row.rawLog === 'string') {
      return row.rawLog
    }
    return JSON.stringify(row, null, 2)
  } catch {
    return String(row)
  }
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.log-detail-page {
  width: 100vw;
  min-height: 100vh;
  padding: 0;
  margin: 0;
  background: #fff;
  box-sizing: border-box;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
}
body, html, #app {
  background: #fff !important;
}
.log-detail-breadcrumb {
  margin: 0 0 18px 0;
  padding: 32px 48px 0 48px;
}
.log-detail-title {
  font-size: 28px;
  font-weight: bold;
  margin: 0 0 28px 0;
  padding: 0 48px;
}
.log-detail-main {
  display: flex;
  gap: 32px;
  margin-bottom: 32px;
  padding: 0 48px;
}
.log-detail-card {
  background: #fafbfc;
  border-radius: 12px;
  padding: 24px 28px 18px 28px;
  box-sizing: border-box;
  margin-bottom: 0;
  flex: 1;
  min-width: 0;
}
.log-detail-card-title {
  font-weight: bold;
  margin-bottom: 16px;
  font-size: 17px;
}
.log-detail-info-row {
  margin-bottom: 12px;
  font-size: 16px;
}
.label {
  color: #888;
  margin-right: 4px;
}
.log-detail-desc {
  min-width: 320px;
}
.log-detail-raw {
  margin-top: 32px;
  margin-bottom: 32px;
  padding: 0 48px;
}
.log-raw-pre {
  background: #181c20;
  color: #fff;
  font-size: 15px;
  border-radius: 8px;
  padding: 16px;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}
.log-detail-trace {
  margin-bottom: 32px;
  padding: 0 48px;
}
.log-detail-trace-flow {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
}
.log-detail-trace-arrow {
  color: #bbb;
  font-size: 22px;
  margin: 0 4px;
}
.log-detail-actions {
  display: flex;
  gap: 24px;
  margin-top: 24px;
  padding: 0 48px 48px 48px;
}
</style>
