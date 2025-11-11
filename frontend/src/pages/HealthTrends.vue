<template>
  <div class="health-trends-page">
    <div class="header">
      <h1>健康趋势</h1>
    </div>

    <div class="container">
      <!-- 时间范围选择 -->
      <div class="card">
        <div class="range-selector">
          <button
            class="range-btn"
            :class="{ active: days === 7 }"
            @click="changeDays(7)"
          >
            近 7 天
          </button>
          <button
            class="range-btn"
            :class="{ active: days === 30 }"
            @click="changeDays(30)"
          >
            近 30 天
          </button>
        </div>
      </div>

      <div v-if="loading" class="loading">加载中...</div>

      <template v-else-if="trends">
        <!-- 每日总分趋势 -->
        <div class="card">
          <h3>📊 每日健康总分</h3>
          <TrendChart
            type="line"
            :labels="dateLabels"
            :data="scoreData"
            label="健康总分"
            color="#1890ff"
          />
        </div>

        <!-- 运动卡路里趋势 -->
        <div class="card">
          <h3>🔥 运动消耗卡路里</h3>
          <TrendChart
            type="bar"
            :labels="dateLabels"
            :data="trends.exercise_trends.calories"
            label="卡路里"
            color="#ff9800"
          />
        </div>

        <!-- 运动时长趋势 -->
        <div class="card">
          <h3>⏱️ 运动时长</h3>
          <TrendChart
            type="line"
            :labels="dateLabels"
            :data="trends.exercise_trends.duration"
            label="时长(分钟)"
            color="#52c41a"
          />
        </div>

        <!-- 饮食健康得分 -->
        <div class="card">
          <h3>🍎 饮食健康得分</h3>
          <TrendChart
            type="line"
            :labels="dateLabels"
            :data="trends.diet_trends.avg_health_scores"
            label="健康得分"
            color="#eb2f96"
          />
        </div>

        <!-- 任务完成率 -->
        <div class="card">
          <h3>✅ 任务完成率</h3>
          <TrendChart
            type="line"
            :labels="dateLabels"
            :data="taskRateData"
            label="完成率(%)"
            color="#722ed1"
          />
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import TrendChart from '../components/TrendChart.vue'
import api from '../api'

const userId = 1
const days = ref(7)
const loading = ref(false)
const trends = ref(null)

const dateLabels = computed(() => {
  if (!trends.value) return []
  return trends.value.daily_scores.map(item => {
    const date = new Date(item.date)
    return `${date.getMonth() + 1}/${date.getDate()}`
  })
})

const scoreData = computed(() => {
  if (!trends.value) return []
  return trends.value.daily_scores.map(item => item.score)
})

const taskRateData = computed(() => {
  if (!trends.value) return []
  return trends.value.task_completion_rate.map(item => item.rate)
})

const loadTrends = async () => {
  loading.value = true
  try {
    const res = await api.getTrends(userId, days.value)
    if (res.success) {
      trends.value = res.data
    }
  } catch (error) {
    console.error('加载趋势数据失败:', error)
  } finally {
    loading.value = false
  }
}

const changeDays = (newDays) => {
  days.value = newDays
  loadTrends()
}

onMounted(() => {
  loadTrends()
})
</script>

<style scoped>
.health-trends-page {
  padding-bottom: 24px;
}

.header {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: #fff;
  padding: 24px 16px;
  text-align: center;
}

.range-selector {
  display: flex;
  gap: 12px;
}

.range-btn {
  flex: 1;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 16px;
}

.range-btn:hover {
  border-color: #1890ff;
}

.range-btn.active {
  border-color: #1890ff;
  background: #1890ff;
  color: #fff;
  font-weight: bold;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #999;
}

.card h3 {
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
