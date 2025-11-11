<template>
  <div class="task-today-page">
    <div class="header">
      <h1>今日任务</h1>
      <p class="date">{{ currentDate }}</p>
    </div>

    <div class="container">
      <!-- 健康得分卡片 -->
      <div class="card scores-container">
        <h3>今日健康总分</h3>
        <div class="total-score">
          <div class="score-circle score-high">{{ totalScore }}</div>
        </div>
        <div class="score-breakdown">
          <div class="score-item">
            <span class="score-label">运动</span>
            <span class="score-value">{{ exerciseScore }}</span>
          </div>
          <div class="score-item">
            <span class="score-label">饮食</span>
            <span class="score-value">{{ dietScore }}</span>
          </div>
          <div class="score-item">
            <span class="score-label">任务</span>
            <span class="score-value">{{ taskPoints }}</span>
          </div>
        </div>
      </div>

      <!-- 任务列表 -->
      <div class="tasks-section">
        <h3>今日任务 ({{ completedCount }}/{{ totalCount }})</h3>
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="tasks.length === 0" class="empty">暂无任务</div>
        <TaskCard
          v-for="task in tasks"
          :key="task.id"
          :task="task"
          @complete="handleTaskComplete"
        />
      </div>

      <!-- 昨日对比 -->
      <div class="card comparison" v-if="yesterdayScore > 0">
        <p class="comparison-text">
          {{ comparisonText }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import TaskCard from '../components/TaskCard.vue'
import api from '../api'

const userId = 1 // 默认用户ID
const loading = ref(false)
const tasks = ref([])
const taskPoints = ref(0)
const exerciseScore = ref(0)
const dietScore = ref(0)
const yesterdayScore = ref(0)

const currentDate = computed(() => {
  const date = new Date()
  const weekDays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  return `${date.getMonth() + 1}月${date.getDate()}日 ${weekDays[date.getDay()]}`
})

const totalCount = computed(() => tasks.value.length)
const completedCount = computed(() => tasks.value.filter(t => t.done).length)

const totalScore = computed(() => {
  // 综合得分计算
  let score = 0
  let weight = 0
  
  if (exerciseScore.value > 0) {
    score += exerciseScore.value * 0.4
    weight += 0.4
  }
  if (dietScore.value > 0) {
    score += dietScore.value * 0.4
    weight += 0.4
  }
  if (taskPoints.value > 0) {
    score += Math.min(taskPoints.value, 100) * 0.2
    weight += 0.2
  }
  
  return weight > 0 ? Math.round(score / weight) : 0
})

const comparisonText = computed(() => {
  const diff = totalScore.value - yesterdayScore.value
  if (diff > 10) return '🎉 太棒了! 今天比昨天进步很多!'
  if (diff > 0) return '👍 不错! 继续保持!'
  if (diff === 0) return '💪 保持稳定,继续加油!'
  return '😊 别气馁,明天会更好!'
})

const loadTasks = async () => {
  loading.value = true
  try {
    const res = await api.getTodayTasks(userId)
    if (res.success) {
      tasks.value = res.data.tasks
      taskPoints.value = res.data.total_points
    }
  } catch (error) {
    console.error('加载任务失败:', error)
  } finally {
    loading.value = false
  }
}

const handleTaskComplete = async (taskId) => {
  try {
    const res = await api.markTaskDone(taskId, userId)
    if (res.success) {
      // 更新任务状态
      const task = tasks.value.find(t => t.id === taskId)
      if (task) {
        task.done = true
      }
      taskPoints.value = res.data.total_points_today
    }
  } catch (error) {
    console.error('完成任务失败:', error)
  }
}

onMounted(() => {
  loadTasks()
})
</script>

<style scoped>
.task-today-page {
  padding-bottom: 24px;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 24px 16px;
  text-align: center;
}

.header h1 {
  margin-bottom: 8px;
}

.date {
  opacity: 0.9;
}

.scores-container {
  text-align: center;
}

.total-score {
  margin: 20px 0;
}

.score-breakdown {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.score-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.score-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 8px;
}

.score-value {
  font-size: 20px;
  font-weight: bold;
  color: #1890ff;
}

.tasks-section {
  margin-top: 24px;
}

.tasks-section h3 {
  margin-bottom: 16px;
  padding: 0 16px;
}

.loading, .empty {
  text-align: center;
  padding: 40px;
  color: #999;
}

.comparison {
  margin-top: 24px;
  text-align: center;
}

.comparison-text {
  font-size: 16px;
  color: #666;
}
</style>
