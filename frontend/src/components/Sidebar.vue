<template>
  <transition name="slide">
    <div
      v-if="record"
      class="fixed left-0 top-0 w-96 h-full bg-white shadow-lg z-50 p-4 overflow-y-auto text-right"
    >
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold">{{ title }}</h2>
        <button
          @click="$emit('close')"
          class="text-gray-500 hover:text-gray-700"
        >
          ✕
        </button>
      </div>

      <div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">الاسم</p>
          <p class="text-base font-medium">{{ record.name }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">المالك</p>
          <p class="text-base font-medium">{{ record.owner }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">تاريخ الإنشاء</p>
          <p class="text-base font-medium">{{ record.creation }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">آخر تعديل</p>
          <p class="text-base font-medium">{{ record.modified }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">تم التعديل بواسطة</p>
          <p class="text-base font-medium">{{ record.modified_by }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">حالة المستند</p>
          <p class="text-base font-medium">{{ record.docstatus }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">الشركة</p>
          <p class="text-base font-medium">{{ record.company }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">
            تم إرسال إشعار عبر البريد الإلكتروني
          </p>
          <p class="text-base font-medium">
            {{ record.email_notification_sent }}
          </p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">السائق</p>
          <p class="text-base font-medium">{{ record.driver }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">اسم السائق</p>
          <p class="text-base font-medium">{{ record.driver_name }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">بريد السائق الإلكتروني</p>
          <p class="text-base font-medium">{{ record.driver_email }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">عنوان السائق</p>
          <p class="text-base font-medium">{{ record.driver_address }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">المسافة الكلية</p>
          <p class="text-base font-medium">{{ record.total_distance }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">الوحدة</p>
          <p class="text-base font-medium">{{ record.uom }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">المركبة</p>
          <p class="text-base font-medium">{{ record.vehicle }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">وقت المغادرة</p>
          <p class="text-base font-medium">{{ record.departure_time }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">الموظف</p>
          <p class="text-base font-medium">{{ record.employee }}</p>
        </div>
        <div class="mb-3">
          <p class="text-sm text-gray-500">الحالة</p>
          <p class="text-base font-medium">{{ record.status }}</p>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({
  record: { type: Object, default: null },
  title: { type: String, default: 'Details' },
  fields: { type: Array, default: null },
})
</script>

<style>
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}
</style>
