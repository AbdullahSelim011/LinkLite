<template>
  <div class="w-full h-full">
    <Doughnut
      :data="chartData"
      :options="chartOptions"
      class="w-full h-full"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  title: {
    type: String,
    default: 'Doughnut Chart'
  },
  height: {
    type: Number,
    default: 400
  },
  colors: {
    type: Array,
    default: () => [
      'rgba(59, 130, 246, 0.8)',
      'rgba(16, 185, 129, 0.8)',
      'rgba(245, 158, 11, 0.8)',
      'rgba(239, 68, 68, 0.8)',
      'rgba(139, 92, 246, 0.8)',
      'rgba(236, 72, 153, 0.8)',
      'rgba(20, 184, 166, 0.8)',
      'rgba(251, 146, 60, 0.8)'
    ]
  },
  borderColors: {
    type: Array,
    default: () => [
      'rgba(59, 130, 246, 1)',
      'rgba(16, 185, 129, 1)',
      'rgba(245, 158, 11, 1)',
      'rgba(239, 68, 68, 1)',
      'rgba(139, 92, 246, 1)',
      'rgba(236, 72, 153, 1)',
      'rgba(20, 184, 166, 1)',
      'rgba(251, 146, 60, 1)'
    ]
  }
})

const chartData = computed(() => ({
  labels: props.data.labels || [],
  datasets: props.data.datasets?.map((dataset, index) => ({
    ...dataset,
    backgroundColor: dataset.backgroundColor || props.colors,
    borderColor: dataset.borderColor || props.borderColors,
    borderWidth: 2,
    hoverBorderWidth: 4,
    hoverOffset: 8
  })) || []
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
      labels: {
        usePointStyle: true,
        padding: 20,
        font: {
          size: 12,
          family: 'Tajawal, sans-serif'
        },
        generateLabels: (chart) => {
          const datasets = chart.data.datasets
          if (datasets.length) {
            const dataset = datasets[0]
            const labels = chart.data.labels || []
            return labels.map((label, index) => ({
              text: label,
              fillStyle: dataset.backgroundColor[index],
              strokeStyle: dataset.borderColor[index],
              lineWidth: dataset.borderWidth,
              pointStyle: 'circle',
              hidden: false,
              index: index
            }))
          }
          return []
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
      },
      callbacks: {
        label: function(context) {
          const label = context.label || ''
          const value = context.parsed
          const total = context.dataset.data.reduce((acc, val) => acc + val, 0)
          const percentage = ((value / total) * 100).toFixed(1)
          return `${label}: ${value} (${percentage}%)`
        }
      }
    }
  },
  cutout: '70%',
  animation: {
    animateRotate: true,
    animateScale: true,
    duration: 1000,
    easing: 'easeOutQuart'
  },
  interaction: {
    intersect: false
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
