import { createRouter, createWebHistory } from 'vue-router';
import MainLayout from '../views/MainLayout.vue'; // 主布局（包含导航栏）
import LogManager from '../views/LogManager.vue';
import LogDetail from '../views/LogDetail.vue';
import LogAssistant from '../views/LogAssistant.vue';

const routes = [
  {
    path: '/',
    component: MainLayout, // 所有页面都基于主布局显示（包含导航栏）
    children: [
      // 默认显示对话框页面
      { path: '', redirect: '/log-assistant' },
      
      // 日志管理页面
      {
        path: 'logs',
        name: 'LogManager',
        component: LogManager,
        meta: { title: '日志管理系统' }
      },
      
      // 日志详情页面
      {
        path: 'logs/detail',
        name: 'LogDetail',
        component: LogDetail,
        meta: { title: '日志详情' }
      },
      
      // 对话框页面（默认显示）
      {
        path: 'log-assistant',
        name: 'LogAssistant',
        component: LogAssistant,
        meta: { title: '问题解答' }
      },
      
      // 首页/仪表盘
      {
        path: 'home',
        name: 'Home',
        component: LogManager, // 暂时使用LogManager作为首页
        meta: { title: '首页' }
      },
      
      // 轮巡数据页面
      {
        path: 'data',
        name: 'Data',
        component: LogManager, // 暂时使用LogManager作为轮巡数据页面
        meta: { title: '轮巡数据' }
      },
      
      // 应用告警页面
      {
        path: 'alerts',
        name: 'Alerts',
        component: LogManager, // 暂时使用LogManager作为应用告警页面
        meta: { title: '应用告警' }
      },
      
      // 系统设置页面
      {
        path: 'settings',
        name: 'Settings',
        component: LogManager, // 暂时使用LogManager作为系统设置页面
        meta: { title: '系统设置' }
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// 全局路由守卫：修改页面标题
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title;
  }
  next();
});

export default router;
    