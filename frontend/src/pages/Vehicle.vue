<template>
  <div>
    <h2 class="font-bold text-ink-gray-8">إدارة المركبات</h2>

    <div class="flex justify-between items-center mb-4">
      <Button
        :label="showCreateForm ? 'إخفاء النموذج' : 'إضافة مركبة جديدة'"
        :icon-left="showCreateForm ? 'x' : 'plus'"
        @click="showCreateForm = !showCreateForm"
      />

      <div class="relative w-72">
        <input
          v-model="searchQuery"
          type="text"
          class="w-full pr-4 pl-10 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="ابحث في المركبات..."
        />
        <button
          class="absolute left-0 top-0 h-full px-3 text-gray-500 hover:text-gray-700"
          @click="fetchVehicles"
        >
          <i class="fas fa-search"></i>
        </button>
      </div>
    </div>

    <div v-if="showCreateForm" class="bg-white rounded-lg shadow-md mb-4 p-6">
      <h3 class="text-lg font-semibold mb-4">إضافة مركبة جديدة</h3>

      <form @submit.prevent="createVehicle">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">الصانع</label>
            <input
              v-model="newVehicle.make"
              type="text"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">الموديل</label>
            <input
              v-model="newVehicle.model"
              type="text"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">رقم اللوحة</label>
            <input
              v-model="newVehicle.license_plate"
              type="text"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">آخر قراءة للعداد (كم)</label>
            <input
              v-model.number="newVehicle.last_odometer"
              type="number"
              min="0"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">نوع الوقود</label>
            <select
              v-model="newVehicle.fuel_type"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="" disabled>اختر نوع الوقود</option>
              <option
                v-for="option in fuelOptions"
                :key="option"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">وحدة القياس</label>
            <select
              v-model="newVehicle.uom"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="" disabled>اختر وحدة القياس</option>
              <option
                v-for="option in uomOptions"
                :key="option"
                :value="option"
              >
                {{ option }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">عدد العجلات</label>
            <input
              v-model.number="newVehicle.wheels"
              type="number"
              min="2"
              max="18"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div class="col-span-2">
            <div class="flex justify-end space-x-2">
              <Button
                label="إعادة تعيين"
                appearance="secondary"
                @click="resetVehicleForm"
              />
              <Button
                :label="isCreating ? 'جاري الإنشاء...' : 'إضافة المركبة'"
                :icon-left="isCreating ? 'loader' : 'plus'"
                :loading="isCreating"
                type="submit"
              />
            </div>
          </div>
        </div>
      </form>
    </div>

    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">رقم المركبة</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الصانع</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الموديل</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">لوحة المركبة</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">آخر قراءة للعداد</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">نوع الوقود</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">وحدة القياس</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الإجراءات</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="vehicle in filteredVehicles" :key="vehicle.name" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ vehicle.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ vehicle.make }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ vehicle.model }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ vehicle.license_plate }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ formatNumber(vehicle.last_odometer) }} كم</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ vehicle.fuel_type }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ vehicle.uom }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex flex-wrap gap-2 justify-end">
                  <!-- <Button
                    label="عرض"
                    icon-left="eye"
                    appearance="minimal"
                    @click="viewVehicle(vehicle.name)"
                  />

                  <Button
                    label="تعديل"
                    icon-left="edit"
                    appearance="minimal"
                    :disabled="vehicle.docstatus !== 0"
                    @click="editVehicle(vehicle.name)"
                  /> -->

                  <Button
                    label="حذف"
                    icon-left="trash-2"
                    appearance="minimal"
                    :loading="isDeleting"
                    @click="deleteVehicle(vehicle.name)"
                  />

                  <Button
                    label="طباعة"
                    icon-left="printer"
                    appearance="minimal"
                    @click="printVehicle(vehicle.name)"
                  />
                </div>
              </td>
            </tr>
            <tr v-if="filteredVehicles.length === 0 && !isLoading">
              <td colspan="8" class="px-6 py-4 text-center text-gray-500">
                لا توجد مركبات مسجلة
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="isLoading" class="text-center my-8 py-8">
      <div
        class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"
      ></div>
      <h5 class="mt-3 text-gray-600">جاري تحميل بيانات المركبات...</h5>
    </div>

    <div
      v-if="error"
      class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mt-4 rounded"
    >
      <div class="flex justify-between items-center">
        <div class="flex items-center">
          <i class="fas fa-exclamation-triangle ml-2"></i>
          <strong>خطأ!</strong> {{ getArabicError(error) }}
        </div>
        <button type="button" class="text-red-700" @click="error = null">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>

    <div
      v-if="successMessage"
      class="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mt-4 rounded"
    >
      <div class="flex justify-between items-center">
        <div class="flex items-center">
          <i class="fas fa-check-circle ml-2"></i>
          {{ getArabicSuccess(successMessage) }}
        </div>
        <button type="button" class="text-green-700" @click="successMessage = ''">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { createResource, frappe } from 'frappe-ui';

// البيانات
const vehicles = ref([]);
const searchQuery = ref('');
const isLoading = ref(false);
const isCreating = ref(false);
const isDeleting = ref(false);
const error = ref(null);
const successMessage = ref('');
const showCreateForm = ref(false);

// خيارات ثابتة لنوع الوقود
const fuelOptions = ref(['Petrol', 'Diesel', 'Electric', 'Natural Gas']);

// خيارات ثابتة لوحدة القياس
const uomOptions = ref(['Box', 'Unit', 'Nos', 'Pair', 'Set']);

const newVehicle = reactive({
  make: "",
  model: "",
  license_plate: "",
  last_odometer: 0,
  fuel_type: "",
  uom: "",
  wheels: 4,
  color: ""
});

// دوال مساعدة
const getArabicError = (err) => {
  if (err.includes('Not Found')) return 'البيانات المطلوبة غير موجودة.';
  if (err.includes('Permission Error')) return 'ليس لديك صلاحية للقيام بهذا الإجراء.';
  return typeof err === 'string' ? err : 'حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى.';
};

const getArabicSuccess = (msg) => {
  if (msg.includes('إضافة')) return 'تم إضافة المركبة بنجاح!';
  if (msg.includes('حذف')) return 'تم حذف المركبة بنجاح!';
  if (msg.includes('تحديث')) return 'تم تحديث بيانات المركبة بنجاح!';
  return 'تم الإجراء بنجاح!';
};

const formatNumber = (num) => {
  return isNaN(num) ? '٠' : new Intl.NumberFormat('ar-SA').format(num);
};

const resetVehicleForm = () => {
  Object.assign(newVehicle, {
    make: "",
    model: "",
    license_plate: "",
    last_odometer: 0,
    fuel_type: "",
    uom: "",
    wheels: 4,
    color: ""
  });
};

// دالة جلب خيارات UOM من الخادم لم تعد ضرورية
// const fetchUOMOptions = async () => { ... };


// جلب المركبات
const fetchVehicles = () => {
  isLoading.value = true;
  const resource = createResource({
    url: 'frappe.client.get_list',
    params: {
      doctype: 'Vehicle',
      fields: ["name", "make", "model", "license_plate", "last_odometer", "fuel_type", "uom", "wheels", "color", "docstatus"],
      limit_page_length: 0
    },
    onSuccess(data) {
      vehicles.value = data || [];
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isLoading.value = false;
  });
};

// دالة إنشاء المركبة
const createVehicle = () => {
  isCreating.value = true;
  const resource = createResource({
    url: 'linklite.api.create_vehicle_custom',
    params: {
      license_plate: newVehicle.license_plate,
      make: newVehicle.make,
      model: newVehicle.model,
      last_odometer: newVehicle.last_odometer,
      fuel_type: newVehicle.fuel_type,
      uom: newVehicle.uom,
      color: newVehicle.color
    },
    onSuccess() {
      resetVehicleForm();
      fetchVehicles();
      showCreateForm.value = false;
      successMessage.value = 'تم إضافة المركبة بنجاح!';
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isCreating.value = false;
  });
};

// حذف مركبة
const deleteVehicle = (name) => {
  if (!confirm('هل أنت متأكد أنك تريد حذف هذه المركبة؟')) return;

  isDeleting.value = true;
  const resource = createResource({
    url: 'frappe.client.delete',
    params: {
      doctype: 'Vehicle',
      name: name
    },
    onSuccess() {
      successMessage.value = 'تم حذف المركبة بنجاح!';
      fetchVehicles();
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isDeleting.value = false;
  });
};

// عرض المركبة
const viewVehicle = (name) => {
  window.open(`/app/vehicle/${name}`, '_blank');
};

// تعديل المركبة
const editVehicle = (name) => {
  const vehicle = vehicles.value.find(v => v.name === name);
  if (vehicle.docstatus !== 0) {
    error.value = 'يمكن تعديل المركبات المسودة فقط!';
    return;
  }
  window.open(`/app/vehicle/${name}`, '_blank');
};

// طباعة المركبة
const printVehicle = (name) => {
  window.open(`/printview?doctype=Vehicle&name=${name}&format=Standard`, '_blank');
};

// الخصائص المحسوبة
const filteredVehicles = computed(() => {
  if (!searchQuery.value) return vehicles.value;
  const query = searchQuery.value.toLowerCase();
  return vehicles.value.filter(vehicle => (
    (vehicle.name && vehicle.name.toLowerCase().includes(query)) ||
    (vehicle.make && vehicle.make.toLowerCase().includes(query)) ||
    (vehicle.model && vehicle.model.toLowerCase().includes(query)) ||
    (vehicle.license_plate && vehicle.license_plate.toLowerCase().includes(query))
  ));
});

// جلب البيانات الأولية عند تحميل المكون
onMounted(() => {
  fetchVehicles();
  // لم يعد هناك حاجة لاستدعاء دالة جلب وحدات القياس من الخادم
});
</script>

<style scoped>
/* Arabic font and RTL support */
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');

body,
* {
  font-family: 'Tajawal', sans-serif;
}

/* RTL table adjustments */
table {
  direction: rtl;
}

th,
td {
  text-align: right;
}

/* Loading spinner animation */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Responsive table */
@media (max-width: 768px) {
  table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }
}

/* Arabic datepicker styles */
input[type="date"] {
  direction: ltr;
  text-align: right;
}

input[type="date"]::-webkit-calendar-picker-indicator {
  filter: invert(0.5);
}
</style>