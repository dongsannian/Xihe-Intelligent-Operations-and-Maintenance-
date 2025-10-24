<template>
  <div class="full-layout">
    

    <!-- 右侧主内容区 -->
    <div class="main-content">
      <!-- 顶部标签导航 -->
      <el-tabs v-model="activeTab" class="tab-header" @tab-click="handleTabClick">
        <el-tab-pane label="基础系统日志" name="basic" />
        <el-tab-pane label="应用服务日志" name="app" />
        <el-tab-pane label="安全审计日志" name="security" />
        <el-tab-pane label="性能监控日志" name="performance" />
        <el-tab-pane label="业务操作日志" name="biz" />
        <el-tab-pane label="日志存储与查询" name="storage" />
        <el-tab-pane label="定制化日志" name="custom" />
        <el-tab-pane label="实际应用日志" name="actual" />
      </el-tabs>

      <!-- 基础系统日志内容 -->
      <div class="content" v-if="activeTab === 'basic'">
        <div class="title-desc">实时掌握操作系统核心事件与运行状态，保障系统稳定与安全。</div>
        <div class="filter-bar">
          <el-date-picker
            v-model="timeRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            class="mr-2"
          />
          <el-select
            v-model="logLevel"
            placeholder="选择日志级别"
            class="mr-2"
          >
            <el-option label="全部" value="" />
            <el-option label="ERROR" value="ERROR" />
            <el-option label="WARN" value="WARN" />
            <el-option label="INFO" value="INFO" />
          </el-select>
          <el-input
            v-model="searchKey"
            placeholder="请输入事件类型或关键字搜索"
            class="mr-2"
            clearable
          />
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button type="success" @click="exportCSV">导出CSV</el-button>
          <el-button type="info" @click="exportJSON">导出JSON</el-button>
          <el-button type="warning" @click="configAlert">配置告警策略</el-button>
        </div>
        <el-table :data="tableData" border style="width: 100%; margin-top: 20px">
          <el-table-column prop="time" label="发生时间" />
          <el-table-column prop="level" label="日志级别">
            <template #default="scope">
              <el-tag :type="scope.row.level === 'ERROR' ? 'danger' : scope.row.level === 'WARN' ? 'warning' : 'info'">
                {{ scope.row.level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="type" label="事件类型" />
          <el-table-column prop="summary" label="日志摘要" />
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.status === '异常' ? 'danger' : scope.row.status === '处理中' ? 'warning' : 'success'">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button type="text" @click="goToDetail(scope.row)">查看详情</el-button>
              <el-button type="text" @click="markHandled(scope.row)">标记已处理</el-button>
              <el-button type="text" @click="archive(scope.row)">归档</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 应用服务日志内容 -->
      <div class="content" v-if="activeTab === 'app'">
        <div class="title-desc">实时监控关键应用服务的运行状态与异常，助力业务系统高可用。</div>
        <div class="filter-bar">
          <el-date-picker
            v-model="appTimeRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            class="mr-2"
          />
          <el-select
            v-model="appLogLevel"
            placeholder="选择日志级别"
            class="mr-2"
          >
            <el-option label="全部" value="" />
            <el-option label="ERROR" value="ERROR" />
            <el-option label="WARN" value="WARN" />
            <el-option label="INFO" value="INFO" />
          </el-select>
          <el-input
            v-model="appSearchKey"
            placeholder="请输入服务名称或关键字搜索"
            class="mr-2"
            clearable
          />
          <el-button type="primary" @click="handleAppSearch">搜索</el-button>
          <el-button type="success" @click="exportAppCSV">导出CSV</el-button>
          <el-button type="info" @click="exportAppJSON">导出JSON</el-button>
          <el-button type="warning" @click="configAppAlert">配置告警策略</el-button>
        </div>
        <el-table
          :data="appTableData"
          border
          style="width: 100%; margin-top: 20px"
        >
          <el-table-column prop="time" label="发生时间" />
          <el-table-column prop="level" label="日志级别">
            <template #default="scope">
              <el-tag :type="scope.row.level === 'ERROR' ? 'danger' : scope.row.level === 'WARN' ? 'warning' : 'info'">
                {{ scope.row.level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="service" label="服务名称" />
          <el-table-column prop="summary" label="日志摘要" />
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.status === '异常' ? 'danger' : scope.row.status === '处理中' ? 'warning' : 'success'">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button type="text" @click="goToDetail(scope.row)">查看详情</el-button>
              <el-button type="text" @click="markAppHandled(scope.row)">标记已处理</el-button>
              <el-button type="text" @click="archiveApp(scope.row)">归档</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 安全审计日志内容 -->
      <div class="content" v-if="activeTab === 'security'">
        <div class="title-desc">记录和追踪系统安全相关事件，提升安全合规与风险防控能力。</div>
        <div class="filter-bar">
          <el-date-picker
            v-model="securityTimeRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            class="mr-2"
          />
          <el-select
            v-model="securityLogLevel"
            placeholder="选择日志级别"
            class="mr-2"
          >
            <el-option label="全部" value="" />
            <el-option label="ERROR" value="ERROR" />
            <el-option label="WARN" value="WARN" />
            <el-option label="INFO" value="INFO" />
          </el-select>
          <el-input
            v-model="securitySearchKey"
            placeholder="请输入安全事件或关键字搜索"
            class="mr-2"
            clearable
          />
          <el-button type="primary" @click="handleSecuritySearch">搜索</el-button>
          <el-button type="success" @click="exportSecurityCSV">导出CSV</el-button>
          <el-button type="info" @click="exportSecurityJSON">导出JSON</el-button>
          <el-button type="warning" @click="configSecurityAlert">配置告警策略</el-button>
        </div>
        <el-table
          :data="securityTableData"
          border
          style="width: 100%; margin-top: 20px"
        >
          <el-table-column prop="time" label="发生时间" />
          <el-table-column prop="level" label="日志级别">
            <template #default="scope">
              <el-tag :type="scope.row.level === 'ERROR' ? 'danger' : scope.row.level === 'WARN' ? 'warning' : 'info'">
                {{ scope.row.level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="event" label="安全事件" />
          <el-table-column prop="summary" label="日志摘要" />
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.status === '异常' ? 'danger' : scope.row.status === '处理中' ? 'warning' : 'success'">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button type="text" @click="goToDetail(scope.row)">查看详情</el-button>
              <el-button type="text" @click="markSecurityHandled(scope.row)">标记已处理</el-button>
              <el-button type="text" @click="archiveSecurity(scope.row)">归档</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 性能监控日志内容 -->
      <div class="content" v-if="activeTab === 'performance'">
        <div class="title-desc">监控系统与应用性能指标，及时发现性能瓶颈与异常。</div>
        <div class="filter-bar">
          <el-date-picker
            v-model="perfTimeRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            class="mr-2"
          />
          <el-select
            v-model="perfLogLevel"
            placeholder="选择日志级别"
            class="mr-2"
          >
            <el-option label="全部" value="" />
            <el-option label="ERROR" value="ERROR" />
            <el-option label="WARN" value="WARN" />
            <el-option label="INFO" value="INFO" />
          </el-select>
          <el-input
            v-model="perfSearchKey"
            placeholder="请输入性能项或关键字搜索"
            class="mr-2"
            clearable
          />
          <el-button type="primary" @click="handlePerfSearch">搜索</el-button>
          <el-button type="success" @click="exportPerfCSV">导出CSV</el-button>
          <el-button type="info" @click="exportPerfJSON">导出JSON</el-button>
          <el-button type="warning" @click="configPerfAlert">配置告警策略</el-button>
        </div>
        <el-table
          :data="perfTableData"
          border
          style="width: 100%; margin-top: 20px"
        >
          <el-table-column prop="time" label="发生时间" />
          <el-table-column prop="level" label="日志级别">
            <template #default="scope">
              <el-tag :type="scope.row.level === 'ERROR' ? 'danger' : scope.row.level === 'WARN' ? 'warning' : 'info'">
                {{ scope.row.level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="metric" label="性能项" />
          <el-table-column prop="summary" label="日志摘要" />
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.status === '异常' ? 'danger' : scope.row.status === '处理中' ? 'warning' : 'success'">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button type="text" @click="goToDetail(scope.row)">查看详情</el-button>
              <el-button type="text" @click="markPerfHandled(scope.row)">标记已处理</el-button>
              <el-button type="text" @click="archivePerf(scope.row)">归档</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 业务操作日志内容 -->
      <div class="content" v-if="activeTab === 'biz'">
        <div class="title-desc">记录用户及系统的业务操作行为，便于追溯与分析。</div>
        <div class="filter-bar">
          <el-date-picker
            v-model="bizTimeRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            class="mr-2"
          />
          <el-select
            v-model="bizLogLevel"
            placeholder="选择日志级别"
            class="mr-2"
          >
            <el-option label="全部" value="" />
            <el-option label="ERROR" value="ERROR" />
            <el-option label="WARN" value="WARN" />
            <el-option label="INFO" value="INFO" />
          </el-select>
          <el-input
            v-model="bizSearchKey"
            placeholder="请输入操作类型或关键字搜索"
            class="mr-2"
            clearable
          />
          <el-button type="primary" @click="handleBizSearch">搜索</el-button>
          <el-button type="success" @click="exportBizCSV">导出CSV</el-button>
          <el-button type="info" @click="exportBizJSON">导出JSON</el-button>
          <el-button type="warning" @click="configBizAlert">配置告警策略</el-button>
        </div>
        <el-table
          :data="bizTableData"
          border
          style="width: 100%; margin-top: 20px"
        >
          <el-table-column prop="time" label="发生时间" />
          <el-table-column prop="level" label="日志级别">
            <template #default="scope">
              <el-tag :type="scope.row.level === 'ERROR' ? 'danger' : scope.row.level === 'WARN' ? 'warning' : 'info'">
                {{ scope.row.level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="action" label="操作类型" />
          <el-table-column prop="summary" label="日志摘要" />
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.status === '异常' ? 'danger' : scope.row.status === '处理中' ? 'warning' : 'success'">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button type="text" @click="goToDetail(scope.row)">查看详情</el-button>
              <el-button type="text" @click="markBizHandled(scope.row)">标记已处理</el-button>
              <el-button type="text" @click="archiveBiz(scope.row)">归档</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 日志存储与查询内容 -->
      <div class="content" v-if="activeTab === 'storage'">
        <div class="title-desc">统一管理日志存储，支持高效检索与归档。</div>
        <div class="filter-bar">
          <el-date-picker
            v-model="storageTimeRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            class="mr-2"
          />
          <el-input
            v-model="storageSearchKey"
            placeholder="请输入存储类型或关键字搜索"
            class="mr-2"
            clearable
          />
          <el-button type="primary" @click="handleStorageSearch">搜索</el-button>
          <el-button type="success" @click="exportStorageCSV">导出CSV</el-button>
          <el-button type="info" @click="exportStorageJSON">导出JSON</el-button>
        </div>
        <el-table
          :data="storageTableData"
          border
          style="width: 100%; margin-top: 20px"
        >
          <el-table-column prop="time" label="归档时间" />
          <el-table-column prop="type" label="存储类型" />
          <el-table-column prop="summary" label="日志摘要" />
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.status === '失败' ? 'danger' : scope.row.status === '处理中' ? 'warning' : 'success'">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button type="text" @click="viewStorageDetail(scope.row)">查看详情</el-button>
              <el-button type="text" @click="archiveStorage(scope.row)">归档</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 定制化日志内容 -->
      <div class="content" v-if="activeTab === 'custom'">
        <div class="title-desc">支持自定义日志采集与展示，满足个性化需求。</div>
        <div class="filter-bar">
          <el-date-picker
            v-model="customTimeRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            class="mr-2"
          />
          <el-input
            v-model="customSearchKey"
            placeholder="请输入自定义标签或关键字搜索"
            class="mr-2"
            clearable
          />
          <el-button type="primary" @click="handleCustomSearch">搜索</el-button>
          <el-button type="success" @click="exportCustomCSV">导出CSV</el-button>
          <el-button type="info" @click="exportCustomJSON">导出JSON</el-button>
        </div>
        <el-table
          :data="customTableData"
          border
          style="width: 100%; margin-top: 20px"
        >
          <el-table-column prop="time" label="记录时间" />
          <el-table-column prop="tag" label="自定义标签" />
          <el-table-column prop="summary" label="日志摘要" />
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.status === '异常' ? 'danger' : scope.row.status === '处理中' ? 'warning' : 'success'">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button type="text" @click="viewCustomDetail(scope.row)">查看详情</el-button>
              <el-button type="text" @click="archiveCustom(scope.row)">归档</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 实际应用日志内容 -->
      <div class="content" v-if="activeTab === 'actual'">
        <div class="title-desc">展示实际生产环境中的日志样例，便于参考与分析。</div>
        <div class="filter-bar">
          <el-date-picker
            v-model="actualTimeRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            class="mr-2"
          />
          <el-input
            v-model="actualSearchKey"
            placeholder="请输入日志内容或关键字搜索"
            class="mr-2"
            clearable
          />
          <el-button type="primary" @click="handleActualSearch">搜索</el-button>
          <el-button type="success" @click="exportActualCSV">导出CSV</el-button>
          <el-button type="info" @click="exportActualJSON">导出JSON</el-button>
        </div>
        <el-table
          :data="actualTableData"
          border
          style="width: 100%; margin-top: 20px"
        >
          <el-table-column prop="time" label="日志时间" />
          <el-table-column prop="content" label="日志内容" />
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.status === '异常' ? 'danger' : scope.row.status === '处理中' ? 'warning' : 'success'">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button type="text" @click="viewActualDetail(scope.row)">查看详情</el-button>
              <el-button type="text" @click="archiveActual(scope.row)">归档</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMenu, ElMenuItem, ElTabs, ElTabPane, ElDatePicker, ElSelect, ElOption, ElInput, ElButton, ElTable, ElTableColumn, ElTag } from 'element-plus'

// 响应式数据
const activeTab = ref('basic') // 当前激活的标签
const timeRange = ref([])      // 时间范围
const logLevel = ref('')       // 日志级别
const searchKey = ref('')      // 搜索关键字
const tableData = ref([        // 模拟表格数据
  {
    time: '2024-01-20 14:30:25',
    level: 'ERROR',
    type: '系统服务启动失败',
    summary: '系统服务sshd启动失败，返回错误码1',
    status: '异常'
  },
  {
    time: '2024-01-20 14:28:15',
    level: 'WARN',
    type: '系统资源使用率',
    summary: 'CPU使用率超过80%，请关注系统负载',
    status: '处理中'
  },
  {
    time: '2024-01-20 14:25:00',
    level: 'INFO',
    type: '系统例行检查',
    summary: '系统例行检查完成，未发现异常',
    status: '正常'
  }
])

const appTimeRange = ref([])
const appLogLevel = ref('')
const appSearchKey = ref('')
const appTableData = ref([
  {
    time: '2024-01-20 15:10:12',
    level: 'ERROR',
    service: '订单服务',
    summary: '订单服务启动失败，端口被占用',
    status: '异常'
  },
  {
    time: '2024-01-20 15:05:33',
    level: 'WARN',
    service: '支付服务',
    summary: '支付服务响应时间超过2秒',
    status: '处理中'
  },
  {
    time: '2024-01-20 15:00:00',
    level: 'INFO',
    service: '用户服务',
    summary: '用户服务健康检查通过',
    status: '正常'
  }
])

// 安全审计日志
const securityTimeRange = ref([])
const securityLogLevel = ref('')
const securitySearchKey = ref('')
const securityTableData = ref([
  { time: '2024-01-20 16:00:00', level: 'ERROR', event: '登录失败', summary: '管理员多次登录失败，触发锁定', status: '异常' },
  { time: '2024-01-20 15:55:00', level: 'WARN', event: '权限变更', summary: '用户权限被提升，请核查', status: '处理中' },
  { time: '2024-01-20 15:50:00', level: 'INFO', event: '安全扫描', summary: '定期安全扫描完成，无高危风险', status: '正常' }
])

// 性能监控日志
const perfTimeRange = ref([])
const perfLogLevel = ref('')
const perfSearchKey = ref('')
const perfTableData = ref([
  { time: '2024-01-20 17:00:00', level: 'ERROR', metric: '内存使用率', summary: '内存使用率超过90%', status: '异常' },
  { time: '2024-01-20 16:55:00', level: 'WARN', metric: '磁盘IO', summary: '磁盘IO延迟升高', status: '处理中' },
  { time: '2024-01-20 16:50:00', level: 'INFO', metric: '网络带宽', summary: '网络带宽使用正常', status: '正常' }
])

// 业务操作日志
const bizTimeRange = ref([])
const bizLogLevel = ref('')
const bizSearchKey = ref('')
const bizTableData = ref([
  { time: '2024-01-20 18:00:00', level: 'ERROR', action: '删除数据', summary: '用户误删重要数据', status: '异常' },
  { time: '2024-01-20 17:55:00', level: 'WARN', action: '批量导入', summary: '批量导入部分失败', status: '处理中' },
  { time: '2024-01-20 17:50:00', level: 'INFO', action: '登录', summary: '用户正常登录', status: '正常' }
])

// 日志存储与查询
const storageTimeRange = ref([])
const storageSearchKey = ref('')
const storageTableData = ref([
  { time: '2024-01-20 19:00:00', type: '本地存储', summary: '本地归档成功', status: '成功' },
  { time: '2024-01-20 18:55:00', type: '云存储', summary: '云端归档处理中', status: '处理中' },
  { time: '2024-01-20 18:50:00', type: '远程备份', summary: '远程备份失败', status: '失败' }
])

// 定制化日志
const customTimeRange = ref([])
const customSearchKey = ref('')
const customTableData = ref([
  { time: '2024-01-20 20:00:00', tag: '自定义1', summary: '自定义日志内容1', status: '正常' },
  { time: '2024-01-20 19:55:00', tag: '自定义2', summary: '自定义日志内容2', status: '处理中' },
  { time: '2024-01-20 19:50:00', tag: '自定义3', summary: '自定义日志内容3', status: '异常' }
])

// 实际应用日志
const actualTimeRange = ref([])
const actualSearchKey = ref('')
const actualTableData = ref([
  { time: '2024-01-20 21:00:00', content: '2024-01-20 21:00:00 [INFO] 服务启动完成', status: '正常' },
  { time: '2024-01-20 20:55:00', content: '2024-01-20 20:55:00 [WARN] 内存使用率高', status: '处理中' },
  { time: '2024-01-20 20:50:00', content: '2024-01-20 20:50:00 [ERROR] 数据库连接失败', status: '异常' }
])

const router = useRouter()

// 左侧菜单选择事件
const handleMenuSelect = (key) => {
  console.log('左侧菜单选中：', key)
  // 可根据菜单key实现路由跳转
  // if (key === '3') router.push('/logs')
  if (key === '5') {  // 这是新增的第1行
    router.push('/log-assistant')  // 这是新增的第2行（跳转你的对话框页面）
  }
}

// 标签页切换事件
const handleTabClick = (tab) => {
  console.log('切换到标签：', tab.name)
}

// 搜索与导出方法
const handleSearch = () => { console.log('基础日志搜索：', { timeRange, logLevel, searchKey }) }
const exportCSV = () => { console.log('导出基础日志CSV') }
const exportJSON = () => { console.log('导出基础日志JSON') }
const configAlert = () => { console.log('配置基础日志告警') }

const handleAppSearch = () => { console.log('应用日志搜索：', { appTimeRange, appLogLevel, appSearchKey }) }
const exportAppCSV = () => { console.log('导出应用日志CSV') }
const exportAppJSON = () => { console.log('导出应用日志JSON') }
const configAppAlert = () => { console.log('配置应用日志告警') }

const handleSecuritySearch = () => { console.log('安全日志搜索：', { securityTimeRange, securityLogLevel, securitySearchKey }) }
const exportSecurityCSV = () => { console.log('导出安全日志CSV') }
const exportSecurityJSON = () => { console.log('导出安全日志JSON') }
const configSecurityAlert = () => { console.log('配置安全日志告警') }

const handlePerfSearch = () => { console.log('性能日志搜索：', { perfTimeRange, perfLogLevel, perfSearchKey }) }
const exportPerfCSV = () => { console.log('导出性能日志CSV') }
const exportPerfJSON = () => { console.log('导出性能日志JSON') }
const configPerfAlert = () => { console.log('配置性能日志告警') }

const handleBizSearch = () => { console.log('业务日志搜索：', { bizTimeRange, bizLogLevel, bizSearchKey }) }
const exportBizCSV = () => { console.log('导出业务日志CSV') }
const exportBizJSON = () => { console.log('导出业务日志JSON') }
const configBizAlert = () => { console.log('配置业务日志告警') }

const handleStorageSearch = () => { console.log('存储日志搜索：', { storageTimeRange, storageSearchKey }) }
const exportStorageCSV = () => { console.log('导出存储日志CSV') }
const exportStorageJSON = () => { console.log('导出存储日志JSON') }

const handleCustomSearch = () => { console.log('定制日志搜索：', { customTimeRange, customSearchKey }) }
const exportCustomCSV = () => { console.log('导出定制日志CSV') }
const exportCustomJSON = () => { console.log('导出定制日志JSON') }

const handleActualSearch = () => { console.log('实际日志搜索：', { actualTimeRange, actualSearchKey }) }
const exportActualCSV = () => { console.log('导出实际日志CSV') }
const exportActualJSON = () => { console.log('导出实际日志JSON') }

// 日志操作方法
const goToDetail = (row) => {
  router.push({
    name: 'LogDetail',
    query: { log: encodeURIComponent(JSON.stringify(row)) }
  })
}

const markHandled = (row) => { console.log('标记基础日志已处理：', row) }
const archive = (row) => { console.log('归档基础日志：', row) }

const markAppHandled = (row) => { console.log('标记应用日志已处理：', row) }
const archiveApp = (row) => { console.log('归档应用日志：', row) }

const markSecurityHandled = (row) => { console.log('标记安全日志已处理：', row) }
const archiveSecurity = (row) => { console.log('归档安全日志：', row) }

const markPerfHandled = (row) => { console.log('标记性能日志已处理：', row) }
const archivePerf = (row) => { console.log('归档性能日志：', row) }

const markBizHandled = (row) => { console.log('标记业务日志已处理：', row) }
const archiveBiz = (row) => { console.log('归档业务日志：', row) }

const viewStorageDetail = (row) => { console.log('查看存储日志详情：', row) }
const archiveStorage = (row) => { console.log('归档存储日志：', row) }

const viewCustomDetail = (row) => { console.log('查看定制日志详情：', row) }
const archiveCustom = (row) => { console.log('归档定制日志：', row) }

const viewActualDetail = (row) => { console.log('查看实际日志详情：', row) }
const archiveActual = (row) => { console.log('归档实际日志：', row) }
</script>

<style scoped>
.full-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* 左侧导航栏样式 */
.sidebar {
  width: 220px;
  background-color: #001529;
  color: #fff;
  height: 100%;
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

/* 右侧主内容区样式 */
.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #f5f7fa;
}

.tab-header {
  margin-bottom: 20px;
  background-color: #fff;
  padding: 10px;
  border-radius: 4px;
}

.content {
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.title-desc {
  font-size: 14px;
  color: #666;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px dashed #e8e8e8;
}

.filter-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.mr-2 {
  margin-right: 10px;
}
</style>
/* 修改最外层布局，去除默认边距 */
.full-layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
  margin: 0; /* 新增：去除外部边距 */
  padding: 0; /* 新增：去除外部内边距 */
  background-color: #000; /* 保持黑色背景 */
}

/* 左侧导航栏全屏高度 */
.sidebar {
  width: 220px;
  background-color: #001529;
  color: #fff;
  height: 100vh; /* 修改为100vh确保全屏高度 */
  box-shadow: 2px 0 6px rgba(255, 255, 255, 0.1); /* 调整阴影适应黑色背景 */
  margin: 0; /* 去除边距 */
}

/* 右侧主内容区充满剩余空间 */
.main-content {
  flex: 1;
  padding: 15px; /* 适当减少内边距 */
  overflow-y: auto;
  background-color: #000;
  color: #fff;
  height: 100vh; /* 确保全屏高度 */
  box-sizing: border-box; /* 新增：确保内边距不影响整体尺寸 */
  margin: 0; /* 去除边距 */
}

/* 标签页容器样式调整 */
.tab-header {
  margin-bottom: 0px;
  background-color: #1a1a1a;
  padding: 10px;
  border-radius: 4px;
  width: 100%; /* 确保宽度100% */
  box-sizing: border-box; /* 确保内边距不影响宽度 */
}

/* 内容区域样式调整 */
.content {
  background-color: #1a1a1a;
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(255, 255, 255, 0.1);
  color: #fff;
  width: 100%; /* 确保宽度100% */
  box-sizing: border-box; /* 确保内边距不影响宽度 */
}

/* 表格样式调整，确保充满容器 */
.el-table {
  width: 100% !important; /* 强制表格宽度100% */
}

/* 全局去除body可能存在的边距 */
body {
  margin: 0;
  padding: 0;
  overflow: hidden;
}
