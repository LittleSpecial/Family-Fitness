import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 请求拦截器：添加 token
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器
api.interceptors.response.use(
  response => response,
  error => {
    // 未授权，跳转到登录页
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default {
  // 原始 axios 实例（用于登录注册）
  post: (url, data) => api.post(url, data),
  get: (url, config) => api.get(url, config),

  // 运动相关
  parseExerciseReport(file, userId) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('user_id', userId)
    return api.post('/parse_report', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }).then(res => res.data)
  },

  // 任务相关
  getTodayTasks(userId) {
    return api.get('/tasks/today', { params: { user_id: userId } }).then(res => res.data)
  },

  markTaskDone(taskId, userId) {
    return api.post('/tasks/done', { task_id: taskId, user_id: userId }).then(res => res.data)
  },

  // 饮食相关
  addMealRecord(data) {
    return api.post('/meals/add', data).then(res => res.data)
  },

  getTodayMeals(userId) {
    return api.get('/meals/today', { params: { user_id: userId } }).then(res => res.data)
  },

  // 趋势数据
  getTrends(userId, days = 7) {
    return api.get('/trends', { params: { user_id: userId, days } }).then(res => res.data)
  }
}
