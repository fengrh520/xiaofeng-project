<template>
  <div class="app-container">
    <div class="header">
      <h1>🚀 AI 提示词优化实验室</h1>
      <p class="subtitle">让你的 Prompt 更有生产力</p>
      <div style="margin-top: 10px;">
        <el-button type="primary" link @click="$router.push('/blog')">📖 阅读项目开发实战复盘</el-button>
      </div>
    </div>
    
    <div class="main-content">
      <!-- 左侧：输入与操作区 -->
      <el-card class="operation-card">
        <template #header>
          <div class="card-header">
            <span>✨ 优化工作台</span>
          </div>
        </template>
        
        <el-input
          v-model="inputPrompt"
          :rows="6"
          type="textarea"
          placeholder="请输入你想优化的原始提示词... (例如：帮我写个周报)"
          resize="none"
        />
        
        <div class="btn-area">
          <el-button 
            type="primary" 
            size="large" 
            @click="optimizePrompt" 
            :loading="isLoading"
            round
          >
            {{ isLoading ? 'AI 正在思考中...' : '立即优化 ⚡' }}
          </el-button>
        </div>

        <!-- 优化结果展示 -->
        <transition name="el-fade-in">
          <div v-if="optimizedResult" class="result-box">
            <div class="result-header">
              <h3>🎉 优化结果：</h3>
              <el-button size="small" @click="copyResult" icon="CopyDocument" circle />
            </div>
            <div class="result-content">
              {{ optimizedResult }}
            </div>
          </div>
        </transition>
      </el-card>

      <!-- 右侧：历史记录区 -->
      <el-card class="history-card">
        <template #header>
          <div class="card-header">
            <span>📜 历史记录</span>
            <el-button link @click="fetchHistory">刷新</el-button>
          </div>
          <!-- 搜索和筛选栏 -->
          <div class="filter-bar">
            <div class="search-group">
              <el-input 
                v-model="searchQuery" 
                placeholder="搜索..." 
                clearable
                size="small"
                class="search-input"
                @clear="fetchHistory"
                @keyup.enter="fetchHistory"
              />
              <el-button size="small" :icon="Search" @click="fetchHistory" />
            </div>
            <el-radio-group v-model="filterType" size="small">
              <el-radio-button label="all">全部</el-radio-button>
              <el-radio-button label="starred">
                <el-icon><StarFilled /></el-icon>
              </el-radio-button>
            </el-radio-group>
          </div>
        </template>
        
        <el-scrollbar height="500px">
          <div v-if="historyList.length === 0" class="empty-history">
            暂无记录
          </div>
          <div 
            v-for="item in historyList" 
            :key="item.id" 
            class="history-item"
            :class="{ 'pinned-item': item.is_pinned }"
            @click="loadHistory(item)"
          >
            <div class="item-header">
              <span class="history-title">{{ item.title || item.original_prompt.substring(0, 10) }}...</span>
              <div class="item-actions">
                <!-- 置顶按钮 -->
                <el-button 
                  link 
                  size="small" 
                  @click.stop="togglePin(item)"
                  :type="item.is_pinned ? 'warning' : 'info'"
                >
                  <el-icon><Top /></el-icon>
                </el-button>
                <!-- 星标按钮 -->
                <el-button 
                  link 
                  size="small" 
                  @click.stop="toggleStar(item)"
                  :type="item.is_starred ? 'warning' : 'info'"
                >
                  <el-icon v-if="item.is_starred"><StarFilled /></el-icon>
                  <el-icon v-else><Star /></el-icon>
                </el-button>
                <!-- 删除按钮 -->
                 <el-button 
                  link 
                  size="small" 
                  type="danger"
                  @click.stop="deletePrompt(item)"
                >
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>
            <div class="history-time">{{ new Date(item.created_at).toLocaleString() }}</div>
          </div>
        </el-scrollbar>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { CopyDocument, Search, Star, StarFilled, Top, Delete } from '@element-plus/icons-vue' 
import axios from 'axios'

import { useAuthStore } from './stores/auth' // 引入 store

const inputPrompt = ref('')
const optimizedResult = ref('')
const isLoading = ref(false)
const historyList = ref([])

// 搜索和筛选状态
const searchQuery = ref('')
const filterType = ref('all') // 'all' or 'starred'

// 优化函数
const optimizePrompt = async () => {
  if (!inputPrompt.value) {
    ElMessage.warning('请先输入内容！')
    return
  }

  isLoading.value = true
  const authStore = useAuthStore() // 获取 store

  try {
    const response = await axios.post('/api/prompts/', {
      original_prompt: inputPrompt.value,
      // 可以在这里传更多参数，比如场景选择
    }, {
      headers: { Authorization: `Bearer ${authStore.accessToken}` } // 显式传递 Token
    })

    optimizedResult.value = response.data.optimized_prompt
    ElMessage.success('优化成功！')
    fetchHistory() // 成功后刷新历史记录
  } catch (error) {
    console.error(error)
    ElMessage.error('服务繁忙，请稍后再试: ' + (error.response?.data?.detail || error.message))
  } finally {
    isLoading.value = false
  }
}

