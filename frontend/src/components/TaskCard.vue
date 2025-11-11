<template>
  <div class="task-card" :class="{ done: task.done }" @click="handleClick">
    <div class="task-icon">{{ taskIcon }}</div>
    <div class="task-content">
      <div class="task-name">{{ task.task_name }}</div>
      <div class="task-points">+{{ task.reward_points }} 积分</div>
    </div>
    <div class="task-check">
      <span v-if="task.done" class="check-icon">✓</span>
      <span v-else class="check-box"></span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  task: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['complete'])

const taskIcon = computed(() => {
  const icons = {
    water: '💧',
    stretch: '🧘',
    walk: '🚶',
    diet: '🥗',
    no_sugar: '🚫',
    sleep: '😴',
    exercise: '🏃'
  }
  return icons[props.task.task_type] || '📌'
})

const handleClick = () => {
  if (!props.task.done) {
    emit('complete', props.task.id)
  }
}
</script>

<style scoped>
.task-card {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #fff;
  border-radius: 12px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.3s;
}

.task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.task-card.done {
  background: #f6ffed;
  border: 1px solid #b7eb8f;
}

.task-icon {
  font-size: 32px;
  margin-right: 16px;
}

.task-content {
  flex: 1;
}

.task-name {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 4px;
}

.task-points {
  font-size: 12px;
  color: #ff9800;
}

.task-check {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.check-icon {
  font-size: 24px;
  color: #52c41a;
}

.check-box {
  width: 24px;
  height: 24px;
  border: 2px solid #d9d9d9;
  border-radius: 50%;
  display: block;
}
</style>
