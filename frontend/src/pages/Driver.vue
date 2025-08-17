<template>
  <div>
    <h2 class="font-bold text-ink-gray-8">إدارة السائقين</h2>

    <div class="flex justify-between items-center mb-4">
      <Button
        :label="showCreateForm ? 'إخفاء النموذج' : 'إضافة سائق جديد'"
        :icon-left="showCreateForm ? 'x' : 'plus'"
        @click="showCreateForm = !showCreateForm"
      />

      <div class="relative w-72">
        <input
          v-model="searchQuery"
          type="text"
          class="w-full pr-4 pl-10 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="ابحث في السائقين..."
        />
        <button
          class="absolute left-0 top-0 h-full px-3 text-gray-500 hover:text-gray-700"
          @click="fetchDrivers"
        >
          <i class="fas fa-search"></i>
        </button>
      </div>
    </div>

    <div v-if="showCreateForm" class="bg-white rounded-lg shadow-md mb-4 p-6">
      <h3 class="text-lg font-semibold mb-4">إضافة سائق جديد</h3>

      <form @submit.prevent="createDriver">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">الاسم الكامل</label>
            <input
              v-model="newDriver.full_name"
              type="text"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">حالة السائق</label>
            <select
              v-model="newDriver.status"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="" disabled>اختر الحالة</option>
              <option value="Active">نشط</option>
              <option value="Inactive">غير نشط</option>
              <option value="Suspended">موقوف</option>
            </select>
          </div>

          <div class="col-span-2 flex justify-end space-x-2">
            <Button label="إعادة تعيين" appearance="secondary" @click="resetDriverForm" />
            <Button
              :label="isCreating ? 'جاري الإضافة...' : 'إضافة السائق'"
              :icon-left="isCreating ? 'loader' : 'plus'"
              :loading="isCreating"
              type="submit"
            />
          </div>
        </div>
      </form>
    </div>

    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                رقم السائق
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                الاسم الكامل
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                رقم الرخصة
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                رقم الجوال
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                الحالة
              </th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                الإجراءات
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="driver in filteredDrivers" :key="driver.name" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ driver.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ driver.full_name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ driver.license_number }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ driver.cell_number }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">
                <span :class="getStatusClass(driver.status)">
                  {{ getStatusArabic(driver.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex flex-wrap gap-2 justify-end">
                  <!-- <Button
                    label="تعديل"
                    icon-left="edit"
                    appearance="minimal"
                    @click="editDriver(driver)"
                  /> -->
                  <Button
                    label="حذف"
                    icon-left="trash-2"
                    appearance="minimal"
                    :loading="isDeleting"
                    @click="deleteDriver(driver)"
                  />
                </div>
              </td>
            </tr>
            <tr v-if="filteredDrivers.length === 0 && !isLoading">
              <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                لا يوجد سائقون لعرضهم
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
      <h5 class="mt-3 text-gray-600">جاري تحميل السائقين...</h5>
    </div>

    <div
      v-if="successMessage"
      class="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mt-4 rounded"
    >
      <div class="flex justify-between items-center">
        <div class="flex items-center">
          <i class="fas fa-check-circle ml-2"></i>
          {{ successMessage }}
        </div>
        <button type="button" class="text-green-700" @click="successMessage = ''">
          <i class="fas fa-times"></i>
        </button>
      </div>
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
  </div>
</template>

<script setup>
import { createResource } from 'frappe-ui';
import { ref, reactive, computed, onMounted } from 'vue';

const drivers = ref([]);
const searchQuery = ref('');
const isLoading = ref(false);
const isCreating = ref(false);
const isDeleting = ref(false);
const error = ref(null);
const successMessage = ref('');
const showCreateForm = ref(false);

const newDriver = reactive({
  full_name: "",
  status: "",
  license_number: "",
  cell_number: "",
  address: ""
});

// Helper functions
const getStatusArabic = (status) => {
  const statusMap = {
    'Active': 'نشط',
    'Inactive': 'غير نشط',
    'Suspended': 'موقوف',
    '': '--'
  };
  return statusMap[status] || status;
};

const resetDriverForm = () => {
  Object.assign(newDriver, {
    full_name: "",
    status: "",
    license_number: "",
    cell_number: "",
    address: ""
  });
};

const getArabicError = (err) => {
  if (err.includes('Not Found')) return 'البيانات المطلوبة غير موجودة.';
  if (err.includes('Permission Error')) return 'ليس لديك صلاحية للقيام بهذا الإجراء.';
  return typeof err === 'string' ? err : 'حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى.';
};

// Fetch drivers
const fetchDrivers = () => {
  isLoading.value = true;
  const resource = createResource({
    url: 'frappe.client.get_list',
    params: {
      doctype: 'Driver',
      fields: ["name", "full_name", "status", "license_number", "cell_number", "address"],
      limit_page_length: 0
    },
    onSuccess(data) {
      drivers.value = data || [];
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isLoading.value = false;
  });
};

// Create driver
const createDriver = () => {
  isCreating.value = true;
  const resource = createResource({
    url: 'linklite.api.create_driver_custom',
    params: {
      full_name: newDriver.full_name,
      status: newDriver.status
    },
    onSuccess(data) {
      successMessage.value = data.message;
      resetDriverForm();
      fetchDrivers();
      showCreateForm.value = false;
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isCreating.value = false;
  });
};

// Delete driver
const deleteDriver = (driver) => {
  if (!confirm(`هل أنت متأكد أنك تريد حذف السائق ${driver.full_name}؟`)) {
    return;
  }

  isDeleting.value = true;
  const resource = createResource({
    url: 'linklite.api.delete_driver',
    params: {
      name: driver.name,
      full_name: driver.full_name,
      status: driver.status
    },
    onSuccess() {
      successMessage.value = `تم حذف السائق ${driver.full_name} بنجاح!`;
      fetchDrivers();
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isDeleting.value = false;
  });
};

const viewDriver = (driver) => {
  console.log('View driver:', driver);
};

const editDriver = (driver) => {
  console.log('Edit driver:', driver);
};

// Computed properties
const filteredDrivers = computed(() => {
  if (!searchQuery.value) return drivers.value;
  const query = searchQuery.value.toLowerCase();
  return drivers.value.filter(driver => (
    (driver.full_name && driver.full_name.toLowerCase().includes(query)) ||
    (driver.name && driver.name.toLowerCase().includes(query)) ||
    (driver.license_number && driver.license_number.toLowerCase().includes(query)) ||
    (driver.cell_number && driver.cell_number.toLowerCase().includes(query)) ||
    (driver.status && getStatusArabic(driver.status).toLowerCase().includes(query))
  ));
});

const getStatusClass = (status) => {
  const statusClasses = {
    'Active': 'bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs',
    'Inactive': 'bg-gray-200 text-gray-800 px-2 py-1 rounded-full text-xs',
    'Suspended': 'bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs'
  };
  return statusClasses[status] || 'bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs';
};

// Initial fetch
onMounted(fetchDrivers);
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

/* Status badge styles */
.bg-green-100,
.bg-gray-200,
.bg-blue-100,
.bg-red-100 {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}
</style>