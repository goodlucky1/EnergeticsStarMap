import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'

// 创建Vue应用实例
const app = createApp(App)

// 使用router
app.use(router)

// 使用ElementPlus
app.use(ElementPlus)

// 将axios挂载到全局
app.config.globalProperties.$axios = axios

// 挂载应用
app.mount('#app')