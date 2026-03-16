<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2>👋 欢迎回来</h2>
      <el-form :model="form" label-width="0">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名" prefix-icon="User" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="login-btn" @click="handleLogin" :loading="loading">登录</el-button>
        </el-form-item>
        <div class="blog-link">
          <router-link to="/blog">随便看看 (访问博客)</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const form = ref({ username: '', password: '' })
const loading = ref(false)
const authStore = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请输入账号密码')
    return
  }
  
  loading.value = true
  const success = await authStore.login(form.value.username, form.value.password)
  loading.value = false
  
  if (success) {
    ElMessage.success('登录成功！')
    router.push('/') // 跳转到首页
  } else {
    ElMessage.error('账号或密码错误')
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}
.login-card {
  width: 400px;
  padding: 20px;
}
.login-btn {
  width: 100%;
}
.blog-link {
  text-align: center;
  margin-top: 15px;
}
.blog-link a {
  color: #409eff;
  text-decoration: none;
  font-size: 14px;
}
.blog-link a:hover {
  text-decoration: underline;
}
</style>