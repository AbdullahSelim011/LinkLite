<template>
  <div class="customer-management-container">
    <!-- Header Section -->
    <div class="page-header">
      <h2 class="page-title">إدارة العملاء</h2>
      <div class="header-actions">
        <button
          @click="toggleCreateForm"
          class="btn btn-primary"
          :class="{ 'btn-outline': showCreateForm }"
        >
          <i class="fas" :class="showCreateForm ? 'fa-times' : 'fa-plus'"></i>
          {{ showCreateForm ? 'إغلاق النموذج' : 'إضافة عميل جديد' }}
        </button>
      </div>
    </div>

    <!-- Search and Filter Bar -->
    <div class="search-filter-bar">
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="ابحث في العملاء..."
          class="search-input"
        />
        <i class="fas fa-search search-icon"></i>
      </div>
    </div>

    <!-- Create/Edit Form -->
    <transition name="slide-fade">
      <div v-if="showCreateForm" class="customer-form-container">
        <div class="form-card">
          <h3 class="form-title">
            {{ isEditing ? 'تعديل العميل' : 'إضافة عميل جديد' }}
          </h3>
          
          <form @submit.prevent="submitCustomer" class="customer-form">
            <div class="form-grid">
              <!-- Row 1 -->
              <div class="form-group">
                <label class="form-label">اسم العميل*</label>
                <input
                  v-model="newCustomer.customer_name"
                  type="text"
                  class="form-control"
                  required
                  placeholder="اسم العميل الكامل"
                />
              </div>
              
              <div class="form-group">
                <label class="form-label">نوع العميل*</label>
                <select
                  v-model="newCustomer.customer_type"
                  class="form-control"
                  required
                >
                  <option value="" disabled>اختر نوع العميل</option>
                  <option value="Company">شركة</option>
                  <option value="Individual">فرد</option>
                </select>
              </div>

              <!-- Row 2 -->
              <div class="form-group">
                <label class="form-label">العنوان</label>
                <input
                  v-model="newCustomer.customer_primary_address"
                  type="text"
                  class="form-control"
                  placeholder="العنوان الرئيسي"
                />
              </div>
              
              <div class="form-group">
                <label class="form-label">الرقم الضريبي</label>
                <input
                  v-model="newCustomer.tax_id"
                  type="text"
                  class="form-control"
                  placeholder="الرقم الضريبي (اختياري)"
                />
              </div>
            </div>

            <!-- Form Actions -->
            <div class="form-actions">
              <button
                type="button"
                @click="resetForm"
                class="btn btn-secondary"
              >
                إعادة تعيين
              </button>
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="isCreating"
              >
                <span v-if="isCreating">
                  <i class="fas fa-spinner fa-spin"></i> جاري الحفظ...
                </span>
                <span v-else>
                  <i class="fas fa-save"></i> {{ isEditing ? 'حفظ التعديلات' : 'حفظ العميل' }}
                </span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- Customer List -->
    <div class="customer-list-container">
      <div v-if="isLoading" class="loading-overlay">
        <div class="spinner"></div>
        <p>جاري تحميل العملاء...</p>
      </div>

      <div v-if="!isLoading && filteredCustomers.length === 0" class="empty-state">
        <i class="fas fa-users empty-icon"></i>
        <h3>لا يوجد عملاء مسجلين</h3>
        <p>ابدأ بإضافة عميل جديد باستخدام زر "إضافة عميل جديد" بالأعلى</p>
      </div>

      <div v-else class="customer-cards">
        <div
          v-for="customer in filteredCustomers"
          :key="customer.name"
          class="customer-card"
          :class="{
            'company-customer': customer.customer_type === 'Company',
            'individual-customer': customer.customer_type === 'Individual'
          }"
        >
          <div class="customer-card-header">
            <div class="customer-type-badge">
              {{ getCustomerTypeArabic(customer.customer_type) }}
            </div>
            <h3 class="customer-title">{{ customer.customer_name || customer.name }}</h3>
          </div>
          
          <div class="customer-card-body">
            <div class="customer-info">
              <div class="info-row">
                <span class="info-label">العنوان:</span>
                <span class="info-value">{{ customer.customer_primary_address || 'غير محدد' }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">الرقم الضريبي:</span>
                <span class="info-value">{{ customer.tax_id || 'غير محدد' }}</span>
              </div>
            </div>
          </div>
          
          <div class="customer-card-actions">
            <button
              @click="editCustomer(customer)"
              class="btn-action btn-edit"
            >
              <i class="fas fa-edit"></i> تعديل
            </button>
            <button
              @click="confirmDelete(customer.name)"
              class="btn-action btn-delete"
            >
              <i class="fas fa-trash-alt"></i> حذف
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast Notifications -->
    <transition name="fade">
      <div v-if="successMessage" class="toast toast-success">
        <div class="toast-content">
          <i class="fas fa-check-circle toast-icon"></i>
          <p>{{ successMessage }}</p>
        </div>
        <button @click="successMessage = ''" class="toast-close">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="error" class="toast toast-error">
        <div class="toast-content">
          <i class="fas fa-exclamation-circle toast-icon"></i>
          <p>{{ getArabicError(error) }}</p>
        </div>
        <button @click="error = null" class="toast-close">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </transition>

    <!-- Delete Confirmation Modal -->
    <transition name="modal">
      <div v-if="showDeleteModal" class="modal-overlay">
        <div class="modal-container">
          <div class="modal-header">
            <h3>تأكيد الحذف</h3>
            <button @click="showDeleteModal = false" class="modal-close">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="modal-body">
            <p>هل أنت متأكد أنك تريد حذف هذا العميل؟ لا يمكن التراجع عن هذه العملية.</p>
          </div>
          <div class="modal-footer">
            <button
              @click="showDeleteModal = false"
              class="btn btn-secondary"
            >
              إلغاء
            </button>
            <button
              @click="deleteCustomer"
              class="btn btn-danger"
              :disabled="isDeleting"
            >
              <span v-if="isDeleting">
                <i class="fas fa-spinner fa-spin"></i> جاري الحذف...
              </span>
              <span v-else>
                <i class="fas fa-trash-alt"></i> حذف
              </span>
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { createResource } from 'frappe-ui';

// البيانات
const customers = ref([]);
const searchQuery = ref('');
const isLoading = ref(false);
const isCreating = ref(false);
const isDeleting = ref(false);
const error = ref(null);
const successMessage = ref('');
const showCreateForm = ref(false);
const isEditing = ref(false);
const currentEditId = ref(null);
const showDeleteModal = ref(false);
const customerToDelete = ref(null);

const newCustomer = reactive({
  customer_name: '',
  customer_type: '',
  customer_primary_address: '',
  tax_id: ''
});

// دوال مساعدة
const getCustomerTypeArabic = (type) => {
  const typeMap = {
    'Company': 'شركة',
    'Individual': 'فرد',
    '': 'غير محدد'
  };
  return typeMap[type] || type;
};

const getArabicError = (err) => {
  if (err.includes('Not Found')) return 'البيانات المطلوبة غير موجودة.';
  if (err.includes('Permission Error')) return 'ليس لديك صلاحية للقيام بهذا الإجراء.';
  return typeof err === 'string' ? err : 'حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى.';
};

const getArabicSuccess = (msg) => {
  if (msg.includes('إنشاء')) return 'تم إنشاء العميل بنجاح!';
  if (msg.includes('تحديث')) return 'تم تحديث العميل بنجاح!';
  if (msg.includes('حذف')) return 'تم حذف العميل بنجاح!';
  return 'تم الإجراء بنجاح!';
};

const toggleCreateForm = () => {
  showCreateForm.value = !showCreateForm.value;
  if (!showCreateForm.value) {
    resetForm();
  }
};

const resetForm = () => {
  Object.assign(newCustomer, {
    customer_name: '',
    customer_type: '',
    customer_primary_address: '',
    tax_id: ''
  });
  isEditing.value = false;
  currentEditId.value = null;
};

// جلب العملاء
const fetchCustomers = () => {
  isLoading.value = true;
  const resource = createResource({
    url: 'frappe.client.get_list',
    params: {
      doctype: 'Customer',
      fields: ["name", "customer_name", "customer_type", "customer_primary_address", "tax_id"],
      limit_page_length: 0
    },
    onSuccess(data) {
      customers.value = data || [];
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isLoading.value = false;
  });
};

// إنشاء أو تحديث عميل
const submitCustomer = () => {
  isCreating.value = true;
  
  const apiMethod = isEditing.value ? 'linklite.api.update_customer' : 'linklite.api.create_customer';
  const params = {
    ...newCustomer,
    name: isEditing.value ? currentEditId.value : undefined
  };

  const resource = createResource({
    url: apiMethod,
    params: params,
    onSuccess(data) {
      resetForm();
      fetchCustomers();
      showCreateForm.value = false;
      successMessage.value = isEditing.value ? 'تم تحديث العميل بنجاح!' : 'تم إنشاء العميل بنجاح!';
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isCreating.value = false;
  });
};

// تعديل عميل
const editCustomer = (customer) => {
  isEditing.value = true;
  currentEditId.value = customer.name;
  Object.assign(newCustomer, {
    customer_name: customer.customer_name,
    customer_type: customer.customer_type,
    customer_primary_address: customer.customer_primary_address,
    tax_id: customer.tax_id
  });
  showCreateForm.value = true;
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

// تأكيد الحذف
const confirmDelete = (name) => {
  customerToDelete.value = name;
  showDeleteModal.value = true;
};

// حذف عميل
const deleteCustomer = () => {
  isDeleting.value = true;
  const resource = createResource({
    url: 'linklite.api.delete_customer',
    params: {
      name: customerToDelete.value
    },
    onSuccess() {
      successMessage.value = 'تم حذف العميل بنجاح!';
      fetchCustomers();
      showDeleteModal.value = false;
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

// جلب البيانات الأولية عند تحميل المكون
onMounted(() => {
  fetchCustomers();
});
</script>

<style scoped>
/* أنماط CSS مشابهة لصفحة العناوين مع تعديلات طفيفة */
.customer-management-container {
  font-family: 'Tajawal', sans-serif;
  direction: rtl;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* بطاقات العملاء */
.customer-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border-left: 4px solid #e2e8f0;
}

.company-customer {
  border-left-color: #4f46e5;
}

.individual-customer {
  border-left-color: #10b981;
}

.customer-type-badge {
  position: absolute;
  left: 16px;
  top: 16px;
  background-color: #e2e8f0;
  color: #4a5568;
  font-size: 12px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 12px;
}

.company-customer .customer-type-badge {
  background-color: #e0e7ff;
  color: #4f46e5;
}

.individual-customer .customer-type-badge {
  background-color: #d1fae5;
  color: #10b981;
}

.info-row {
  display: flex;
  margin-bottom: 8px;
}

.info-label {
  font-weight: 500;
  color: #4a5568;
  min-width: 100px;
}

.info-value {
  color: #718096;
}


.btn-action {
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: transparent;
  color: #64748b;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-action:hover {
  background-color: #f1f5f9;
  color: #4f46e5;
}

.btn-danger:hover {
  background-color: #fee2e2;
  color: #ef4444;
}

/* Toast Notifications */
.toast {
  position: fixed;
  bottom: 20px;
  left: 20px;
  right: 20px;
  max-width: 400px;
  padding: 12px 16px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  animation: slideIn 0.3s ease-out;
}

.toast-success {
  background-color: #f0fdf4;
  color: #166534;
  border-left: 4px solid #22c55e;
}

.toast-error {
  background-color: #fef2f2;
  color: #991b1b;
  border-left: 4px solid #ef4444;
}

.toast-content {
  display: flex;
  align-items: center;
}

.toast-icon {
  margin-left: 8px;
}

.toast-close {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 0;
  margin-right: 8px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  width: 90%;
  max-width: 400px;
  overflow: hidden;
}

.modal-header {
  padding: 16px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: #2d3748;
}

.modal-close {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  font-size: 18px;
}

.modal-body {
  padding: 16px;
  color: #4a5568;
}

.modal-footer {
  padding: 16px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* Animations */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes slideIn {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.95);
}

/* Responsive Styles */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .col-span-2 {
    grid-column: span 1;
  }
  
  .address-cards {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>