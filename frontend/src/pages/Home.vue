<template>
  <div
    class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6"
    dir="rtl"
  >
    <div class="max-w-7xl mx-auto mb-10 animate-fade-in-down">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-4xl font-bold text-gray-900 flex items-center">
            <span
              class="ml-3 text-blue-600 transform transition-transform hover:scale-110"
              >🚛</span
            >
            <span class="relative">
              نظام جود لإدارة النقل
              <span
                class="absolute bottom-0 right-0 w-full h-1 bg-blue-600 rounded-full animate-underline"
              ></span>
            </span>
          </h1>
          <p class="text-gray-600 mt-3 text-lg">
            نظام متكامل لإدارة النقل والخدمات اللوجستية بكل كفاءة
          </p>
        </div>
        <div class="flex items-center space-x-4 space-x-reverse">
          <RouterLink to="/dashboard">
            <Button
              variant="outline"
              icon="bar-chart"
              label="لوحة التحكم"
              class="w-full bg-blue-600 hover:bg-blue-700 py-3 text-lg font-medium transition-colors"
            ></Button>
          </RouterLink>
          <Button
            variant="ghost"
            icon="bell"
            class="relative p-3 hover:bg-gray-100 rounded-full transition-colors animate-pulse-once"
          >
            <span
              class="absolute top-1 right-1 h-3 w-3 rounded-full bg-red-500 ring-2 ring-white"
            ></span>
          </Button>
          <Button
            variant="ghost"
            icon="user"
            label="حسابي"
            class="px-4 py-2 border border-gray-200 hover:border-blue-500 rounded-lg transition-all flex items-center space-x-2 space-x-reverse"
          ></Button>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto">
      <!-- Dashboard Quick Link -->
      <div class="mb-8">
        <RouterLink to="/dashboard" class="block">
          <div
            class="bg-white  rounded-2xl shadow-lg p-8 text-gray-900 transform transition-transform hover:-translate-y-1 hover:shadow-xl"
          >
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-2xl font-bold mb-2">📊 لوحة التحكم الشاملة</h2>
                <p class="text-gray-600 mb-4">
                  اطلع على جميع الإحصائيات والمقاييس في مكان واحد
                </p>
                <Button
                  variant="outline"
                  class="px-6 py-3 font-medium hover:bg-blue-600 hover:text-white transition-colors"
                >
                  عرض لوحة التحكم
                </Button>
              </div>
              <div class="hidden md:block">
                <div class="text-6xl">📈</div>
              </div>
            </div>
          </div>
        </RouterLink>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
        <RouterLink
          to="/deliverytrip"
          class="transform transition-transform hover:-translate-y-1"
        >
          <div
            class="bg-white rounded-2xl shadow-sm overflow-hidden hover:shadow-lg transition-all duration-300 border-l-4 border-blue-500 h-full group card-animation-delay-1"
          >
            <div class="p-7">
              <div class="flex items-center mb-5">
                <div
                  class="bg-blue-100 p-3 rounded-full ml-4 group-hover:bg-blue-200 transition-colors"
                >
                  <span class="text-blue-600 text-2xl">🗺️</span>
                </div>
                <h2 class="text-xl font-semibold text-gray-800">
                  إدارة الرحلات
                </h2>
              </div>
              <p class="text-gray-600 mb-6 text-justify">
                تخطيط وتتبع رحلات النقل والتسليم مع إمكانية تحديد المسارات
                المثلى وتنبيهات التأخير
              </p>
              <Button
                variant="outline"
                class="w-full bg-blue-600 hover:bg-blue-700 py-3 text-lg font-medium transition-colors"
              >
                عرض الرحلات
              </Button>
            </div>
          </div>
        </RouterLink>

        <RouterLink
          to="/salesinvoice"
          class="transform transition-transform hover:-translate-y-1"
        >
          <div
            class="bg-white rounded-2xl shadow-sm overflow-hidden hover:shadow-lg transition-all duration-300 border-l-4 border-green-500 h-full group card-animation-delay-2"
          >
            <div class="p-7">
              <div class="flex items-center mb-5">
                <div
                  class="bg-green-100 p-3 rounded-full ml-4 group-hover:bg-green-200 transition-colors"
                >
                  <span class="text-green-600 text-2xl">💰</span>
                </div>
                <h2 class="text-xl font-semibold text-gray-800">
                  فواتير المبيعات
                </h2>
              </div>
              <p class="text-gray-600 mb-6 text-justify">
                إدارة الفواتير والحسابات المالية مع إمكانية التصدير والربط
                بالنظام المحاسبي
              </p>
              <Button
                variant="solid"
                class="w-full bg-green-600 hover:bg-green-700 py-3 text-lg font-medium transition-colors"
              >
                عرض الفواتير
              </Button>
            </div>
          </div>
        </RouterLink>

        <RouterLink
          to="/vehicle"
          class="transform transition-transform hover:-translate-y-1"
        >
          <div
            class="bg-white rounded-2xl shadow-sm overflow-hidden hover:shadow-lg transition-all duration-300 border-l-4 border-purple-500 h-full group card-animation-delay-3"
          >
            <div class="p-7">
              <div class="flex items-center mb-5">
                <div
                  class="bg-purple-100 p-3 rounded-full ml-4 group-hover:bg-purple-200 transition-colors"
                >
                  <span class="text-purple-600 text-2xl">🚗</span>
                </div>
                <h2 class="text-xl font-semibold text-gray-800">
                  إدارة المركبات
                </h2>
              </div>
              <p class="text-gray-600 mb-6 text-justify">
                إدارة بيانات المركبات وحالاتها مع تنبيهات الصيانة وتتبع استهلاك
                الوقود
              </p>
              <Button
                variant="solid"
                class="w-full bg-purple-600 hover:bg-purple-700 py-3 text-lg font-medium transition-colors"
              >
                عرض المركبات
              </Button>
            </div>
          </div>
        </RouterLink>

        <RouterLink
          to="/customer"
          class="transform transition-transform hover:-translate-y-1"
        >
          <div
            class="bg-white rounded-2xl shadow-sm overflow-hidden hover:shadow-lg transition-all duration-300 border-l-4 border-yellow-500 h-full group card-animation-delay-4"
          >
            <div class="p-7">
              <div class="flex items-center mb-5">
                <div
                  class="bg-yellow-100 p-3 rounded-full ml-4 group-hover:bg-yellow-200 transition-colors"
                >
                  <span class="text-yellow-600 text-2xl">👥</span>
                </div>
                <h2 class="text-xl font-semibold text-gray-800">
                  إدارة العملاء
                </h2>
              </div>
              <p class="text-gray-600 mb-6 text-justify">
                إدارة بيانات العملاء والعلاقات معهم مع تقارير الولاء وتتبع
                الطلبات السابقة
              </p>
              <Button
                variant="solid"
                class="w-full bg-yellow-600 hover:bg-yellow-700 py-3 text-lg font-medium transition-colors"
              >
                عرض العملاء
              </Button>
            </div>
          </div>
        </RouterLink>

        <RouterLink
          to="/address"
          class="transform transition-transform hover:-translate-y-1"
        >
          <div
            class="bg-white rounded-2xl shadow-sm overflow-hidden hover:shadow-lg transition-all duration-300 border-l-4 border-indigo-500 h-full group card-animation-delay-5"
          >
            <div class="p-7">
              <div class="flex items-center mb-5">
                <div
                  class="bg-indigo-100 p-3 rounded-full ml-4 group-hover:bg-indigo-200 transition-colors"
                >
                  <span class="text-indigo-600 text-2xl">📊</span>
                </div>
                <h2 class="text-xl font-semibold text-gray-800">العناوين</h2>
              </div>
              <p class="text-gray-600 mb-6 text-justify">
                إدارة عناوين العملاء مع خرائط تحديد الموقع وتصنيف المناطق
                الجغرافية
              </p>
              <Button
                variant="solid"
                class="w-full bg-indigo-600 hover:bg-indigo-700 py-3 text-lg font-medium transition-colors"
              >
                عرض العناوين
              </Button>
            </div>
          </div>
        </RouterLink>

        <RouterLink
          to="/driver"
          class="transform transition-transform hover:-translate-y-1"
        >
          <div
            class="bg-white rounded-2xl shadow-sm overflow-hidden hover:shadow-lg transition-all duration-300 border-l-4 border-cyan-500 h-full group card-animation-delay-6"
          >
            <div class="p-7">
              <div class="flex items-center mb-5">
                <div
                  class="bg-cyan-100 p-3 rounded-full ml-4 group-hover:bg-cyan-200 transition-colors"
                >
                  <span class="text-cyan-600 text-2xl">👤</span>
                </div>
                <h2 class="text-xl font-semibold text-gray-800">
                  إدارة السائقين
                </h2>
              </div>
              <p class="text-gray-600 mb-6 text-justify">
                إدارة بيانات السائقين وتوفرهم مع تقييم الأداء وتتبع ساعات العمل
              </p>
              <Button
                variant="solid"
                class="w-full bg-cyan-600 hover:bg-cyan-700 py-3 text-lg font-medium transition-colors"
              >
                عرض السائقين
              </Button>
            </div>
          </div>
        </RouterLink>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
        <div
          class="bg-white rounded-xl shadow-sm p-6 text-center hover:shadow-lg transition-all transform hover:-translate-y-1 border-t-4 border-blue-500 stats-animation-delay-1"
        >
          <div class="bg-blue-100 p-3 rounded-full inline-flex mb-4">
            <span class="text-blue-600 text-2xl">🚚</span>
          </div>
          <h3 class="text-lg font-medium text-gray-700 mb-2">الرحلات النشطة</h3>
          <p class="text-4xl font-bold text-blue-600 mb-1">
            {{ activeTripsCount }}
          </p>
          <p class="text-sm text-gray-500">+2 عن الأمس</p>
        </div>
        <div
          class="bg-white rounded-xl shadow-sm p-6 text-center hover:shadow-lg transition-all transform hover:-translate-y-1 border-t-4 border-green-500 stats-animation-delay-2"
        >
          <div class="bg-green-100 p-3 rounded-full inline-flex mb-4">
            <span class="text-green-600 text-2xl">🧾</span>
          </div>
          <h3 class="text-lg font-medium text-gray-700 mb-2">الفواتير اليوم</h3>
          <p class="text-4xl font-bold text-green-600 mb-1">
            {{ todayInvoicesCount }}
          </p>
          <p class="text-sm text-gray-500">قيمة 45,800 ر.س</p>
        </div>
        <div
          class="bg-white rounded-xl shadow-sm p-6 text-center hover:shadow-lg transition-all transform hover:-translate-y-1 border-t-4 border-purple-500 stats-animation-delay-3"
        >
          <div class="bg-purple-100 p-3 rounded-full inline-flex mb-4">
            <span class="text-purple-600 text-2xl">🚛</span>
          </div>
          <h3 class="text-lg font-medium text-gray-700 mb-2">
            المركبات المتاحة
          </h3>
          <p class="text-4xl font-bold text-purple-600 mb-1">
            {{ availableVehiclesCount }}
          </p>
          <p class="text-sm text-gray-500">3 تحت الصيانة</p>
        </div>
        <div
          class="bg-white rounded-xl shadow-sm p-6 text-center hover:shadow-lg transition-all transform hover:-translate-y-1 border-t-4 border-cyan-500 stats-animation-delay-4"
        >
          <div class="bg-cyan-100 p-3 rounded-full inline-flex mb-4">
            <span class="text-cyan-600 text-2xl">👨‍✈️</span>
          </div>
          <h3 class="text-lg font-medium text-gray-700 mb-2">
            السائقين النشطين
          </h3>
          <p class="text-4xl font-bold text-cyan-600 mb-1">
            {{ activeDriversCount }}
          </p>
          <p class="text-sm text-gray-500">5 في إجازة</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Button } from 'frappe-ui'
