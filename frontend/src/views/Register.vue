<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2>🚀 创建新账号</h2>
      <el-form :model="form" label-width="0">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名" prefix-icon="User" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.confirmPassword" type="password" placeholder="确认密码" prefix-icon="Check" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="login-btn" @click="handleRegister" :loading="loading">立即注册</el-button>
        </el-form-item>
        <div class="blog-link">
          <router-link to="/login">已有账号？去登录</router-link>
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

const form = ref({ username: '', password: '', confirmPassword: '' })
const loading = ref(false)
const authStore = useAuthStore()
const router = useRouter()

const handleRegister = async () => {
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请输入完整信息')
    return
  }
  
  if (form.value.password !== form.value.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  
  loading.value = true
  try {
    await authStore.register(form.value.username, form.value.password)
    ElMessage.success('注册成功！请登录')
    router.push('/login')
  } catch (error) {
    ElMessage.error('注册失败: ' + (error.response?.data?.username?.[0] || '用户名可能已存在'))
  } finally {
    loading.value = false
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