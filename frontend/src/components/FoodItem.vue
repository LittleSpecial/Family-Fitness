<template>
  <div class="food-item">
    <div class="food-info">
      <span class="food-name">{{ food.name }}</span>
      <span class="food-amount">{{ food.amount }}</span>
    </div>
    <button class="remove-btn" @click="handleRemove">✕</button>
  </div>
</template>

<script setup>
const props = defineProps({
  food: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['remove'])

const handleRemove = () => {
  emit('remove')
}
</script>

<style scoped>
.food-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background: #f5f5f5;
  border-radius: 8px;
  margin-bottom: 8px;
}

.food-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.food-name {
  font-size: 16px;
  font-weight: 500;
}

.food-amount {
  font-size: 14px;
  color: #666;
}

.remove-btn {
  width: 24px;
  height: 24px;
  border: none;
  background: #ff4d4f;
  color: #fff;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.remove-btn:hover {
  background: #ff7875;
  transform: scale(1.1);
}
</style>
