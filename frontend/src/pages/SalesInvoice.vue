<template>
  <div>
    <h2 class="font-bold text-ink-gray-8">فواتير المبيعات</h2>

    <div class="flex justify-between items-center mb-4">
      <Button
        :label="showCreateForm ? 'إخفاء النموذج' : 'إضافة فاتورة جديدة'"
        :icon-left="showCreateForm ? 'x' : 'plus'"
        @click="showCreateForm = !showCreateForm"
      />

      <div class="relative w-72">
        <input
          v-model="searchQuery"
          type="text"
          class="w-full pr-4 pl-10 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="ابحث في الفواتير..."
        />
        <button
          class="absolute left-0 top-0 h-full px-3 text-gray-500 hover:text-gray-700"
          @click="fetchInvoices"
        >
          <i class="fas fa-search"></i>
        </button>
      </div>
    </div>

    <div v-if="showCreateForm" class="bg-white rounded-lg shadow-md mb-4 p-6">
      <h3 class="text-lg font-semibold mb-4">إنشاء فاتورة جديدة</h3>

      <form @submit.prevent="createInvoice">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">العميل</label>
            <select
              v-model="newInvoice.customer"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="" disabled>اختر عميل</option>
              <option v-for="customer in customers" :key="customer.name" :value="customer.name">
                {{ customer.customer_name || customer.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">التاريخ</label>
            <input
              v-model="newInvoice.posting_date"
              type="date"
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div class="col-span-2">
            <h5 class="font-medium mb-2">المنتجات:</h5>
            <div v-for="(item, index) in newInvoice.items" :key="index" class="grid grid-cols-12 gap-3 mb-3">
              <div class="col-span-12 md:col-span-5">
                <label class="block text-sm font-medium text-gray-700 mb-1">المنتج</label>
                <select
                  v-model="item.item_code"
                  class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  @change="updateItemRate(index)"
                  required
                >
                  <option value="" disabled>اختر منتج</option>
                  <option v-for="product in items" :key="product.name" :value="product.name">
                    {{ product.item_name || product.name }} ({{ formatCurrency(product.standard_rate || 0) }})
                  </option>
                </select>
              </div>
              <div class="col-span-4 md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-1">الكمية</label>
                <input
                  v-model.number="item.qty"
                  type="number"
                  min="1"
                  class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div class="col-span-4 md:col-span-3">
                <label class="block text-sm font-medium text-gray-700 mb-1">السعر</label>
                <input
                  v-model.number="item.rate"
                  type="number"
                  min="0"
                  step="0.01"
                  class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div class="col-span-4 md:col-span-2 flex items-end">
                <Button
                  icon="trash-2"
                  appearance="minimal"
                  @click="removeItem(index)"
                />
              </div>
            </div>

            <Button
              label="إضافة منتج"
              icon-left="plus"
              appearance="minimal"
              @click="addItem"
            />
          </div>

          <div class="col-span-2">
            <div class="flex justify-between items-center">
              <div class="font-bold">
                الإجمالي: {{ formatCurrency(calculateTotal()) }}
              </div>
              <div class="flex space-x-2">
                <Button
                  label="إعادة تعيين"
                  appearance="secondary"
                  @click="resetInvoiceForm"
                />
                <Button
                  :label="isCreating ? 'جاري الإنشاء...' : 'إنشاء الفاتورة'"
                  :icon-left="isCreating ? 'loader' : 'plus'"
                  :loading="isCreating"
                  type="submit"
                />
              </div>
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
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">رقم الفاتورة</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">العميل</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">التاريخ</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">المبلغ</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الحالة</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الإجراءات</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="invoice in filteredInvoices" :key="invoice.name" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ invoice.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ getCustomerName(invoice.customer) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ formatDate(invoice.posting_date) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ formatCurrency(invoice.grand_total) }} {{ invoice.currency || 'USD' }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">
                <span :class="getStatusClass(invoice.status)">
                  {{ getStatusArabic(invoice.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex flex-wrap gap-2 justify-end">
                  <Button
                    label="عرض"
                    icon-left="eye"
                    appearance="minimal"
                    @click="fetchInvoiceDetails(invoice.name)"
                  />

                  <Button
                    v-if="invoice.status === 'Draft'"
                    label="ترحيل"
                    icon-left="check"
                    appearance="minimal"
                    :loading="isSubmitting"
                    @click="submitInvoice(invoice.name)"
                  />

                  <Button
                    v-if="invoice.docstatus === 1 && invoice.status !== 'Cancelled'"
                    label="إلغاء"
                    icon-left="ban"
                    appearance="minimal"
                    :loading="isCancelling"
                    @click="cancelInvoice(invoice.name)"
                  />

                  <Button
                    v-if="invoice.status === 'Draft' || invoice.status === 'Cancelled'"
                    label="حذف"
                    icon-left="trash-2"
                    appearance="minimal"
                    :loading="isDeleting"
                    @click="deleteInvoice(invoice.name)"
                  />

                  <Button
                    v-if="invoice.docstatus !== 2"
                    label="طباعة"
                    icon-left="printer"
                    appearance="minimal"
                    @click="printInvoice(invoice.name)"
                  />
                </div>
              </td>
            </tr>
            <tr v-if="filteredInvoices.length === 0 && !isLoading">
              <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                لا توجد فواتير
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
      <h5 class="mt-3 text-gray-600">جاري تحميل الفواتير...</h5>
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
  <Sidebar2
    v-if="showInvoiceSidebar"
    :record="selectedInvoice"
    title="تفاصيل الفاتورة"
    :visible="showInvoiceSidebar"
    @close="showInvoiceSidebar = false"
  />


</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { createResource } from 'frappe-ui';
import Sidebar2 from "@/components/Sidebar2.vue"
// البيانات
const invoices = ref([]);
const customers = ref([]);
const items = ref([]);
const searchQuery = ref('');
const isLoading = ref(false);
const isCreating = ref(false);
const isSubmitting = ref(false);
const isCancelling = ref(false);
const isDeleting = ref(false);
const error = ref(null);
const successMessage = ref('');
const showCreateForm = ref(false);
// state for sidebar
const selectedInvoice = ref(null)
const showInvoiceSidebar = ref(false)

const newInvoice = reactive({
  customer: "",
  posting_date: new Date().toISOString().split('T')[0],
  items: [{ item_code: "", qty: 1, rate: 0 }]
});

// دوال مساعدة
const getStatusArabic = (status) => {
  const statusMap = {
    'Draft': 'مسودة',
    'Submitted': 'مرحّلة',
    'Paid': 'مدفوعة',
    'Unpaid': 'غير مدفوعة',
    'Overdue': 'متأخرة',
    'Cancelled': 'ملغاة'
  };
  return statusMap[status] || status;
};

const getArabicError = (err) => {
  if (err.includes('Not Found')) return 'البيانات المطلوبة غير موجودة.';
  if (err.includes('Permission Error')) return 'ليس لديك صلاحية للقيام بهذا الإجراء.';
  return typeof err === 'string' ? err : 'حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى.';
};

const getArabicSuccess = (msg) => {
  if (msg.includes('إنشاء')) return 'تم إنشاء الفاتورة بنجاح!';
  if (msg.includes('ترحيل')) return 'تم ترحيل الفاتورة بنجاح!';
  if (msg.includes('إلغاء')) return 'تم إلغاء الفاتورة بنجاح!';
  if (msg.includes('حذف')) return 'تم حذف الفاتورة بنجاح!';
  return 'تم الإجراء بنجاح!';
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ar-SA', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
};

const formatCurrency = (amount) => {
  return isNaN(amount) ? '٠٫٠٠ ر.س' : 
    new Intl.NumberFormat('ar-SA', { 
      style: 'currency', 
      currency: 'SAR' 
    }).format(amount);
};

const getStatusClass = (status) => {
  const statusClasses = {
    'Draft': 'bg-gray-200 text-gray-800 px-2 py-1 rounded-full text-xs',
    'Submitted': 'bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs',
    'Paid': 'bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs',
    'Unpaid': 'bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs',
    'Overdue': 'bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs',
    'Cancelled': 'bg-gray-800 text-white px-2 py-1 rounded-full text-xs'
  };
  return statusClasses[status] || 'bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs';
};

const getCustomerName = (customerId) => {
  const customer = customers.value.find(c => c.name === customerId);
  return customer ? (customer.customer_name || customer.name) : customerId;
};

const updateItemRate = (index) => {
  const selectedItem = items.value.find(item => item.name === newInvoice.items[index].item_code);
  if (selectedItem && selectedItem.standard_rate) {
    newInvoice.items[index].rate = selectedItem.standard_rate;
  }
};

const calculateTotal = () => {
  return newInvoice.items.reduce((total, item) => {
    return total + (item.qty * item.rate);
  }, 0);
};

const resetInvoiceForm = () => {
  Object.assign(newInvoice, {
    customer: "",
    posting_date: new Date().toISOString().split('T')[0],
    items: [{ item_code: "", qty: 1, rate: 0 }]
  });
};

const addItem = () => {
  newInvoice.items.push({ item_code: "", qty: 1, rate: 0 });
};

const removeItem = (index) => {
  if (newInvoice.items.length > 1) {
    newInvoice.items.splice(index, 1);
  }
};

// جلب الفواتير
const fetchInvoices = () => {
  isLoading.value = true;
  const resource = createResource({
    url: 'linklite.api.get_salesInvoice',
    params: {
      doctype: 'Sales Invoice',
      fields: ["name", "customer", "posting_date", "grand_total", "status", "currency", "docstatus"],
      limit_page_length: 0
    },
    onSuccess(data) {
      invoices.value = data || [];
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isLoading.value = false;
  });
};

// جلب العملاء
const fetchCustomers = () => {
  const resource = createResource({
    url: 'frappe.client.get_list',
    params: {
      doctype: 'Customer',
      fields: ["name", "customer_name"],
      limit_page_length: 0
    },
    onSuccess(data) {
      customers.value = data || [];
    },
    onError(err) {
      console.error("Failed to fetch customers:", err.message);
    }
  });
  resource.fetch();
};

// جلب المنتجات
const fetchItems = () => {
  const resource = createResource({
    url: 'frappe.client.get_list',
    params: {
      doctype: 'Item',
      fields: ["name", "item_name", "standard_rate"],
      limit_page_length: 0
    },
    onSuccess(data) {
      items.value = data || [];
    },
    onError(err) {
      console.error("Failed to fetch items:", err.message);
    }
  });
  resource.fetch();
};

// إنشاء فاتورة
const createInvoice = () => {
  isCreating.value = true;
  const resource = createResource({
    url: 'linklite.api.create_sales_invoice_custom', 
    params: {
      // تأكد أن هذه الحقول موجودة
      customer: newInvoice.customer,
      items: newInvoice.items.map(item => ({
          item_code: item.item_code,
          qty: item.qty,
          rate: item.rate
      }))
    },
    onSuccess() {
      resetInvoiceForm();
      fetchInvoices();
      showCreateForm.value = false;
      successMessage.value = 'تم إنشاء الفاتورة بنجاح!';
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isCreating.value = false;
  });
};

// ترحيل الفاتورة
const submitInvoice = (name) => {
  if (!confirm('هل تريد ترحيل هذه الفاتورة؟')) return;
  
  isSubmitting.value = true;
  const resource = createResource({
    url: 'linklite.api.submit_sales_invoice',
    params: {
      doctype: 'Sales Invoice',
      name: name
    },
    onSuccess() {
      successMessage.value = 'تم ترحيل الفاتورة بنجاح!';
      fetchInvoices();
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isSubmitting.value = false;
  });
};

// إلغاء الفاتورة
const cancelInvoice = (name) => {
  if (!confirm('هل تريد إلغاء هذه الفاتورة؟')) return;
  
  isCancelling.value = true;
  const resource = createResource({
    url: 'linklite.api.cancel_sales_invoice',
    params: {
      doctype: 'Sales Invoice',
      name: name
    },
    onSuccess() {
      successMessage.value = 'تم إلغاء الفاتورة بنجاح!';
      fetchInvoices();
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isCancelling.value = false;
  });
};

// حذف الفاتورة
const deleteInvoice = (name) => {
  if (!confirm('هل تريد حذف هذه الفاتورة نهائياً؟')) return;
  
  isDeleting.value = true;
  const resource = createResource({
    url: 'linklite.api.delete_sales_invoice',
    params: {
      doctype: 'Sales Invoice',
      name: name
    },
    onSuccess() {
      successMessage.value = 'تم حذف الفاتورة بنجاح!';
      fetchInvoices();
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isDeleting.value = false;
  });
};

// عرض الفاتورة
const viewInvoice = (name) => {
  window.open(`/app/sales-invoice/${name}`, '_blank');
};

// طباعة الفاتورة
const printInvoice = (name) => {
  window.open(`/printview?doctype=Sales%20Invoice&name=${name}&format=Standard`, '_blank');
};

// الخصائص المحسوبة
const filteredInvoices = computed(() => {
  if (!searchQuery.value) return invoices.value;
  const query = searchQuery.value.toLowerCase();
  return invoices.value.filter(invoice => (
    (invoice.name && invoice.name.toLowerCase().includes(query)) ||
    (invoice.customer && getCustomerName(invoice.customer).toLowerCase().includes(query)) ||
    (invoice.posting_date && formatDate(invoice.posting_date).toLowerCase().includes(query)) ||
    (invoice.status && getStatusArabic(invoice.status).toLowerCase().includes(query))
  ));
});

// جلب البيانات الأولية عند تحميل المكون
onMounted(() => {
  fetchInvoices();
  fetchCustomers();
  fetchItems();
});

function fetchInvoiceDetails(invoiceName) {


  const resource = createResource({
    url: "frappe.client.get",
    params: {
      doctype: "Sales Invoice",
      name: invoiceName,
    },
    onSuccess(data) {
      selectedInvoice.value = data
      showInvoiceSidebar.value = true
    },
    onError(err) {
      console.error("❌ Error fetching invoice:", err)
    },
  })

  resource.fetch()
}

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