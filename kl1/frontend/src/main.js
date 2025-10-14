import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import router from './router';  // 引入路由配置
import ElementPlus from 'element-plus';  // 引入 Element Plus
import 'element-plus/dist/index.css';  // 引入 Element Plus 样式

const app = createApp(App);
app.use(router);  // 使用路由
app.use(ElementPlus);  // 使用 Element Plus 组件库
app.mount('#app');  // 挂载到页面 #app 元素