import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    const message = error.response?.data?.detail || error.message || '请求失败'
    console.error('API Error:', message)
    return Promise.reject(new Error(message))
  }
)

export default {
  // 运动相关
  parseExerciseReport(file, userId) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('user_id', userId)
    return api.post('/parse_report', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 任务相关
  getTodayTasks(userId) {
    return api.get('/tasks/today', { params: { user_id: userId } })
  },

  markTaskDone(taskId, userId) {
    return api.post('/tasks/done', { task_id: taskId, user_id: userId })
  },

  // 饮食相关
  addMealRecord(data) {
    return api.post('/meals/add', data)
  },

  getTodayMeals(userId) {
    return api.get('/meals/today', { params: { user_id: userId } })
  },

  // 趋势数据
  getTrends(userId, days = 7) {
    return api.get('/trends', { params: { user_id: userId, days } })
  }
}
