<template>
  <div class="login-container">
    <div class="login-box">
      <h1>🏃‍♂️ FamilyFit 健康助手</h1>
      <p class="subtitle">记录运动，健康生活</p>

      <div class="tabs">
        <button 
          :class="{ active: isLogin }" 
          @click="isLogin = true"
        >
          登录
        </button>
        <button 
          :class="{ active: !isLogin }" 
          @click="isLogin = false"
        >
          注册
        </button>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>👤 用户名</label>
          <input 
            v-model="form.username" 
            type="text" 
            placeholder="请输入用户名"
            required
          />
        </div>

        <div class="form-group">
          <label>🔒 密码</label>
          <input 
            v-model="form.password" 
            type="password" 
            placeholder="请输入密码"
            required
          />
        </div>

        <div v-if="!isLogin" class="form-group">
          <label>📝 显示名称</label>
          <input 
            v-model="form.name" 
            type="text" 
            placeholder="请输入您的名字"
            :required="!isLogin"
          />
        </div>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? '处理中...' : (isLogin ? '登录' : '注册') }}
        </button>
      </form>

      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="isLogin" class="hint">💡 测试账号: test / 123456</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const isLogin = ref(true)
const loading = ref(false)
const error = ref('')

const form = ref({
  username: '',
  password: '',
  name: ''
})

const handleSubmit = async () => {
  error.value = ''
  loading.value = true

  try {
    const endpoint = isLogin.value ? '/auth/login' : '/auth/register'
    const data = isLogin.value 
      ? { username: form.value.username, password: form.value.password }
      : form.value

    const response = await api.post(endpoint, data)
    
    // 保存用户信息和 token
    localStorage.setItem('token', response.data.token)
    localStorage.setItem('user', JSON.stringify(response.data))
    
    // 跳转到首页
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || '操作失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-box {
  background: white;
  border-radius: 20px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 10px;
  font-size: 28px;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 30px;
  font-size: 14px;
}

.tabs {
  display: flex;
  margin-bottom: 30px;
  background: #f5f5f5;
  border-radius: 10px;
  padding: 4px;
}

.tabs button {
  flex: 1;
  padding: 10px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s;
  color: #666;
}

.tabs button.active {
  background: white;
  color: #667eea;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 16px;
  transition: border-color 0.3s;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.submit-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  color: #f44336;
  text-align: center;
  margin-top: 15px;
  font-size: 14px;
}

.hint {
  color: #999;
  text-align: center;
  margin-top: 15px;
  font-size: 13px;
}
</style>
