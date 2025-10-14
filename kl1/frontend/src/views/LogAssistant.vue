<template>
  <div class="page-container">
    <!-- 页面头部（导航栏） -->
    <header class="page-header">
      <div class="logo">日志管理系统</div>
      <nav class="nav-menu">
        <el-menu mode="horizontal" :default-active="activeNav">
          <el-menu-item index="dashboard">仪表盘</el-menu-item>
          <el-menu-item index="log-assistant" :route="{ name: 'LogAssistant' }">日志助手</el-menu-item>
          <el-menu-item index="settings">系统设置</el-menu-item>
        </el-menu>
      </nav>
    </header>

    <!-- 页面主体内容（原 LogAssistantCore 的内容） -->
    <main class="page-content">
      <div class="log-assistant-core">
        <!-- 标题与说明 -->
        <div class="section-intro">
          <h2>智能日志助手</h2>
          <p>通过对话方式管理和分析日志，支持查询、筛选、导出等操作</p>
        </div>

        <!-- 主体交互区 -->
        <div class="main-layout">
          <!-- 左侧对话区 -->
          <div class="chat-column">
            <div class="chat-history-scroll">
              <div
                v-for="(msg, idx) in chatMessages"
                :key="idx"
                class="chat-message"
                :class="{ 'user-message': msg.isUser }"
              >
                <div class="chat-avatar" :style="{ background: msg.isUser ? '#409eff' : '#67c23a' }">
                  {{ msg.isUser ? '你' : 'AI' }}
                </div>
                <div class="chat-content">
                  <div class="chat-text">{{ msg.text }}</div>
                  <div class="chat-time">{{ formatTime(msg.timestamp) }}</div>
                </div>
              </div>
            </div>
            <!-- 输入区 -->
            <div class="chat-input-area">
              <el-input
                v-model="chatInput"
                placeholder="请输入指令（如：分析今日ERROR日志）"
                clearable
                @keyup.enter="sendMessage"
              />
              <el-button type="primary" icon="el-icon-send" @click="sendMessage">发送</el-button>
            </div>
          </div>

          <!-- 右侧结果区 -->
          <div class="result-column">
            <!-- 推荐操作 -->
            <div class="prompt-section">
              <div class="section-title">推荐操作</div>
              <el-tag
                v-for="(prompt, idx) in prompts"
                :key="idx"
                type="info"
                @click="handlePrompt(prompt)"
              >
                {{ prompt }}
              </el-tag>
            </div>

            <!-- 日志表格（已移除日志结果板块） -->
            <!--
            <div class="log-table-section">
              <div class="section-title">日志结果</div>
              <el-table :data="logTableData" border style="width: 100%">
                <el-table-column prop="time" label="时间" />
                <el-table-column prop="level" label="级别">
                  <template #default="scope">
                    <el-tag :type="getTagType(scope.row.level)">{{ scope.row.level }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="type" label="类型" />
                <el-table-column prop="message" label="内容" />
                <el-table-column label="操作">
                  <template #default="scope">
                    <el-button type="text" @click="handleDetail(scope.row)">详情</el-button>
                    <el-button type="text" @click="handleArchive(scope.row)">归档</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
            -->

            <!-- 操作历史 -->
            <div class="history-section">
              <div class="section-title">操作历史</div>
              <div
                v-for="(hist, idx) in historyRecords"
                :key="idx"
                class="history-item"
              >
                <div class="history-text">{{ hist.text }}</div>
                <div class="history-time">{{ formatTime(hist.timestamp) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="page-footer">
      <p>© 2024 日志管理系统 | 版本 v1.0.0</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { ElTag, ElInput, ElButton, ElMessage } from 'element-plus';
import { format } from 'date-fns';
import { generateLogReport, getLogs } from '@/api/logs';

const chatInput = ref('');
const chatMessages = ref([
  { text: '您好，我可以帮您分析日志，试试输入指令或点击推荐操作吧~', isUser: false, timestamp: Date.now() }
]);
const prompts = ref([
  '分析基础系统日志趋势',
  '生成应用服务日志报告',
  '检查安全审计日志异常',
  '优化性能监控日志配置'
]);
const historyRecords = ref([]);

const activeNav = ref('log-assistant');

const chatHistoryRef = ref(null);

// 聊天历史滚动到顶部
const scrollToTop = () => {
  if (chatHistoryRef.value) {
    chatHistoryRef.value.scrollTop = 0;
  }
};

const sendMessage = async () => {
  if (!chatInput.value.trim()) return;

  const userMsg = { text: chatInput.value, isUser: true, timestamp: Date.now() };
  chatMessages.value.push(userMsg);
  historyRecords.value.push(userMsg);

  try {
    const params = {
      user_id: "nnm",
      assistant_id: "OLFdKirfJdaS",
      log_content: chatInput.value
    };
    console.log('发送日志分析请求：', params);

    const res = await generateLogReport(params);
    console.log('日志分析响应：', res.data);

    // 处理后端返回的格式 - 兼容不同的响应结构
    if (res.data.answer) {
      // 处理当前后端返回的格式：{"source":"yuanqi","answer":"..."}
      chatMessages.value.push({
        text: res.data.answer,
        isUser: false,
        timestamp: Date.now()
      });
    } else if (Array.isArray(res.data.messages) && res.data.messages.length > 0) {
      // 处理原来可能的格式（messages数组）
      res.data.messages.forEach(msg => {
        chatMessages.value.push({
          text: msg.content,
          isUser: msg.role === 'user',
          timestamp: msg.timestamp ? new Date(msg.timestamp).getTime() : Date.now()
        });
      });
    } else if (res.data.analysis) {
      // 处理原来可能的格式（analysis字段）
      chatMessages.value.push({
        text: res.data.analysis,
        isUser: false,
        timestamp: Date.now()
      });
    }

    // 获取日志列表并格式化时间显示
    const logsRes = await getLogs();
    logTableData.value = logsRes.data.map(log => ({
      ...log,
      time: format(new Date(log.timestamp), 'yyyy-MM-dd HH:mm:ss')
    }));
    await nextTick();
    scrollToTop();
  } catch (err) {
    console.error('发送请求异常:', err);
    ElMessage.error('操作失败：' + (err.response?.data?.detail || err.message));
  }

  chatInput.value = '';
};

const handlePrompt = (prompt) => {
  chatInput.value = prompt;
  sendMessage();
};

const formatTime = (timestamp) => format(new Date(timestamp), 'HH:mm:ss');

const getTagType = (level) => {
  const levelMap = {
    ERROR: 'danger',
    WARNING: 'warning',
    INFO: 'info',
    DEBUG: 'primary'
  };
  return levelMap[level] || 'info';
};

onMounted(async () => {
  try {
    const logsRes = await getLogs();
    logTableData.value = logsRes.data.map(log => ({
      ...log,
      time: format(new Date(log.timestamp), 'yyyy-MM-dd HH:mm:ss')
    }));
  } catch (err) {
    ElMessage.error('初始化加载日志失败：' + err.message);
  }
});
</script>


<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.logo {
  font-size: 18px;
  font-weight: bold;
  color: #1890ff;
}

.page-content {
  flex: 1;
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

.page-footer {
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 14px;
  color: #e62424ff;
  border-top: 1px solid #e8e8e8;
}

.page-content .log-assistant-core {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  margin: 20px 0;
}

.page-content .section-intro {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.page-content .section-intro h2 {
  margin: 0 0 10px 0;
  font-size: 20px;
  color: #333;
}

.page-content .section-intro p {
  margin: 0;
  color: #fb0303ff;
  font-size: 14px;
}

.page-content .main-layout {
  display: flex;
  gap: 20px;
  height: calc(100% - 60px);
}

.page-content .chat-column {
  width: 40%;
  display: flex;
  flex-direction: column;
  height: 600px;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  padding: 15px;
  box-sizing: border-box;
  overflow: hidden;
  
}

.chat-history-scroll {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column-reverse;
  /* 让新消息在底部，历史消息向上滚动 */
  margin-bottom: 10px;
}

.page-content .chat-message {
  display: flex;
  margin-bottom: 15px;
  animation: fadeIn 0.3s ease;
}

.page-content .user-message {
  flex-direction: row-reverse;
}

.page-content .chat-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

.page-content .user-message .chat-avatar {
  margin-left: 10px;
  margin-right: 0;
}

.page-content .chat-content {
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 8px;
  background: #f1f5f9;
  position: relative;
  color: #000; /* 字体变黑 */
}

.page-content .user-message .chat-content {
  background: #e6f7ff;
  color: #000; /* 字体变黑 */
}

.page-content .chat-text {
  margin: 0 0 5px 0;
  line-height: 1.5;
}

.page-content .chat-time {
  font-size: 12px;
  color: #888;
  text-align: right;
}

.page-content .chat-input-area {
  display: flex;
  gap: 10px;
  margin-top: auto;
}

.page-content .result-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-content .prompt-section,
.page-content .history-section {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
}

.page-content .section-title {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.page-content .prompt-section {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.page-content .history-section {
  max-height: 200px;
  overflow-y: auto;
}

.page-content .history-item {
  padding: 8px 0;
  border-bottom: 1px dashed #e0e0e0;
}

.page-content .history-text {
  font-size: 14px;
  margin-bottom: 3px;
}

.page-content .history-time {
  font-size: 12px;
  color: #999;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
  border-bottom: 1px dashed #e0e0e0;
}

.page-content .history-text {
  font-size: 14px;
  margin-bottom: 3px;
}

.page-content .history-time {
  font-size: 12px;
  color: #999;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
