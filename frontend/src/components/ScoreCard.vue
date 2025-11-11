<template>
  <div class="score-card">
    <div class="score-item">
      <div class="score-label">{{ label }}</div>
      <div 
        class="score-circle"
        :class="scoreClass"
      >
        {{ score }}
      </div>
      <div class="score-text">{{ description }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: String,
  score: {
    type: Number,
    default: 0
  },
  description: String
})

const scoreClass = computed(() => {
  if (props.score >= 80) return 'score-high'
  if (props.score >= 60) return 'score-medium'
  return 'score-low'
})
</script>

<style scoped>
.score-card {
  text-align: center;
}

.score-item {
  padding: 16px;
}

.score-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
}

.score-text {
  font-size: 12px;
  color: #999;
  margin-top: 12px;
}
</style>
