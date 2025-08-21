<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6" dir="rtl">
    <!-- Header -->
    <div class="max-w-7xl mx-auto mb-8">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-4xl font-bold text-gray-900 flex items-center">
            <span class="ml-3 text-blue-600">📊</span>
            <span class="relative">
              لوحة التحكم الرئيسية
              <span class="absolute bottom-0 right-0 w-full h-1 bg-blue-600 rounded-full"></span>
            </span>
          </h1>
          <p class="text-gray-600 mt-2 text-lg">
            مراقبة الأداء والإحصائيات في الوقت الفعلي
          </p>
        </div>
        <div class="flex items-center space-x-4 space-x-reverse">
          <Button @click="refreshData" :loading="refreshing" variant="outline" icon="refresh-cw" label="تحديث البيانات"
            class="px-4 py-2"></Button>
          <Button variant="ghost" icon="download" label="تصدير التقرير" class="px-4 py-2"></Button>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto space-y-8">
      <!-- Metrics Summary -->
      <MetricsSummary :metrics="metrics" :loading="loading" />


      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Revenue Trend Chart -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-semibold text-gray-800">اتجاه الإيرادات</h3>
            <div class="flex space-x-2 space-x-reverse">
              <button @click="revenueChartPeriod = 7" :class="[
                'px-3 py-1 text-sm rounded-md transition-colors',
                revenueChartPeriod === 7
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200',
              ]">
                7 أيام
              </button>
              <button @click="revenueChartPeriod = 30" :class="[
                'px-3 py-1 text-sm rounded-md transition-colors',
                revenueChartPeriod === 30
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200',
              ]">
                30 يوم
              </button>
              <button @click="revenueChartPeriod = 90" :class="[
                'px-3 py-1 text-sm rounded-md transition-colors',
                revenueChartPeriod === 90
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200',
              ]">
                90 يوم
              </button>
            </div>
          </div>
          <div class="h-80">
            <LineChart :data="revenueChartData" title="الإيرادات اليومية (ر.س)" />
          </div>
        </div>

        <!-- Trips Status Chart -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 class="text-xl font-semibold text-gray-800 mb-4">حالة الرحلات</h3>
          <div class="h-80">
            <DoughnutChart :key="JSON.stringify(tripsStatusChartData)" :data="tripsStatusChartData" title="توزيع حالات الرحلات" />
          </div>
        </div>
      </div>

      <!-- Charts Row 2 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Monthly Performance -->
        <div class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 class="text-xl font-semibold text-gray-800 mb-4">
            الأداء الشهري
          </h3>
          <div class="h-80">
            <BarChart :data="monthlyPerformanceData" title="مقارنة الأداء الشهري" />
          </div>
        </div>

        <!-- Driver Performance -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 class="text-xl font-semibold text-gray-800 mb-4">
            أداء السائقين
          </h3>
          <div class="space-y-4">
            <div v-for="driver in topDrivers" :key="driver.id"
              class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
              <div class="flex items-center">
                <div
                  class="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold mr-3">
                  {{ driver.name.charAt(0) }}
                </div>
                <div>
                  <p class="font-medium text-gray-800">{{ driver.name }}</p>
                  <p class="text-sm text-gray-500">{{ driver.trips }} رحلة</p>
                </div>
              </div>
              <div class="flex items-center">
                <div class="flex items-center mr-2">
                  <Star class="w-4 h-4 text-yellow-400 fill-current" />
                  <span class="text-sm font-medium text-gray-700 mr-1">{{
                    driver.rating
                    }}</span>
                </div>
                <div :class="[
                  'px-2 py-1 rounded-full text-xs font-medium',
                  driver.status === 'active'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-800',
                ]">
                  {{ driver.status === 'active' ? 'نشط' : 'غير متاح' }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activities & Alerts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Recent Activities -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-semibold text-gray-800">الأنشطة الأخيرة</h3>
            <Button variant="ghost" icon="external-link" label="عرض الكل" class="text-sm" />
          </div>
          <div class="space-y-4">
            <div v-for="activity in recentActivities" :key="activity.id"
              class="flex items-start space-x-3 space-x-reverse p-3 hover:bg-gray-50 rounded-lg transition-colors">
              <div :class="[
                'p-2 rounded-full mt-1',
                getActivityIconBg(activity.type),
              ]">
                <component :is="getActivityIcon(activity.type)"
                  :class="['w-4 h-4', getActivityIconColor(activity.type)]" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900">
                  {{ activity.title }}
                </p>
                <p class="text-sm text-gray-500">{{ activity.description }}</p>
                <p class="text-xs text-gray-400 mt-1">
                  {{ formatRelativeTime(activity.timestamp) }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Alerts & Notifications -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-semibold text-gray-800">
              التنبيهات والإشعارات
            </h3>
            <div class="flex items-center space-x-2 space-x-reverse">
              <span class="bg-red-100 text-red-800 text-xs font-medium px-2 py-1 rounded-full">
                {{ alerts.length }} تنبيه
              </span>
              <Button variant="ghost" icon="bell-off" class="text-sm p-1" @click="clearAllAlerts" />
            </div>
          </div>
          <div class="space-y-3">
            <div v-for="alert in alerts" :key="alert.id" :class="[
              'p-4 rounded-lg border-r-4 transition-all hover:shadow-sm',
              getAlertStyles(alert.level),
            ]">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center">
                    <component :is="getAlertIcon(alert.level)"
                      :class="['w-5 h-5 mr-2', getAlertIconColor(alert.level)]" />
                    <h4 class="text-sm font-semibold">{{ alert.title }}</h4>
                  </div>
                  <p class="text-sm text-gray-600 mt-1">{{ alert.message }}</p>
                  <p class="text-xs text-gray-500 mt-2">
                    {{ formatRelativeTime(alert.timestamp) }}
                  </p>
                </div>
                <Button variant="ghost" icon="x" class="p-1 opacity-50 hover:opacity-100"
                  @click="dismissAlert(alert.id)" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- System Status -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 class="text-xl font-semibold text-gray-800 mb-4">حالة النظام</h3>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="text-center">
            <div class="w-16 h-16 mx-auto mb-3 bg-green-100 rounded-full flex items-center justify-center">
              <Server class="w-8 h-8 text-green-600" />
            </div>
            <h4 class="font-medium text-gray-800">الخادم الرئيسي</h4>
            <p class="text-sm text-green-600 font-medium">متصل</p>
            <p class="text-xs text-gray-500">وقت التشغيل: 99.9%</p>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 mx-auto mb-3 bg-blue-100 rounded-full flex items-center justify-center">
              <Database class="w-8 h-8 text-blue-600" />
            </div>
            <h4 class="font-medium text-gray-800">قاعدة البيانات</h4>
            <p class="text-sm text-blue-600 font-medium">طبيعي</p>
            <p class="text-xs text-gray-500">استجابة: 12ms</p>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 mx-auto mb-3 bg-yellow-100 rounded-full flex items-center justify-center">
              <Wifi class="w-8 h-8 text-yellow-600" />
            </div>
            <h4 class="font-medium text-gray-800">الاتصال</h4>
            <p class="text-sm text-yellow-600 font-medium">بطيء</p>
            <p class="text-xs text-gray-500">زمن الاستجابة: 245ms</p>
          </div>
          <div class="text-center">
            <div class="w-16 h-16 mx-auto mb-3 bg-purple-100 rounded-full flex items-center justify-center">
              <Shield class="w-8 h-8 text-purple-600" />
            </div>
            <h4 class="font-medium text-gray-800">الأمان</h4>
            <p class="text-sm text-purple-600 font-medium">آمن</p>
            <p class="text-xs text-gray-500">آخر فحص: اليوم</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch , watchEffect, nextTick } from 'vue'
