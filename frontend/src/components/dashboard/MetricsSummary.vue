<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
    <StatCard
      title="إجمالي الرحلات"
      subtitle="الرحلات المكتملة هذا الشهر"
      :value="props.metrics.totalTrips"
      :icon="TruckIcon"
      color="blue"
      :change="12.5"
      changeLabel="من الشهر الماضي"
      description="رحلة جديدة في آخر 24 ساعة 15"
      :loading="props.loading"
    />

    <StatCard
      title="إجمالي الإيرادات"
      subtitle="الإيرادات هذا الشهر"
      :value="formatCurrency(props.metrics.totalRevenue)"
      unit="ر.س"
      :icon="DollarSignIcon"
      color="green"
      :change="8.2"
      changeLabel="من الشهر الماضي"
      description="متوسط الإيرادات اليومية"
      :loading="props.loading"
    />

    <StatCard
      title="العملاء النشطين"
      subtitle="العملاء الذين طلبوا خدمات"
      :value="props.metrics.activeCustomers"
      :icon="UsersIcon"
      color="purple"
      :change="15.3"
      changeLabel="من الشهر الماضي"
      description="عميل جديد هذا الأسبوع 8"
      :loading="props.loading"
    />
  </div>

  <!-- Additional metrics row -->
  <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-8">
    <div
      class="bg-white rounded-lg shadow-sm border border-gray-100 p-4 text-center"
    >
      <div class="flex items-center justify-center mb-2">
        <div class="p-2 bg-red-100 rounded-full">
          <AlertTriangleIcon class="w-5 h-5 text-red-600" />
        </div>
      </div>
      <h4 class="text-sm font-medium text-gray-700">الرحلات الملغاه</h4>
      <p class="text-2xl font-bold text-red-600">
        {{ props.metrics.cancelledTrips }}
      </p>
      <p class="text-xs text-gray-500">تحتاج متابعة</p>
    </div>

    <div
      class="bg-white rounded-lg shadow-sm border border-gray-100 p-4 text-center"
    >
      <div class="flex items-center justify-center mb-2">
        <div class="p-2 bg-blue-100 rounded-full">
          <MapPinIcon class="w-5 h-5 text-blue-600" />
        </div>
      </div>
      <h4 class="text-sm font-medium text-gray-700">رحلات قيد التنفيذ</h4>
      <p class="text-2xl font-bold text-blue-600">
        {{ props.metrics.ongoingTrips }}
      </p>
      <p class="text-xs text-gray-500">على الطريق</p>
    </div>

    <div
      class="bg-white rounded-lg shadow-sm border border-gray-100 p-4 text-center"
    >
      <div class="flex items-center justify-center mb-2">
        <div class="p-2 bg-green-100 rounded-full">
          <CheckCircleIcon class="w-5 h-5 text-green-600" />
        </div>
      </div>
      <h4 class="text-sm font-medium text-gray-700">رحلات مكتملة</h4>
      <p class="text-2xl font-bold text-green-600">
        {{ props.metrics.completedTrips }}
      </p>
      <p class="text-xs text-gray-500">اليوم</p>
    </div>

    <div
      class="bg-white rounded-lg shadow-sm border border-gray-100 p-4 text-center"
    >
      <div class="flex items-center justify-center mb-2">
        <div class="p-2 bg-purple-100 rounded-full">
          <CarIcon class="w-5 h-5 text-purple-600" />
        </div>
      </div>
      <h4 class="text-sm font-medium text-gray-700">مركبات متاحة</h4>
      <p class="text-2xl font-bold text-purple-600">
        {{ props.metrics.availableVehicles }}
      </p>
      <p class="text-xs text-gray-500">
        من إجمالي {{ props.metrics.totalVehicles }}
      </p>
    </div>

    <div
      class="bg-white rounded-lg shadow-sm border border-gray-100 p-4 text-center"
    >
      <div class="flex items-center justify-center mb-2">
        <div class="p-2 bg-indigo-100 rounded-full">
          <UserCheckIcon class="w-5 h-5 text-indigo-600" />
        </div>
      </div>
      <h4 class="text-sm font-medium text-gray-700">سائقين نشطين</h4>
      <p class="text-2xl font-bold text-indigo-600">
        {{ props.metrics.activeDrivers }}
      </p>
      <p class="text-xs text-gray-500">
        من إجمالي {{ props.metrics.totalDrivers }}
      </p>
    </div>
  </div>
</template>

<script setup>
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
  Clock as ClockIcon,
} from 'lucide-vue-next'

const props = defineProps({
  metrics: {
    type: Object,
    default: () => ({
      totalTrips: 0,
      totalRevenue: 0,
      activeCustomers: 0,
      cancelledTrips: 0,
      ongoingTrips: 0,
      completedTrips: 0,
      availableVehicles: 0,
      totalVehicles: 0,
      activeDrivers: 0,
      totalDrivers: 0,
    }),
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ar-SA', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');

* {
  font-family: 'Tajawal', sans-serif;
}
</style>
