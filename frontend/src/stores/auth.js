// frontend/src/stores/auth.js
import { defineStore } from 'pinia'
import axios from 'axios'
import { jwtDecode } from 'jwt-decode'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    user: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.accessToken
  },

  actions: {
    async initialize() {
      if (this.accessToken) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`
        try {
          const decoded = jwtDecode(this.accessToken)
          this.user = { id: decoded.user_id }
        } catch (e) {
          this.logout()
        }
      }
    },

    async login(username, password) {
      try {
        const response = await axios.post('/api/token/', {
          username,
          password
        })
        
        const { access, refresh } = response.data
        this.setToken(access, refresh)
        return true
      } catch (error) {
        console.error('登录失败', error)
        return false
      }
    },

    async register(username, password) {
      try {
        await axios.post('/api/register/', {
          username,
          password
        })
        return true
      } catch (error) {
        // 将具体的错误信息抛出，以便在 Register.vue 中捕获并显示
        console.error('注册接口返回错误:', error.response?.data)
        throw error
      }
    },

    setToken(access, refresh) {
      this.accessToken = access
      this.refreshToken = refresh
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      
      // 解析 Token 获取用户信息 (比如用户名)
      const decoded = jwtDecode(access)
      this.user = { id: decoded.user_id }
      
      // 设置 Axios 默认请求头，以后所有请求都会自动带上 Token
      axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
    },

    logout() {
      this.accessToken = null
      this.refreshToken = null
      this.user = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      delete axios.defaults.headers.common['Authorization']
    }
  }
})