// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    // 懒加载：只有访问登录页时才加载这个组件
    component: () => import('../views/login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/',
    name: 'Home',
    // 为了不大幅改动现在的代码，我们把核心功能暂时当作首页
    // 后面重构时，我们会把它抽成单独的组件
    component: () => import('../Home.vue')
  },
  {
    path: '/blog',
    name: 'Blog',
    component: () => import('../views/Blog.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫 (保安)
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 白名单：不需要登录就能访问的页面
  const whiteList = ['Login', 'Blog', 'Register']

  // 如果想去的地方不在白名单里，而且用户没登录
  if (!whiteList.includes(to.name) && !authStore.isAuthenticated) {
    next({ name: 'Login' }) // 踢去登录页
  } 
  // 如果想去登录页，但用户已经登录了
  else if (to.name === 'Login' && authStore.isAuthenticated) {
    next({ name: 'Home' }) // 踢回首页
  } 
  else {
    next() // 放行
  }
})

export default router