// 复制结果
const copyResult = async () => {
  try {
    await navigator.clipboard.writeText(optimizedResult.value)
    ElMessage.success('已复制到剪贴板')
  } catch (err) {
    ElMessage.error('复制失败')
  }
}

// 获取历史记录
const fetchHistory = async () => {
  const authStore = useAuthStore() // 获取 store
  try {
    const params = {}
    if (searchQuery.value) params.search = searchQuery.value
    if (filterType.value === 'starred') params.is_starred = true

    // console.log('正在请求历史记录，参数:', params) // 调试日志

    const res = await axios.get('/api/prompts/', { 
      params,
      headers: { Authorization: `Bearer ${authStore.accessToken}` } // 显式传递 Token，防止拦截器失效
    })
    historyList.value = res.data
    // console.log('获取到的数据:', res.data) // 调试日志
    
  } catch (error) {
    console.error('获取历史记录失败', error)
    // 显式显示错误，方便排查
    ElMessage.error('无法加载历史记录: ' + (error.response?.status === 401 ? '登录已过期' : error.message))
  }
}

// 切换星标
const toggleStar = async (item) => {
  const authStore = useAuthStore()
  try {
    const newVal = !item.is_starred
    await axios.patch(`/api/prompts/${item.id}/`, {
      is_starred: newVal
    }, {
      headers: { Authorization: `Bearer ${authStore.accessToken}` }
    })
    item.is_starred = newVal
    // 如果在星标筛选下取消了星标，可能需要刷新列表，或者前端直接移除
    if (filterType.value === 'starred' && !newVal) {
      fetchHistory()
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 切换置顶
const togglePin = async (item) => {
  const authStore = useAuthStore()
  try {
    const newVal = !item.is_pinned
    await axios.patch(`/api/prompts/${item.id}/`, {
      is_pinned: newVal
    }, {
      headers: { Authorization: `Bearer ${authStore.accessToken}` }
    })
    item.is_pinned = newVal
    fetchHistory() // 置顶会影响排序，需要重新获取列表
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 删除记录
const deletePrompt = async (item) => {
  const authStore = useAuthStore()
  try {
    await ElMessageBox.confirm('确定要删除这条记录吗？', '提示', {
      type: 'warning'
    })
    
    await axios.delete(`/api/prompts/${item.id}/`, {
      headers: { Authorization: `Bearer ${authStore.accessToken}` }
    })
    ElMessage.success('删除成功')
    fetchHistory()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 监听搜索和筛选变化
// 使用 debounce 防抖，避免用户输入过程中频繁请求
let timeout
watch([searchQuery, filterType], () => {
  clearTimeout(timeout)
  timeout = setTimeout(() => {
    fetchHistory()
  }, 300)
})

// 点击历史记录回填
const loadHistory = (item) => {
  inputPrompt.value = item.original_prompt
  optimizedResult.value = item.optimized_prompt
}

// 页面加载时自动获取历史
onMounted(() => {
  fetchHistory()
})
</script>

<style scoped>
.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h1 {
  color: #409EFF;
  margin: 0;
  font-size: 2.5rem;
}

.subtitle {
  color: #909399;
  margin-top: 10px;
}

.main-content {
  display: grid;
  grid-template-columns: 2fr 1fr; /* 左边占2份，右边占1份 */
  gap: 20px;
}

.card-header {
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 新增：筛选栏样式 */
.filter-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.search-group {
  display: flex;
  flex: 1;
  gap: 5px;
}

.search-input {
  flex: 1;
}

/* 历史记录项样式 */
.history-item {
  padding: 12px;
  border-bottom: 1px solid #ebeef5;
  cursor: pointer;
  transition: all 0.3s;
  color: #333; /* 确保文字颜色可见 */
  background-color: #fff; /* 确保背景色为白色，防止透明导致的看不清 */
  min-height: 60px; /* 确保每项有高度 */
  display: flex;
  flex-direction: column;
}

.history-item:hover {
  background-color: #f5f7fa;
}

.pinned-item {
  background-color: #fff8e1; /* 置顶项背景色 */
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 5px;
}

.history-title {
  font-weight: 500;
  color: #303133;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-right: 10px;
}

.item-actions {
  display: flex;
  gap: 2px;
}

.history-time {
  font-size: 0.8rem;
  color: #909399;
}

.empty-history {
  text-align: center;
  color: #909399;
  padding: 20px;
}

.btn-area {
  margin-top: 20px;
  text-align: right;
}

.result-box {
  margin-top: 30px;
  padding: 20px;
  background-color: #f0f9eb;
  border-radius: 8px;
  border: 1px solid #e1f3d8;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.result-header h3 {
  margin: 0;
  color: #67c23a;
}

.result-content {
  white-space: pre-wrap; /* 保持换行格式 */
  line-height: 1.6;
  color: #606266;
}
</style>