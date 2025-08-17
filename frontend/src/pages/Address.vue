<template>
  <div>
    <h2 class="font-bold text-ink-gray-8">إدارة العناوين</h2>

    <div class="flex justify-between items-center mb-4">
      <Button
        :label="showCreateForm ? 'إخفاء النموذج' : 'إضافة عنوان جديد'"
        :icon-left="showCreateForm ? 'x' : 'plus'"
        @click="showCreateForm = !showCreateForm"
      />

      <div class="relative w-72">
        <input
          v-model="searchQuery"
          type="text"
          class="w-full pr-4 pl-10 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="ابحث في العناوين..."
        />
        <button
          class="absolute left-0 top-0 h-full px-3 text-gray-500 hover:text-gray-700"
          @click="fetchAddresses"
        >
          <i class="fas fa-search"></i>
        </button>
      </div>
    </div>

    <div v-if="showCreateForm" class="bg-white rounded-lg shadow-md mb-4 p-6">
      <h3 class="text-lg font-semibold mb-4">إضافة عنوان جديد</h3>

      <form @submit.prevent="createAddress">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">اسم العنوان</label>
            <input
              v-model="newAddress.address_title"
              type="text"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
              placeholder="مثال: العنوان الرئيسي"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">نوع العنوان</label>
            <select
              v-model="newAddress.address_type"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="Billing">عنوان الفواتير</option>
              <option value="Shipping">عنوان الشحن</option>
              <option value="Office">عنوان المكتب</option>
              <option value="Personal">عنوان شخصي</option>
              <option value="Other">أخرى</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">الاسم</label>
            <input
              v-model="newAddress.name"
              type="text"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
              placeholder="الاسم الكامل"
            />
          </div>

          <div class="col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">السطر الأول للعنوان</label>
            <input
              v-model="newAddress.address_line1"
              type="text"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
              placeholder="الشارع، رقم المبنى"
            />
          </div>

          <div class="col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">السطر الثاني للعنوان (اختياري)</label>
            <input
              v-model="newAddress.address_line2"
              type="text"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="الحي، رقم الشقة"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">المدينة</label>
            <input
              v-model="newAddress.city"
              type="text"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">المنطقة/المحافظة</label>
            <input
              v-model="newAddress.state"
              type="text"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div class="col-span-2">
            <div class="flex justify-end space-x-2">
              <Button
                label="إعادة تعيين"
                appearance="secondary"
                @click="resetAddressForm"
              />
              <Button
                :label="isCreating ? 'جاري الإضافة...' : 'حفظ العنوان'"
                :icon-left="isCreating ? 'loader' : 'save'"
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
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">اسم العنوان</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">النوع</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الاسم</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">العنوان</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">المدينة</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">المنطقة</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الإجراءات</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="address in filteredAddresses" :key="address.name" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ address.address_title }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ getAddressTypeArabic(address.address_type) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ address.name }}</td>
              <td class="px-6 py-4 text-right">
                <div>{{ address.address_line1 }}</div>
                <div class="text-gray-500">{{ address.address_line2 }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ address.city }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ address.state }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex flex-wrap gap-2 justify-end">
                  <Button
                    label="تعديل"
                    icon-left="edit"
                    appearance="minimal"
                    @click="editAddress(address)"
                  />

                  <Button
                    label="حذف"
                    icon-left="trash-2"
                    appearance="minimal"
                    :loading="isDeleting"
                    @click="deleteAddress(address.name)"
                  />
                </div>
              </td>
            </tr>
            <tr v-if="filteredAddresses.length === 0 && !isLoading">
              <td colspan="7" class="px-6 py-4 text-center text-gray-500">
                لا توجد عناوين
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
      <h5 class="mt-3 text-gray-600">جاري تحميل العناوين...</h5>
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
import { createResource } from 'frappe-ui';

// البيانات
const addresses = ref([]);
const searchQuery = ref('');
const isLoading = ref(false);
const isCreating = ref(false);
const isDeleting = ref(false);
const error = ref(null);
const successMessage = ref('');
const showCreateForm = ref(false);
const isEditing = ref(false);
const currentEditId = ref(null);

const newAddress = reactive({
  name: '',
  address_title: '',
  address_type: 'Billing',
  address_line1: '',
  address_line2: '',
  city: '',
  state: ''
});

