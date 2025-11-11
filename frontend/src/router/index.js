import { createRouter, createWebHistory } from 'vue-router'
import TaskToday from '../pages/TaskToday.vue'
import ExerciseUpload from '../pages/ExerciseUpload.vue'
import DietRecord from '../pages/DietRecord.vue'
import HealthTrends from '../pages/HealthTrends.vue'

const routes = [
  {
    path: '/',
    name: 'TaskToday',
    component: TaskToday,
    meta: { title: '今日任务' }
  },
  {
    path: '/upload',
    name: 'ExerciseUpload',
    component: ExerciseUpload,
    meta: { title: '运动上传' }
  },
  {
    path: '/diet',
    name: 'DietRecord',
    component: DietRecord,
    meta: { title: '饮食记录' }
  },
  {
    path: '/trends',
    name: 'HealthTrends',
    component: HealthTrends,
    meta: { title: '健康趋势' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.afterEach((to) => {
  document.title = to.meta.title || 'FamilyFit 健康助手'
})

export default router
