<template>
    <transition name="fade">
      <div
        v-if="record"
        class="fixed inset-0 z-50 flex items-center justify-center"
      >
        <!-- Backdrop -->
        <div
          class="absolute inset-0 bg-black bg-opacity-50"
          @click="$emit('close')"
        ></div>
  
        <!-- Modal -->
        <div
          class="relative bg-white rounded-lg shadow-lg w-full max-w-lg mx-4 p-6 overflow-y-auto z-10"
        >
          <!-- Header -->
          <div class="flex justify-between items-center mb-4 border-b pb-2">
            <h2 class="text-xl font-bold">{{ title }}</h2>
            <button
              @click="$emit('close')"
              class="text-gray-500 hover:text-gray-700 text-2xl leading-none"
            >
              ✕
            </button>
          </div>
  
          <!-- Content -->
          <div class="space-y-3 text-right">
            <div v-for="(value, key) in record" :key="key" class="mb-3">
              <p class="text-sm text-gray-500">{{ getLabel(key) }}</p>
              <p class="text-base font-medium">{{ value }}</p>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </template>
  
  <script setup>
  defineProps({
    record: { type: Object, default: null },
    title: { type: String, default: 'Details' },
    fields: { type: Array, default: null }, // optional mapping
  })
  
  /**
   * Map backend keys to Arabic labels (or use fields if passed)
   */
  const getLabel = (key) => {
    const labels = {
      name: 'الاسم',
      owner: 'المالك',
      creation: 'تاريخ الإنشاء',
      modified: 'آخر تعديل',
      modified_by: 'تم التعديل بواسطة',
      docstatus: 'حالة المستند',
      company: 'الشركة',
      email_notification_sent: 'تم إرسال إشعار عبر البريد الإلكتروني',
      driver: 'السائق',
      driver_name: 'اسم السائق',
      driver_email: 'بريد السائق الإلكتروني',
      driver_address: 'عنوان السائق',
      total_distance: 'المسافة الكلية',
      uom: 'الوحدة',
      vehicle: 'المركبة',
      departure_time: 'وقت المغادرة',
      employee: 'الموظف',
      status: 'الحالة',
    }
    return labels[key] || key
  }
  </script>
  
  <style>
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.3s ease;
  }
  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }
  </style>
  