import { Button } from 'frappe-ui'
import MetricsSummary from '@/components/dashboard/MetricsSummary.vue'
import BarChart from '@/components/charts/BarChart.vue'
import LineChart from '@/components/charts/LineChart.vue'
import DoughnutChart from '@/components/charts/DoughnutChart.vue'
import { frappe } from '@/plugins/frappe'
import { toast } from 'vue-sonner'

const loading = ref(true)
const call = frappe.call() 
const metrics = ref({
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
  revenueChartData: [],
})

import {
  Star,
  Truck,
  Users,
  CheckCircle,
  AlertTriangle,
  User,
  Package,
  Server,
  Database,
  Wifi,
  Shield,
  AlertCircle,
  Info,
} from 'lucide-vue-next'

// Reactive data
const refreshing = ref(false)

const fetchMetrics = async () => {
  try {
    loading.value = true

    const response = await call.get('linklite.api.dashboard_data')
    console.log(response)

    if (response && response.data) {
      const data = response.data

      Object.assign(metrics.value, data)
      console.log('Updated metrics:', metrics.value)
    } else {
      console.error('Invalid response format:', response)
      toast.error('تنسيق البيانات غير صحيح')
    }
  } catch (error) {
    console.error('Error fetching metrics:', error)
    toast.error(`فشل في تحميل البيانات: ${error.message || error}`)
  } finally {
    loading.value = false
    console.log('Loading state set to false')
  }
}

