import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import TaskToday from '../pages/TaskToday.vue'
import ExerciseUpload from '../pages/ExerciseUpload.vue'
import DietRecord from '../pages/DietRecord.vue'
import HealthTrends from '../pages/HealthTrends.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/',
    name: 'TaskToday',
    component: TaskToday,
    meta: { title: '今日任务', requiresAuth: true }
  },
  {
    path: '/upload',
    name: 'ExerciseUpload',
    component: ExerciseUpload,
    meta: { title: '运动上传', requiresAuth: true }
  },
  {
    path: '/diet',
    name: 'DietRecord',
    component: DietRecord,
    meta: { title: '饮食记录', requiresAuth: true }
  },
  {
    path: '/trends',
    name: 'HealthTrends',
    component: HealthTrends,
    meta: { title: '健康趋势', requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：检查登录状态
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    // 需要登录但未登录，跳转到登录页
    next('/login')
  } else if (to.path === '/login' && token) {
    // 已登录但访问登录页，跳转到首页
    next('/')
  } else {
    next()
  }
})

router.afterEach((to) => {
  document.title = to.meta.title || 'FamilyFit 健康助手'
})

export default router
