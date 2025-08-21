<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
    <div class="flex items-center justify-between">
      <div class="flex-1">
        <div class="flex items-center mb-2">
          <div :class="[
            'p-3 rounded-full mr-4 transition-colors duration-300',
            iconBgClass
          ]">
            <component
              :is="icon"
              :class="[
                'w-6 h-6 transition-colors duration-300',
                iconColorClass
              ]"
            />
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-800 mb-1">{{ title }}</h3>
            <p class="text-sm text-gray-500">{{ subtitle }}</p>
          </div>
        </div>

        <div class="mt-4">
          <div class="flex items-baseline">
            <p :class="[
              'text-3xl font-bold transition-colors duration-300',
              valueColorClass
            ]">
              {{ formattedValue }}
            </p>
            <span v-if="unit" class="text-lg text-gray-500 mr-2">{{ unit }}</span>
          </div>

          <!-- <div v-if="change !== undefined" class="flex items-center mt-2">
            <component
              :is="changeIcon"
              :class="[
                'w-4 h-4 mr-1',
                changeColorClass
              ]"
            />
            <span :class="[
              'text-sm font-medium',
              changeColorClass
            ]">
              {{ Math.abs(change) }}{{ changeUnit }}
            </span>
            <span class="text-sm text-gray-500 mr-2">{{ changeLabel }}</span>
          </div> -->

          <!-- <div v-if="description" class="mt-2">
            <p class="text-xs text-gray-400">{{ description }}</p>
          </div> -->
        </div>
      </div>

      <!-- Progress bar if percentage is provided -->
      <div v-if="percentage !== undefined" class="w-2 h-20 bg-gray-200 rounded-full ml-4">
        <div
          :class="[
            'h-full rounded-full transition-all duration-1000 ease-out',
            progressBarClass
          ]"
          :style="{ height: `${Math.min(percentage, 100)}%` }"
        ></div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="absolute inset-0 bg-white bg-opacity-75 rounded-xl flex items-center justify-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { TrendingUp, TrendingDown } from 'lucide-vue-next'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  value: {
    type: [Number, String],
    required: true
  },
  unit: {
    type: String,
    default: ''
  },
  icon: {
    type: Object,
    required: true
  },
  color: {
    type: String,
    default: 'blue',
    validator: (value) => ['blue', 'green', 'yellow', 'red', 'purple', 'indigo', 'pink', 'cyan'].includes(value)
  },
  change: {
    type: Number,
    default: undefined
  },
  changeUnit: {
    type: String,
    default: '%'
  },
  changeLabel: {
    type: String,
    default: 'من الأمس'
  },
  description: {
    type: String,
    default: ''
  },
  percentage: {
    type: Number,
    default: undefined
  },
  loading: {
    type: Boolean,
    default: false
  },
  animate: {
    type: Boolean,
    default: true
  }
})

const colorVariants = {
  blue: {
    icon: 'text-blue-600',
    iconBg: 'bg-blue-100 group-hover:bg-blue-200',
    value: 'text-blue-600',
    progress: 'bg-blue-500',
    changePositive: 'text-green-600',
    changeNegative: 'text-red-600'
  },
  green: {
    icon: 'text-green-600',
    iconBg: 'bg-green-100 group-hover:bg-green-200',
    value: 'text-green-600',
    progress: 'bg-green-500',
    changePositive: 'text-green-600',
    changeNegative: 'text-red-600'
  },
  yellow: {
    icon: 'text-yellow-600',
    iconBg: 'bg-yellow-100 group-hover:bg-yellow-200',
    value: 'text-yellow-600',
    progress: 'bg-yellow-500',
    changePositive: 'text-green-600',
    changeNegative: 'text-red-600'
  },
  red: {
    icon: 'text-red-600',
    iconBg: 'bg-red-100 group-hover:bg-red-200',
    value: 'text-red-600',
    progress: 'bg-red-500',
    changePositive: 'text-green-600',
    changeNegative: 'text-red-600'
  },
  purple: {
    icon: 'text-purple-600',
    iconBg: 'bg-purple-100 group-hover:bg-purple-200',
    value: 'text-purple-600',
    progress: 'bg-purple-500',
    changePositive: 'text-green-600',
    changeNegative: 'text-red-600'
  },
  indigo: {
    icon: 'text-indigo-600',
    iconBg: 'bg-indigo-100 group-hover:bg-indigo-200',
    value: 'text-indigo-600',
    progress: 'bg-indigo-500',
    changePositive: 'text-green-600',
    changeNegative: 'text-red-600'
  },
  pink: {
    icon: 'text-pink-600',
    iconBg: 'bg-pink-100 group-hover:bg-pink-200',
    value: 'text-pink-600',
    progress: 'bg-pink-500',
    changePositive: 'text-green-600',
    changeNegative: 'text-red-600'
  },
  cyan: {
    icon: 'text-cyan-600',
    iconBg: 'bg-cyan-100 group-hover:bg-cyan-200',
    value: 'text-cyan-600',
    progress: 'bg-cyan-500',
    changePositive: 'text-green-600',
    changeNegative: 'text-red-600'
  }
}

const iconColorClass = computed(() => colorVariants[props.color]?.icon || 'text-blue-600')
const iconBgClass = computed(() => colorVariants[props.color]?.iconBg || 'bg-blue-100 group-hover:bg-blue-200')
const valueColorClass = computed(() => colorVariants[props.color]?.value || 'text-blue-600')
const progressBarClass = computed(() => colorVariants[props.color]?.progress || 'bg-blue-500')

const changeIcon = computed(() => {
  if (props.change === undefined) return null
  return props.change >= 0 ? TrendingUp : TrendingDown
})

const changeColorClass = computed(() => {
  if (props.change === undefined) return ''
  const variant = colorVariants[props.color]
  return props.change >= 0 ? variant?.changePositive || 'text-green-600' : variant?.changeNegative || 'text-red-600'
})

const formattedValue = computed(() => {
  if (typeof props.value === 'number') {
    return props.value.toLocaleString('ar-SA')
  }
  return props.value
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');

* {
  font-family: 'Tajawal', sans-serif;
}

.group:hover .group-hover\:bg-blue-200 {
  background-color: rgb(219 234 254);
}

.group:hover .group-hover\:bg-green-200 {
  background-color: rgb(220 252 231);
}

.group:hover .group-hover\:bg-yellow-200 {
  background-color: rgb(254 240 138);
}

.group:hover .group-hover\:bg-red-200 {
  background-color: rgb(254 202 202);
}

.group:hover .group-hover\:bg-purple-200 {
  background-color: rgb(233 213 255);
}

.group:hover .group-hover\:bg-indigo-200 {
  background-color: rgb(199 210 254);
}

.group:hover .group-hover\:bg-pink-200 {
  background-color: rgb(251 207 232);
}

.group:hover .group-hover\:bg-cyan-200 {
  background-color: rgb(165 243 252);
}
</style>