import { RouterLink } from 'vue-router'
import { frappe } from '@/plugins/frappe'

const activeTripsCount = ref(0)
const todayInvoicesCount = ref(0)
const availableVehiclesCount = ref(0)
const activeDriversCount = ref(0)
const call = frappe.call();
const fetchData = async () => {
  try {
    const data = await call.get('linklite.api.get_counts');
    console.log(data)
    if (data?.message) {
      activeTripsCount.value = data.message.active_trips_count
      todayInvoicesCount.value = data.message.today_invoices_count
      availableVehiclesCount.value = data.message.available_vehicles_count
      activeDriversCount.value = data.message.active_drivers_count
    }
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');

body,
* {
  font-family: 'Tajawal', sans-serif;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in-down {
  animation: fadeInDown 0.6s ease-out forwards;
}

@keyframes underline {
  from {
    width: 0%;
  }
  to {
    width: 100%;
  }
}
.animate-underline {
  animation: underline 0.8s ease-out forwards;
}

@keyframes pulseOnce {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}
.animate-pulse-once {
  animation: pulseOnce 1s ease-in-out;
}

@keyframes fadeInSlideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.card-animation-delay-1 {
  animation: fadeInSlideUp 0.6s ease-out 0.2s forwards;
  opacity: 0;
}
.card-animation-delay-2 {
  animation: fadeInSlideUp 0.6s ease-out 0.3s forwards;
  opacity: 0;
}
.card-animation-delay-3 {
  animation: fadeInSlideUp 0.6s ease-out 0.4s forwards;
  opacity: 0;
}
.card-animation-delay-4 {
  animation: fadeInSlideUp 0.6s ease-out 0.5s forwards;
  opacity: 0;
}
.card-animation-delay-5 {
  animation: fadeInSlideUp 0.6s ease-out 0.6s forwards;
  opacity: 0;
}
.card-animation-delay-6 {
  animation: fadeInSlideUp 0.6s ease-out 0.7s forwards;
  opacity: 0;
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
.stats-animation-delay-1 {
  animation: scaleIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) 0.8s forwards;
  opacity: 0;
}
.stats-animation-delay-2 {
  animation: scaleIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) 0.9s forwards;
  opacity: 0;
}
.stats-animation-delay-3 {
  animation: scaleIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) 1s forwards;
  opacity: 0;
}
.stats-animation-delay-4 {
  animation: scaleIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) 1.1s forwards;
  opacity: 0;
}

.group:hover h2 {
  color: theme('colors.blue.600');
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: theme('colors.gray.100');
}
::-webkit-scrollbar-thumb {
  background: theme('colors.blue.500');
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: theme('colors.blue.600');
}
</style>
