import { createApp } from 'vue'
import { createPinia } from 'pinia' // 引入 Pinia
import './style.css'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue' // 引入所有图标
import router from './router' 
const app = createApp(App)
const pinia = createPinia() // 创建 Pinia 实例

app.use(pinia) // 挂载 Pinia
app.use(router) 
app.use(ElementPlus)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.mount('#app')