// Chart data
const revenueChartPeriod = ref(30)
const revenueChartData = computed(() => {
  const records = metrics.value.revenueChartData?.records || []
  console.log("Revenue records:", records)

  // Labels = formatted posting_date (DD-MM)
  const labels = records.map(r => {
    const d = new Date(r.posting_date)
    return `${d.getDate().toString().padStart(2, '0')}-${(d.getMonth() + 1)
      .toString()
      .padStart(2, '0')}`
  })

  // Data = grand_total values
  const data = records.map(r => Number(r.grand_total) || 0)

  return {
    labels,
    datasets: [
      {
        label: 'الإيرادات',
        data,
        borderColor: 'rgba(59, 130, 246, 1)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
      },
    ],
  }
})

const fetchRevenueChartData = async (period = 30) => {
  try {
    loading.value = true

    const response = await call.get('linklite.api.revenueChartData', { period })
    console.log(response)

    if (response && response.message) {
      const data = response.message
      metrics.value.revenueChartData = data
    
    } else {
      console.error('Invalid response format:', response)
      toast.error('تنسيق البيانات غير صحيح')
    }
  } catch (error) {
    console.error('Error fetching metrics:', error)
    toast.error(`فشل في تحميل البيانات: ${error.message || error}`)
  } finally {
    loading.value = false
    console.log('Loading state set to false')
  }
}
watch(revenueChartPeriod, () => {
  fetchRevenueChartData(revenueChartPeriod.value)
})
console.log(revenueChartData)
const tripsStatusChartData = computed(() => {
  return {
    labels: ['مكتملة', 'قيد التنفيذ', 'ملغاه'],
    datasets: [
      {
        data: [
          Number(metrics.value.completedTrips) || 0,
          Number(metrics.value.ongoingTrips) || 0,
          Number(metrics.value.cancelledTrips) || 0,
        ],
        backgroundColor: [
          'rgba(16, 185, 129, 0.8)',  
          'rgba(59, 130, 246, 0.8)',  
          'rgba(245, 158, 11, 0.8)',  
        ],
      },
    ],
  }
})

const monthlyPerformanceData = reactive({
  labels: ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو'],
  datasets: [
    {
      label: 'الرحلات',
      data: [120, 150, 180, 140, 200, 220],
      backgroundColor: 'rgba(59, 130, 246, 0.8)',
    },
    {
      label: 'الإيرادات (آلاف ر.س)',
      data: [80, 95, 120, 85, 140, 155],
      backgroundColor: 'rgba(16, 185, 129, 0.8)',
    },
  ],
})

// Top drivers data
const topDrivers = reactive([
  { id: 1, name: 'أحمد محمد', trips: 45, rating: 4.8, status: 'active' },
  { id: 2, name: 'سعد العتيبي', trips: 42, rating: 4.7, status: 'active' },
  { id: 3, name: 'محمد الزهراني', trips: 38, rating: 4.6, status: 'active' },
  { id: 4, name: 'خالد الشهري', trips: 35, rating: 4.5, status: 'inactive' },
  { id: 5, name: 'عبدالله القحطاني', trips: 33, rating: 4.4, status: 'active' },
])

