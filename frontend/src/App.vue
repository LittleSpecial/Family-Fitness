<template>
  <div id="app">
    <!-- 顶部用户信息栏 -->
    <div v-if="user && $route.path !== '/login'" class="user-header">
      <div class="user-info">
        <span class="user-name">👤 {{ user.name }}</span>
        <span class="user-score">🏆 {{ user.total_score }} 积分</span>
      </div>
      <button @click="logout" class="logout-btn">登出</button>
    </div>

    <router-view />
    
    <!-- 底部导航（仅在登录后显示） -->
    <nav v-if="user && $route.path !== '/login'" class="nav">
      <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
        📋<br>今日任务
      </router-link>
      <router-link to="/upload" class="nav-item" :class="{ active: $route.path === '/upload' }">
        🏃<br>运动上传
      </router-link>
      <router-link to="/diet" class="nav-item" :class="{ active: $route.path === '/diet' }">
        🍎<br>饮食记录
      </router-link>
      <router-link to="/trends" class="nav-item" :class="{ active: $route.path === '/trends' }">
        📊<br>健康趋势
      </router-link>
    </nav>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const user = ref(null)

// 加载用户信息
const loadUser = () => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    user.value = JSON.parse(userStr)
  } else {
    user.value = null
  }
}

onMounted(() => {
  loadUser()
})

// 监听路由变化，重新加载用户信息
watch(() => route.path, () => {
  loadUser()
})

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  user.value = null
  router.push('/login')
}
</script>

<style scoped>
#app {
  padding-bottom: 80px;
}

.user-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.user-name {
  font-size: 16px;
  font-weight: bold;
}

.user-score {
  font-size: 14px;
  opacity: 0.9;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.4);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
