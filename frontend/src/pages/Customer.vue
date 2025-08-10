<template>
    <div class="p-4">
      <h1 class="text-2xl font-bold mb-4">إدارة العملاء</h1>
  
      <div v-if="successMessage" class="p-2 mb-4 bg-green-100 text-green-700 rounded">
        {{ successMessage }}
      </div>
  
      <div v-if="error" class="p-2 mb-4 bg-red-100 text-red-700 rounded">
        {{ error }}
      </div>
  
      <div class="flex justify-between mb-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="بحث عن العملاء..."
          class="border rounded px-2 py-1 w-full max-w-md"
        />
  
        <button 
          @click="showCreateForm = !showCreateForm" 
          class="bg-blue-600 text-white px-4 py-2 rounded"
        >
          {{ showCreateForm ? 'إغلاق النموذج' : 'إضافة عميل جديد' }}
        </button>
      </div>
  
      <div v-if="showCreateForm" class="mb-4 border p-4 rounded bg-gray-50">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block mb-2">اسم العميل:</label>
            <input 
              v-model="newCustomer.customer_name" 
              type="text" 
              class="border rounded px-2 py-1 w-full mb-2" 
              required
            />
          </div>
  
          <div>
            <label class="block mb-2">نوع العميل:</label>
            <select 
              v-model="newCustomer.customer_type" 
              class="border rounded px-2 py-1 w-full mb-2"
              required
            >
              <option value="" disabled>اختر نوع العميل</option>
              <option value="Company">شركة</option>
              <option value="Individual">فرد</option>
            </select>
          </div>
  
          <div>
            <label class="block mb-2">العنوان:</label>
            <input 
              v-model="newCustomer.customer_primary_address" 
              type="text" 
              class="border rounded px-2 py-1 w-full mb-2"
            />
          </div>
  
          <div>
            <label class="block mb-2">الرقم الضريبي:</label>
            <input 
              v-model="newCustomer.tax_id" 
              type="text" 
              class="border rounded px-2 py-1 w-full mb-2"
            />
          </div>
        </div>
  
        <div class="flex justify-end mt-4 space-x-2">
          <button 
            @click="resetCustomerForm" 
            class="bg-gray-200 text-gray-800 px-4 py-2 rounded"
          >
            إعادة تعيين
          </button>
          <button 
            @click="createCustomer" 
            :disabled="isCreating"
            class="bg-green-600 text-white px-4 py-2 rounded"
          >
            {{ isCreating ? 'جاري الحفظ...' : 'حفظ العميل' }}
          </button>
        </div>
      </div>
  
      <table class="w-full border">
        <thead>
          <tr class="bg-gray-200">
            <th class="p-2 border text-right">اسم العميل</th>
            <th class="p-2 border text-right">نوع العميل</th>
            <th class="p-2 border text-right">العنوان</th>
            <th class="p-2 border text-right">الرقم الضريبي</th>
            <th class="p-2 border text-right">إجراءات</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="customer in filteredCustomers" :key="customer.name">
            <td class="p-2 border">{{ customer.customer_name || customer.name }}</td>
            <td class="p-2 border">{{ getCustomerTypeArabic(customer.customer_type) }}</td>
            <td class="p-2 border">{{ customer.customer_primary_address || '--' }}</td>
            <td class="p-2 border">{{ customer.tax_id || '--' }}</td>
            <td class="p-2 border">
              <div class="flex gap-2 justify-end">
                <button 
                  @click="viewCustomer(customer.name)" 
                  class="bg-blue-100 text-blue-800 px-2 py-1 rounded"
                >
                  عرض
                </button>
                <button 
                  @click="editCustomer(customer.name)" 
                  class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded"
                >
                  تعديل
                </button>
                <button 
                  @click="deleteCustomer(customer.name)" 
                  :disabled="isDeleting"
                  class="bg-red-100 text-red-800 px-2 py-1 rounded"
                >
                  {{ isDeleting ? 'جاري الحذف...' : 'حذف' }}
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredCustomers.length === 0 && !isLoading">
            <td colspan="5" class="p-2 border text-center text-gray-500">
              لا يوجد عملاء لعرضهم
            </td>
          </tr>
        </tbody>
      </table>
  
      <div v-if="isLoading" class="mt-4 text-gray-500">جاري تحميل العملاء...</div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, computed, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import { frappe } from 'frappejs';
  
  export default {
    name: 'CustomerManagement',
    setup() {
      const router = useRouter();
      
      // البيانات
      const customers = ref([]);
      const searchQuery = ref('');
      const isLoading = ref(false);
      const isCreating = ref(false);
      const isDeleting = ref(false);
      const error = ref(null);
      const successMessage = ref('');
      const showCreateForm = ref(false);
      
      const newCustomer = reactive({
        customer_name: "",
        customer_type: "",
        customer_primary_address: "",
        tax_id: "",
      });
  
      // جلب العملاء
      const fetchCustomers = async () => {
        isLoading.value = true;
        error.value = null;
        try {
          const data = await frappe.call({
            method: "frappe.client.get_list",
            args: {
              doctype: "Customer",
              fields: ["name", "customer_name", "customer_type", "customer_primary_address", "tax_id"],
              limit_page_length: 0
            }
          });
          customers.value = data || [];
        } catch (err) {
          error.value = handleApiError(err);
        } finally {
          isLoading.value = false;
        }
      };
  
      // إنشاء عميل
      const createCustomer = async () => {
        isCreating.value = true;
        error.value = null;
        try {
          await frappe.call({
            method: "frappe.client.insert",
            args: {
              doc: {
                ...newCustomer,
                doctype: "Customer"
              }
            }
          });
          
          resetCustomerForm();
          await fetchCustomers();
          showCreateForm.value = false;
          successMessage.value = 'تم إضافة العميل بنجاح!';
        } catch (err) {
          error.value = handleApiError(err);
        } finally {
          isCreating.value = false;
        }
      };
  
      // حذف عميل
      const deleteCustomer = async (id) => {
        if (!confirm('هل أنت متأكد أنك تريد حذف هذا العميل؟')) return;
        
        isDeleting.value = true;
        error.value = null;
        try {
          await frappe.call({
            method: "frappe.client.delete",
            args: {
              doctype: "Customer",
              name: id
            }
          });
          successMessage.value = 'تم حذف العميل بنجاح!';
          await fetchCustomers();
        } catch (err) {
          error.value = handleApiError(err);
        } finally {
          isDeleting.value = false;
        }
      };
  
      // عرض تفاصيل العميل
      const viewCustomer = (id) => {
        // يمكنك تعديل هذا الرابط بناءً على بنية مسارات تطبيقك
        console.log('View customer:', id);
        // router.push({ name: 'customer-details', params: { id } });
      };
  
      // تعديل العميل
      const editCustomer = (id) => {
        // يمكنك تعديل هذا الرابط بناءً على بنية مسارات تطبيقك
        console.log('Edit customer:', id);
        // router.push({ name: 'customer-edit', params: { id } });
      };
  
      // دوال مساعدة
      const resetCustomerForm = () => {
        Object.assign(newCustomer, {
          customer_name: "",
          customer_type: "",
          customer_primary_address: "",
          tax_id: "",
        });
      };
  
      const handleApiError = (err) => {
        // فراپي يعيد الأخطاء في بنية مختلفة، لذا نقوم بمعالجتها
        if (err.message) {
          try {
            const errorMessage = JSON.parse(err.message).message;
            return errorMessage;
          } catch {
            return err.message;
          }
        }
        return "حدث خطأ غير معروف.";
      };
  
      // ترجمات عربية
      const getCustomerTypeArabic = (type) => {
        const typeMap = {
          'Company': 'شركة',
          'Individual': 'فرد',
          '': '--'
        };
        return typeMap[type] || type;
      };
  
      // جلب البيانات الأولية
      onMounted(async () => {
        await fetchCustomers();
      });
  
      // الخصائص المحسوبة
      const filteredCustomers = computed(() => {
        if (!searchQuery.value) return customers.value;
        const query = searchQuery.value.toLowerCase();
        return customers.value.filter(customer => (
          (customer.customer_name && customer.customer_name.toLowerCase().includes(query)) ||
          (customer.name && customer.name.toLowerCase().includes(query)) ||
          (customer.customer_primary_address && customer.customer_primary_address.toLowerCase().includes(query)) ||
          (customer.tax_id && customer.tax_id.toLowerCase().includes(query))
        ));
      });
  
      return {
        customers,
        searchQuery,
        isLoading,
        isCreating,
        isDeleting,
        error,
        successMessage,
        showCreateForm,
        newCustomer,
        filteredCustomers,
        fetchCustomers,
        createCustomer,
        deleteCustomer,
        viewCustomer,
        editCustomer,
        resetCustomerForm,
        getCustomerTypeArabic
      };
    }
  }
  </script>
  
  <style scoped>
  /* تنسيقات RTL */
  [dir="rtl"] table th,
  [dir="rtl"] table td {
    text-align: right;
  }
  
  /* تأثيرات الأزرار */
  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  </style>