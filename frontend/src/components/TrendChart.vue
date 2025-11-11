<template>
  <div class="trend-chart">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import {
  Chart,
  LineController,
  BarController,
  LineElement,
  BarElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

// 注册 Chart.js 组件
Chart.register(
  LineController,
  BarController,
  LineElement,
  BarElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
)

const props = defineProps({
  type: {
    type: String,
    default: 'line' // line 或 bar
  },
  labels: {
    type: Array,
    required: true
  },
  data: {
    type: Array,
    required: true
  },
  label: {
    type: String,
    default: '数据'
  },
  color: {
    type: String,
    default: '#1890ff'
  }
})

const chartCanvas = ref(null)
let chartInstance = null

const createChart = () => {
  if (!chartCanvas.value) return
  
  if (chartInstance) {
    chartInstance.destroy()
  }
  
  const ctx = chartCanvas.value.getContext('2d')
  
  chartInstance = new Chart(ctx, {
    type: props.type,
    data: {
      labels: props.labels,
      datasets: [{
        label: props.label,
        data: props.data,
        backgroundColor: props.color + '40',
        borderColor: props.color,
        borderWidth: 2,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  })
}

onMounted(() => {
  createChart()
})

watch([() => props.data, () => props.labels], () => {
  createChart()
})
</script>

<style scoped>
.trend-chart {
  padding: 16px;
  background: #fff;
  border-radius: 12px;
  margin-bottom: 16px;
}

canvas {
  max-height: 250px;
}
</style>
