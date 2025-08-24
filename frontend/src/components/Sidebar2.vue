<template>
  <transition name="slide">
    <div
      v-if="visible && record"
      class="fixed top-0 left-0 w-96 h-full bg-white shadow-xl z-50 p-4 overflow-y-auto text-right"
    >
      <!-- Header -->
      <div class="flex justify-between items-center mb-4 border-b pb-2">
        <h2 class="text-xl font-bold">{{ title }}</h2>
        <button
          @click="$emit('close')"
          class="text-gray-500 hover:text-gray-700"
        >
          ✕
        </button>
      </div>

      <!-- Content -->
      <div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">رقم الفاتورة</p>
          <p class="text-base font-medium">{{ record.name }}</p>
        </div>

        <div class="mb-3">
          <p class="text-sm text-gray-500">العميل</p>
          <p class="text-base font-medium">{{ record.customer }}</p>
        </div>

        <div class="mb-3">
          <p class="text-sm text-gray-500">التاريخ</p>
          <p class="text-base font-medium">{{ record.posting_date }}</p>
        </div>

        <div class="mb-3">
          <p class="text-sm text-gray-500">الإجمالي</p>
          <p class="text-base font-medium">{{ record.grand_total }}</p>
        </div>

        <div class="mb-3">
          <p class="text-sm text-gray-500">الحالة</p>
          <p class="text-base font-medium">{{ record.status }}</p>
        </div>

        <div class="mb-3">
          <p class="text-sm text-gray-500">طريقة الدفع</p>
          <p class="text-base font-medium">{{ record.mode_of_payment }}</p>
        </div>

        <div class="mb-3">
          <p class="text-sm text-gray-500">تم إنشاؤها بواسطة</p>
          <p class="text-base font-medium">{{ record.owner }}</p>
        </div>

        <div class="mb-3">
          <p class="text-sm text-gray-500">آخر تعديل</p>
          <p class="text-base font-medium">{{ record.modified }}</p>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({
  record: { type: Object, default: null },
  title: { type: String, default: "تفاصيل الفاتورة" },
  visible: { type: Boolean, default: true }
})
</script>

<style>
/* Slide animation from the left */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}
</style>

