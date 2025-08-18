<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
    <StatCard
      title="إجمالي الرحلات"
      subtitle="الرحلات المكتملة هذا الشهر"
      :value="metrics.totalTrips"
      :icon="TruckIcon"
      color="blue"
      :change="12.5"
      changeLabel="من الشهر الماضي"
      description="رحلة جديدة في آخر 24 ساعة 15"
      :loading="loading"
    />

    <StatCard
      title="إجمالي الإيرادات"
      subtitle="الإيرادات هذا الشهر"
      :value="formatCurrency(metrics.totalRevenue)"
      unit="ر.س"
      :icon="DollarSignIcon"
      color="green"
      :change="8.2"
      changeLabel="من الشهر الماضي"
      description="متوسط الإيرادات اليومية"
      :loading="loading"
    />

    <StatCard
      title="العملاء النشطين"
      subtitle="العملاء الذين طلبوا خدمات"
      :value="metrics.activeCustomers"
      :icon="UsersIcon"
      color="purple"
      :change="15.3"
      changeLabel="من الشهر الماضي"
      description="عميل جديد هذا الأسبوع 8"
      :loading="loading"
    />

    <StatCard
      title="معدل الرضا"
      subtitle="تقييمات العملاء"
      :value="metrics.satisfactionRate"
      unit="%"
      :icon="StarIcon"
      color="yellow"
      :change="-2.1"
      changeLabel="من الشهر الماضي"
      :percentage="metrics.satisfactionRate"
      description="على أساس 1,234 تقييم"
      :loading="loading"
    />
  </div>

  <!-- Additional metrics row -->
  <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
    <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4 text-center">
      <div class="flex items-center justify-center mb-2">
        <div class="p-2 bg-red-100 rounded-full">
          <AlertTriangleIcon class="w-5 h-5 text-red-600" />
        </div>
      </div>
      <h4 class="text-sm font-medium text-gray-700">رحلات متأخرة</h4>
      <p class="text-2xl font-bold text-red-600">{{ metrics.delayedTrips }}</p>
      <p class="text-xs text-gray-500">تحتاج متابعة</p>
    </div>

    <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4 text-center">
      <div class="flex items-center justify-center mb-2">
        <div class="p-2 bg-blue-100 rounded-full">
          <MapPinIcon class="w-5 h-5 text-blue-600" />
        </div>
      </div>
      <h4 class="text-sm font-medium text-gray-700">رحلات قيد التنفيذ</h4>
      <p class="text-2xl font-bold text-blue-600">{{ metrics.ongoingTrips }}</p>
      <p class="text-xs text-gray-500">على الطريق</p>
    </div>

    <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4 text-center">
      <div class="flex items-center justify-center mb-2">
        <div class="p-2 bg-green-100 rounded-full">
          <CheckCircleIcon class="w-5 h-5 text-green-600" />
        </div>
      </div>
      <h4 class="text-sm font-medium text-gray-700">رحلات مكتملة</h4>
      <p class="text-2xl font-bold text-green-600">{{ metrics.completedTrips }}</p>
      <p class="text-xs text-gray-500">اليوم</p>
    </div>

    <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4 text-center">
      <div class="flex items-center justify-center mb-2">
        <div class="p-2 bg-purple-100 rounded-full">
          <CarIcon class="w-5 h-5 text-purple-600" />
        </div>
      </div>
      <h4 class="text-sm font-medium text-gray-700">مركبات متاحة</h4>
      <p class="text-2xl font-bold text-purple-600">{{ metrics.availableVehicles }}</p>
      <p class="text-xs text-gray-500">من إجمالي {{ metrics.totalVehicles }}</p>
    </div>

    <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4 text-center">
      <div class="flex items-center justify-center mb-2">
        <div class="p-2 bg-indigo-100 rounded-full">
          <UserCheckIcon class="w-5 h-5 text-indigo-600" />
        </div>
      </div>
      <h4 class="text-sm font-medium text-gray-700">سائقين نشطين</h4>
      <p class="text-2xl font-bold text-indigo-600">{{ metrics.activeDrivers }}</p>
      <p class="text-xs text-gray-500">من إجمالي {{ metrics.totalDrivers }}</p>
    </div>

    <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4 text-center">
      <div class="flex items-center justify-center mb-2">
        <div class="p-2 bg-cyan-100 rounded-full">
          <ClockIcon class="w-5 h-5 text-cyan-600" />
        </div>
      </div>
      <h4 class="text-sm font-medium text-gray-700">متوسط وقت التسليم</h4>
      <p class="text-2xl font-bold text-cyan-600">{{ metrics.averageDeliveryTime }}</p>
      <p class="text-xs text-gray-500">دقيقة</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import StatCard from './StatCard.vue'
import {
  Truck as TruckIcon,
  DollarSign as DollarSignIcon,
  Users as UsersIcon,
  Star as StarIcon,
  AlertTriangle as AlertTriangleIcon,
  MapPin as MapPinIcon,
  CheckCircle as CheckCircleIcon,
  Car as CarIcon,
  UserCheck as UserCheckIcon,
  Clock as ClockIcon
} from 'lucide-vue-next'

const props = defineProps({
  refreshInterval: {
    type: Number,
    default: 300000 // 5 minutes
  }
})

const loading = ref(true)
const metrics = ref({
  totalTrips: 0,
  totalRevenue: 0,
  activeCustomers: 0,
  satisfactionRate: 0,
  delayedTrips: 0,
  ongoingTrips: 0,
  completedTrips: 0,
  availableVehicles: 0,
  totalVehicles: 0,
  activeDrivers: 0,
  totalDrivers: 0,
  averageDeliveryTime: 0
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ar-SA', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}

const fetchMetrics = async () => {
  try {
    loading.value = true

    // Simulate API call - replace with actual API
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Mock data - replace with real API data
    metrics.value = {
      totalTrips: 1247,
      totalRevenue: 185600,
      activeCustomers: 342,
      satisfactionRate: 94.2,
      delayedTrips: 8,
      ongoingTrips: 23,
      completedTrips: 15,
      availableVehicles: 18,
      totalVehicles: 25,
      activeDrivers: 21,
      totalDrivers: 28,
      averageDeliveryTime: 42
    }

    /*
    // Real API implementation example:
    const response = await frappe.call({
      method: 'linklite.api.dashboard.get_metrics'
    })

    if (response.message) {
      metrics.value = response.message
    }
    */

  } catch (error) {
    console.error('Error fetching metrics:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchMetrics()

  // Set up auto-refresh
  if (props.refreshInterval > 0) {
    setInterval(fetchMetrics, props.refreshInterval)
  }
})

// Expose refresh method for parent components
defineExpose({
  refresh: fetchMetrics
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');

* {
  font-family: 'Tajawal', sans-serif;
}
</style>
