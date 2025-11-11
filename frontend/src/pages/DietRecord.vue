<template>
  <div class="diet-record-page">
    <div class="header">
      <h1>饮食记录</h1>
    </div>

    <div class="container">
      <!-- 餐次选择 -->
      <div class="card">
        <h3>选择餐次</h3>
        <div class="meal-types">
          <button
            v-for="type in mealTypes"
            :key="type.value"
            class="meal-btn"
            :class="{ active: mealType === type.value }"
            @click="mealType = type.value"
          >
            {{ type.icon }} {{ type.label }}
          </button>
        </div>
      </div>

      <!-- 食物输入 -->
      <div class="card">
        <h3>添加食物</h3>
        <div class="input-group">
          <input
            v-model="foodName"
            class="input"
            placeholder="食物名称"
            @keyup.enter="addFood"
          />
        </div>
        <div class="input-group">
          <input
            v-model="foodAmount"
            class="input"
            placeholder="份量 (如: 1碗、100g)"
            @keyup.enter="addFood"
          />
        </div>
        <button class="btn btn-primary" @click="addFood" style="width: 100%">
          ➕ 添加
        </button>
      </div>

      <!-- 食物列表 -->
      <div class="card" v-if="foodItems.length > 0">
        <h3>已添加食物</h3>
        <FoodItem
          v-for="(food, index) in foodItems"
          :key="index"
          :food="food"
          @remove="removeFood(index)"
        />
        <button
          class="btn btn-primary"
          @click="submitAnalysis"
          :disabled="analyzing"
          style="width: 100%; margin-top: 16px"
        >
          {{ analyzing ? '分析中...' : '🔍 分析健康度' }}
        </button>
      </div>

      <!-- 分析结果 -->
      <div class="card" v-if="analysis">
        <h3>分析结果</h3>
        <div class="analysis-score">
          <div class="score-circle score-high">{{ analysis.health_score }}</div>
          <p>健康得分</p>
        </div>
        <div class="analysis-details">
          <div class="detail-item">
            <span class="label">总卡路里</span>
            <span class="value">{{ analysis.total_calories }} 千卡</span>
          </div>
          <div class="detail-item">
            <span class="label">健康建议</span>
            <span class="value analysis-text">{{ analysis.analysis }}</span>
          </div>
        </div>
        <button class="btn btn-primary" @click="resetForm" style="width: 100%">
          继续记录
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import FoodItem from '../components/FoodItem.vue'
import api from '../api'

const userId = 1
const mealType = ref('lunch')
const foodName = ref('')
const foodAmount = ref('')
const foodItems = ref([])
const analyzing = ref(false)
const analysis = ref(null)

const mealTypes = [
  { value: 'breakfast', label: '早餐', icon: '🌅' },
  { value: 'lunch', label: '午餐', icon: '🌞' },
  { value: 'dinner', label: '晚餐', icon: '🌙' },
  { value: 'snack', label: '加餐', icon: '🍎' }
]

const addFood = () => {
  if (!foodName.value.trim() || !foodAmount.value.trim()) {
    return
  }

  foodItems.value.push({
    name: foodName.value.trim(),
    amount: foodAmount.value.trim()
  })

  foodName.value = ''
  foodAmount.value = ''
}

const removeFood = (index) => {
  foodItems.value.splice(index, 1)
}

const submitAnalysis = async () => {
  analyzing.value = true
  try {
    const today = new Date().toISOString().split('T')[0]
    const res = await api.addMealRecord({
      user_id: userId,
      meal_type: mealType.value,
      food_items: foodItems.value,
      date: today
    })

    if (res.success) {
      analysis.value = res.data
    }
  } catch (error) {
    console.error('分析失败:', error)
    alert('分析失败: ' + error.message)
  } finally {
    analyzing.value = false
  }
}

const resetForm = () => {
  foodItems.value = []
  analysis.value = null
  mealType.value = 'lunch'
}
</script>

<style scoped>
.diet-record-page {
  padding-bottom: 24px;
}

.header {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  color: #fff;
  padding: 24px 16px;
  text-align: center;
}

.meal-types {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 16px;
}

.meal-btn {
  padding: 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 16px;
}

.meal-btn:hover {
  border-color: #1890ff;
}

.meal-btn.active {
  border-color: #1890ff;
  background: #e6f7ff;
  color: #1890ff;
  font-weight: bold;
}

.input-group {
  margin-bottom: 12px;
}

.analysis-score {
  text-align: center;
  margin: 20px 0;
}

.analysis-score p {
  margin-top: 12px;
  color: #666;
}

.analysis-details {
  margin: 24px 0;
}

.detail-item {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.detail-item:last-child {
  border-bottom: none;
}

.label {
  display: block;
  color: #666;
  margin-bottom: 8px;
  font-size: 14px;
}

.value {
  display: block;
  font-weight: 500;
}

.analysis-text {
  line-height: 1.6;
  color: #333;
}
</style>
