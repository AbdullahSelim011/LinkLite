<template>
  <div>
    <transition name="slide">
      <div
        v-if="visible && record"
        class="fixed top-0 left-0 h-full bg-white shadow-xl z-50 overflow-y-auto text-right sidebar-container"
        :class="{ 'sidebar-visible': visible }"
        :style="{ width: sidebarWidth }"
      >
        <!-- Header -->
        <div class="flex justify-between items-center p-4 border-b">
          <h2 class="text-xl font-bold">{{ title }}</h2>
          <button
            @click="$emit('close')"
            class="text-gray-500 hover:text-gray-700 text-lg"
          >
            ✕
          </button>
        </div>

        <!-- Content -->
        <div class="p-4">
          <!-- Lead ID -->
          <div class="mb-6 p-3 bg-gray-100 rounded-md">
            <p class="text-base font-mono font-bold">{{ title }}</p>
          </div>

          <!-- Details Section -->
          <div class="mb-6">
            <div class="flex items-center mb-3">
              <p class="text-sm text-gray-500">  رقم الفاتورة &nbsp;</p>
              <p class="text-base font-medium">{{ record.name }}</p>
            </div>
            
            <div class="grid grid-cols-1 gap-3">
              <div>
                <p class="text-sm text-gray-500">العميل</p>
                <p class="text-base font-medium">{{ record.customer }}</p>
              </div>
              
              <div>
                <p class="text-sm text-gray-500">التاريخ</p>
                <p class="text-base font-medium">{{ record.posting_date }}</p>
              </div>
              
              <div>
                <p class="text-sm text-gray-500">الإجمالي</p>
                <p class="text-base font-medium">{{ record.grand_total }}</p>
              </div>
              
              <div>
                <p class="text-sm text-gray-500">الحالة</p>
                <p class="text-base font-medium">{{ record.status }}</p>
              </div>
              
              <div>
                <p class="text-sm text-gray-500">طريقة الدفع</p>
                <p class="text-base font-medium">{{ record.mode_of_payment }}</p>
              </div>
              
              <div>
                <p class="text-sm text-gray-500">تم إنشاؤها بواسطة</p>
                <p class="text-base font-medium">{{ record.owner }}</p>
              </div>
              
              <div>
                <p class="text-sm text-gray-500">آخر تعديل</p>
                <p class="text-base font-medium">{{ record.modified }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  record: { type: Object, default: null },
  title: { type: String, default: "تفاصيل الفاتورة" },
  visible: { type: Boolean, default: false }
})

const sidebarWidth = computed(() => {
  return props.visible ? '400px' : '0'
})
</script>

<style scoped>
.sidebar-container {
  transition: width 0.3s ease;
}

/* Slide animation from the left */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}

/* Responsive design */
@media (max-width: 768px) {
  .sidebar-container {
    width: 85% !important;
  }
}
</style>