// Recent activities
const recentActivities = reactive([
  {
    id: 1,
    type: 'trip_completed',
    title: 'رحلة مكتملة',
    description: 'تم إكمال رحلة إلى الرياض بواسطة أحمد محمد',
    timestamp: new Date(Date.now() - 300000), // 5 minutes ago
  },
  {
    id: 2,
    type: 'new_customer',
    title: 'عميل جديد',
    description: 'انضم عميل جديد: شركة النقل المتقدم',
    timestamp: new Date(Date.now() - 900000), // 15 minutes ago
  },
  {
    id: 3,
    type: 'payment_received',
    title: 'دفعة مستلمة',
    description: 'تم استلام دفعة بقيمة 15,000 ر.س من شركة الخليج',
    timestamp: new Date(Date.now() - 1800000), // 30 minutes ago
  },
  {
    id: 4,
    type: 'vehicle_maintenance',
    title: 'صيانة مركبة',
    description: 'تم جدولة صيانة للشاحنة رقم ABC-123',
    timestamp: new Date(Date.now() - 3600000), // 1 hour ago
  },
])

// Alerts
const alerts = reactive([
  {
    id: 1,
    level: 'error',
    title: 'رحلة متأخرة',
    message: 'الرحلة #1234 متأخرة بأكثر من ساعة عن الموعد المحدد',
    timestamp: new Date(Date.now() - 600000),
  },
  {
    id: 2,
    level: 'warning',
    title: 'مركبة تحتاج صيانة',
    message: 'الشاحنة ABC-789 قد تحتاج صيانة دورية قريباً',
    timestamp: new Date(Date.now() - 1200000),
  },
  {
    id: 3,
    level: 'info',
    title: 'تقرير شهري متاح',
    message: 'تقرير الأداء الشهري لشهر نوفمبر جاهز للمراجعة',
    timestamp: new Date(Date.now() - 1800000),
  },
])

// Helper functions
const formatRelativeTime = (timestamp) => {
  const now = new Date()
  const diff = now - timestamp
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return 'الآن'
  if (minutes < 60) return `منذ ${minutes} دقيقة`
  if (hours < 24) return `منذ ${hours} ساعة`
  return `منذ ${days} يوم`
}

const getActivityIcon = (type) => {
  const icons = {
    trip_completed: CheckCircle,
    new_customer: User,
    payment_received: Package,
    vehicle_maintenance: Truck,
  }
  return icons[type] || Info
}

const getActivityIconBg = (type) => {
  const backgrounds = {
    trip_completed: 'bg-green-100',
    new_customer: 'bg-blue-100',
    payment_received: 'bg-yellow-100',
    vehicle_maintenance: 'bg-purple-100',
  }
  return backgrounds[type] || 'bg-gray-100'
}

const getActivityIconColor = (type) => {
  const colors = {
    trip_completed: 'text-green-600',
    new_customer: 'text-blue-600',
    payment_received: 'text-yellow-600',
    vehicle_maintenance: 'text-purple-600',
  }
  return colors[type] || 'text-gray-600'
}

const getAlertIcon = (level) => {
  const icons = {
    error: AlertCircle,
    warning: AlertTriangle,
    info: Info,
  }
  return icons[level] || Info
}

const getAlertStyles = (level) => {
  const styles = {
    error: 'bg-red-50 border-red-400',
    warning: 'bg-yellow-50 border-yellow-400',
    info: 'bg-blue-50 border-blue-400',
  }
  return styles[level] || 'bg-gray-50 border-gray-400'
}

const getAlertIconColor = (level) => {
  const colors = {
    error: 'text-red-600',
    warning: 'text-yellow-600',
    info: 'text-blue-600',
  }
  return colors[level] || 'text-gray-600'
}

const refreshData = async () => {
  refreshing.value = true
  try {
    // Refresh metrics
    if (metrics.value) {
      await fetchMetrics()
    }

  } catch (error) {
    console.error('Error refreshing data:', error)
  } finally {
    refreshing.value = false
  }
}

const clearAllAlerts = () => {
  alerts.splice(0, alerts.length)
}

const dismissAlert = (id) => {
  const index = alerts.findIndex((alert) => alert.id === id)
  if (index > -1) {
    alerts.splice(index, 1)
  }
}

onMounted(() => {
  fetchMetrics()
})

onMounted(async () => {
  await fetchMetrics()
  await nextTick()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');

* {
  font-family: 'Tajawal', sans-serif;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Animation classes */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.5s ease-out;
}
</style>