// دوال مساعدة
const getAddressTypeArabic = (type) => {
  const typeMap = {
    'Billing': 'عنوان الفواتير',
    'Shipping': 'عنوان الشحن',
    'Office': 'عنوان المكتب',
    'Personal': 'عنوان شخصي',
    'Other': 'أخرى'
  };
  return typeMap[type] || type;
};

const getArabicError = (err) => {
  if (err.includes('Not Found')) return 'البيانات المطلوبة غير موجودة.';
  if (err.includes('Permission Error')) return 'ليس لديك صلاحية للقيام بهذا الإجراء.';
  return typeof err === 'string' ? err : 'حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى.';
};

const getArabicSuccess = (msg) => {
  if (msg.includes('إنشاء')) return 'تم إنشاء العنوان بنجاح!';
  if (msg.includes('تحديث')) return 'تم تحديث العنوان بنجاح!';
  if (msg.includes('حذف')) return 'تم حذف العنوان بنجاح!';
  return 'تم الإجراء بنجاح!';
};

const resetAddressForm = () => {
  Object.assign(newAddress, {
    name: '',
    address_title: '',
    address_type: 'Billing',
    address_line1: '',
    address_line2: '',
    city: '',
    state: ''
  });
  isEditing.value = false;
  currentEditId.value = null;
};

// جلب العناوين
const fetchAddresses = () => {
  isLoading.value = true;
  const resource = createResource({
    url: 'frappe.client.get_list',
    params: {
      doctype: 'Address',
      fields: ["name", "address_title", "address_type", "name", "address_line1", "address_line2", "city", "state"],
      limit_page_length: 0
    },
    onSuccess(data) {
      addresses.value = data || [];
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isLoading.value = false;
  });
};

// إنشاء عنوان
const createAddress = () => {
  isCreating.value = true;
  
  const apiMethod = isEditing.value ? 'frappe.client.set_value' : 'frappe.client.insert';
  const params = isEditing.value ? {
    doctype: 'Address',
    name: currentEditId.value,
    fieldname: newAddress
  } : {
    doc: {
      doctype: 'Address',
      ...newAddress
    }
  };

  const resource = createResource({
    url: apiMethod,
    params: params,
    onSuccess(data) {
      resetAddressForm();
      fetchAddresses();
      showCreateForm.value = false;
      successMessage.value = isEditing.value ? 'تم تحديث العنوان بنجاح!' : 'تم إنشاء العنوان بنجاح!';
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isCreating.value = false;
  });
};

// تعديل عنوان
const editAddress = (address) => {
  isEditing.value = true;
  currentEditId.value = address.name;
  Object.assign(newAddress, {
    name: address.name,
    address_title: address.address_title,
    address_type: address.address_type,
    address_line1: address.address_line1,
    address_line2: address.address_line2,
    city: address.city,
    state: address.state
  });
  showCreateForm.value = true;
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

// حذف عنوان
const deleteAddress = (name) => {
  if (!confirm('هل تريد حذف هذا العنوان نهائياً؟')) return;
  
  isDeleting.value = true;
  const resource = createResource({
    url: 'frappe.client.delete',
    params: {
      doctype: 'Address',
      name: name
    },
    onSuccess() {
      successMessage.value = 'تم حذف العنوان بنجاح!';
      fetchAddresses();
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isDeleting.value = false;
  });
};

// الخصائص المحسوبة
const filteredAddresses = computed(() => {
  if (!searchQuery.value) return addresses.value;
  const query = searchQuery.value.toLowerCase();
  return addresses.value.filter(address => (
    (address.address_title && address.address_title.toLowerCase().includes(query)) ||
    (address.address_type && getAddressTypeArabic(address.address_type).toLowerCase().includes(query)) ||
    (address.name && address.name.toLowerCase().includes(query)) ||
    (address.address_line1 && address.address_line1.toLowerCase().includes(query)) ||
    (address.city && address.city.toLowerCase().includes(query)) ||
    (address.state && address.state.toLowerCase().includes(query))
  ));
});

// جلب البيانات الأولية عند تحميل المكون
onMounted(() => {
  fetchAddresses();
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
</style>