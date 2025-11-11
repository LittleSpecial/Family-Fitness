<template>
  <div class="exercise-upload-page">
    <div class="header">
      <h1>运动上传</h1>
    </div>

    <div class="container">
      <!-- 上传区域 -->
      <div class="card upload-area">
        <h3>上传运动截图</h3>
        <div class="upload-box" @click="triggerFileInput">
          <input
            ref="fileInput"
            type="file"
            accept="image/jpeg,image/png,image/jpg"
            @change="handleFileSelect"
            style="display: none"
          />
          <div v-if="!uploading && !result">
            <div class="upload-icon">📸</div>
            <p>点击上传运动截图</p>
            <p class="upload-hint">支持 JPG/PNG,最大 10MB</p>
          </div>
          <div v-else-if="uploading" class="uploading">
            <div class="spinner"></div>
            <p>识别中...</p>
          </div>
        </div>
      </div>

      <!-- 识别结果 -->
      <div v-if="result" class="card result-card">
        <h3>识别结果</h3>
        <div class="result-score">
          <div class="score-circle score-high">{{ result.score }}</div>
          <p>运动得分</p>
        </div>
        <div class="result-details">
          <div class="detail-item">
            <span class="label">运动类型</span>
            <span class="value">{{ result.exercise_type }}</span>
          </div>
          <div class="detail-item">
            <span class="label">时长</span>
            <span class="value">{{ result.duration_min }} 分钟</span>
          </div>
          <div class="detail-item">
            <span class="label">卡路里</span>
            <span class="value">{{ result.calories }} 千卡</span>
          </div>
          <div class="detail-item" v-if="result.steps">
            <span class="label">步数</span>
            <span class="value">{{ result.steps }} 步</span>
          </div>
          <div class="detail-item" v-if="result.avg_heart_rate">
            <span class="label">平均心率</span>
            <span class="value">{{ result.avg_heart_rate }} bpm</span>
          </div>
        </div>
        <button class="btn btn-primary" @click="reset">重新上传</button>
      </div>

      <!-- 错误提示 -->
      <div v-if="error" class="card error-card">
        <p>{{ error }}</p>
        <button class="btn btn-primary" @click="reset">重试</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'

const userId = 1
const fileInput = ref(null)
const uploading = ref(false)
const result = ref(null)
const error = ref(null)

const triggerFileInput = () => {
  if (!uploading.value) {
    fileInput.value.click()
  }
}

const handleFileSelect = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // 验证文件大小
  if (file.size > 10 * 1024 * 1024) {
    error.value = '文件大小超过 10MB'
    return
  }

  uploading.value = true
  error.value = null
  result.value = null

  try {
    const res = await api.parseExerciseReport(file, userId)
    if (res.success) {
      result.value = res.data
    }
  } catch (err) {
    error.value = err.message || '识别失败,请重试'
  } finally {
    uploading.value = false
  }
}

const reset = () => {
  result.value = null
  error.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>

<style scoped>
.exercise-upload-page {
  padding-bottom: 24px;
}

.header {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: #fff;
  padding: 24px 16px;
  text-align: center;
}

.upload-area h3 {
  margin-bottom: 16px;
}

.upload-box {
  border: 2px dashed #d9d9d9;
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.upload-box:hover {
  border-color: #1890ff;
  background: #f0f9ff;
}

.upload-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.upload-hint {
  font-size: 12px;
  color: #999;
  margin-top: 8px;
}

.uploading {
  padding: 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f0f0f0;
  border-top-color: #1890ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.result-card {
  margin-top: 16px;
}

.result-score {
  text-align: center;
  margin: 20px 0;
}

.result-score p {
  margin-top: 12px;
  color: #666;
}

.result-details {
  margin: 24px 0;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.detail-item:last-child {
  border-bottom: none;
}

.label {
  color: #666;
}

.value {
  font-weight: 500;
}

.error-card {
  margin-top: 16px;
  text-align: center;
  color: #ff4d4f;
}

.error-card p {
  margin-bottom: 16px;
}
</style>
