<template>
  <div id="app">
    <router-view />
    <nav class="nav">
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
// 无额外逻辑
</script>

<style scoped>
#app {
  padding-bottom: 80px;
}
</style>
