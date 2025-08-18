<template>
  <div class="w-full h-full">
    <Line
      :data="chartData"
      :options="chartOptions"
      class="w-full h-full"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  title: {
    type: String,
    default: 'Line Chart'
  },
  height: {
    type: Number,
    default: 400
  },
  colors: {
    type: Array,
    default: () => [
      'rgba(59, 130, 246, 1)',
      'rgba(16, 185, 129, 1)',
      'rgba(245, 158, 11, 1)',
      'rgba(239, 68, 68, 1)',
      'rgba(139, 92, 246, 1)',
      'rgba(236, 72, 153, 1)'
    ]
  },
  fillColors: {
    type: Array,
    default: () => [
      'rgba(59, 130, 246, 0.1)',
      'rgba(16, 185, 129, 0.1)',
      'rgba(245, 158, 11, 0.1)',
      'rgba(239, 68, 68, 0.1)',
      'rgba(139, 92, 246, 0.1)',
      'rgba(236, 72, 153, 0.1)'
    ]
  }
})

const chartData = computed(() => ({
  labels: props.data.labels || [],
  datasets: props.data.datasets?.map((dataset, index) => ({
    ...dataset,
    borderColor: dataset.borderColor || props.colors[index % props.colors.length],
    backgroundColor: dataset.backgroundColor || props.fillColors[index % props.fillColors.length],
    borderWidth: 3,
    fill: dataset.fill !== undefined ? dataset.fill : true,
    tension: 0.4,
    pointBackgroundColor: dataset.borderColor || props.colors[index % props.colors.length],
    pointBorderColor: '#fff',
    pointBorderWidth: 2,
    pointRadius: 5,
    pointHoverRadius: 8,
    pointHoverBackgroundColor: dataset.borderColor || props.colors[index % props.colors.length],
    pointHoverBorderColor: '#fff',
    pointHoverBorderWidth: 3
  })) || []
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      labels: {
        usePointStyle: true,
        padding: 20,
        font: {
          size: 12,
          family: 'Tajawal, sans-serif'
        }
      }
    },
    title: {
      display: true,
      text: props.title,
      font: {
        size: 16,
        weight: 'bold',
        family: 'Tajawal, sans-serif'
      },
      padding: {
        bottom: 20
      }
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: 'white',
      bodyColor: 'white',
      borderColor: 'rgba(255, 255, 255, 0.1)',
      borderWidth: 1,
      cornerRadius: 8,
      displayColors: true,
      titleFont: {
        family: 'Tajawal, sans-serif'
      },
      bodyFont: {
        family: 'Tajawal, sans-serif'
      }
    }
  },
  scales: {
    x: {
      grid: {
        display: false
      },
      ticks: {
        font: {
          family: 'Tajawal, sans-serif'
        }
      }
    },
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(0, 0, 0, 0.05)',
        drawBorder: false
      },
      ticks: {
        font: {
          family: 'Tajawal, sans-serif'
        }
      }
    }
  },
  elements: {
    line: {
      tension: 0.4
    }
  },
  animation: {
    duration: 1000,
    easing: 'easeOutQuart'
  },
  interaction: {
    intersect: false,
    mode: 'index'
  }
}))
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}
</style>
