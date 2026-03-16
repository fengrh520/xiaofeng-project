<!-- frontend/src/App.vue (根容器) -->
<template>
  <router-view></router-view>
</template>

<script setup>
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
// 立即初始化，确保子组件 (Home.vue) 挂载时 Token 已就绪
authStore.initialize()
</script>