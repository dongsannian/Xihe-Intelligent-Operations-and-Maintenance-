import axios from 'axios';

// 配置后端基础地址（开发环境）
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',  // 后端服务地址（与FastAPI保持一致）
  timeout: 120000,  // 超时时间2分钟（单位毫秒）
  headers: {
    'Content-Type': 'application/json'  // 默认请求头
  }
});

// 1. 获取日志列表（支持分页和筛选）
export const getLogs = (params) => {
  return api.get('/api/logs', { params });
};

// 2. 新增日志
export const addLog = (logData) => {
  return api.post('/api/logs', logData);
};

// 3. 获取单条日志详情
export const getLogDetail = (id) => {
  return api.get(`/api/logs/${id}`);
};

// 4. 删除日志（修正：只保留一个定义）
export const deleteLog = (id) => {
  return api.delete(`/api/logs/${id}`);
};

// 5. 标记日志为已处理（需后端对应接口支持）
export const markAsHandled = (id) => {
  return api.put(`/api/logs/${id}/mark-as-handled`);
};

// 6. 生成日志分析报告（对接AI分析接口）
export const generateLogReport = (data) => {
  // 调试用：打印请求参数
  console.log('generateLogReport 请求参数:', data);
  // 修改为正确的后端接口路径
  return api.post('/api/ask', { question: data.log_content }).then(res => {
    // 调试用：打印AI接口返回内容
    console.log('generateLogReport 返回结果:', res.data);
    return res;
  });
};

export default api;