<template>
    <div>
      <h2 class="font-bold text-ink-gray-8">إدارة رحلات التوصيل</h2>
    </div>
    
    <div class="flex justify-between items-center mb-4">
      <Button
        :label="showCreateForm ? 'إخفاء النموذج' : 'إضافة رحلة جديدة'"
        :icon-left="showCreateForm ? 'x' : 'plus'"
        @click="showCreateForm = !showCreateForm"
      />
      
      <div class="relative w-72">
        <input 
          v-model="searchQuery" 
          type="text" 
          class="w-full pr-4 pl-10 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="ابحث في الرحلات..."
        />
        <button 
          class="absolute left-0 top-0 h-full px-3 text-gray-500 hover:text-gray-700"
          @click="fetchTrips"
        >
          <i class="fas fa-search"></i>
        </button>
      </div>
    </div>
  
    <!-- Create Trip Form -->
    <div v-if="showCreateForm" class="bg-white rounded-lg shadow-md mb-4 p-6">
      <h3 class="text-lg font-semibold mb-4">إضافة رحلة توصيل جديدة</h3>
      
      <form @submit.prevent="createTrip">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">وقت المغادرة</label>
            <input 
              v-model="newTrip.departure_time" 
              type="datetime-local" 
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">المركبة</label>
            <select 
              v-model="newTrip.vehicle" 
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="" disabled>اختر المركبة</option>
              <option v-for="vehicle in vehicles" :key="vehicle.name" :value="vehicle.name">
                {{ vehicle.license_plate || vehicle.name }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">السائق</label>
            <select 
              v-model="newTrip.driver" 
              class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="" disabled>اختر السائق</option>
              <option v-for="driver in drivers" :key="driver.name" :value="driver.name">
                {{ driver.full_name || driver.name }}
              </option>
            </select>
          </div>
          
          <div class="col-span-2">
            <h5 class="font-medium mb-2">توقفات التوصيل:</h5>
            <div v-for="(stop, index) in newTrip.delivery_stops" :key="index" class="grid grid-cols-12 gap-3 mb-3">
              <div class="col-span-10 md:col-span-5">
                <label class="block text-sm font-medium text-gray-700 mb-1">العميل</label>
                <select 
                  v-model="stop.customer" 
                  class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                >
                  <option value="" disabled>اختر العميل</option>
                  <option v-for="customer in customers" :key="customer.name" :value="customer.name">
                    {{ customer.customer_name || customer.name }}
                  </option>
                </select>
              </div>
              <div class="col-span-2 md:col-span-1 flex items-end">
                <Button 
                  icon="trash-2"
                  appearance="minimal"
                  @click="removeStop(index)"
                />
              </div>
            </div>
            
            <Button 
              label="إضافة توقف"
              icon-left="plus"
              appearance="minimal"
              @click="addStop"
            />
          </div>
          
          <div class="col-span-2 flex justify-end space-x-2">
            <Button 
              label="إعادة تعيين"
              appearance="secondary"
              @click="resetTripForm"
            />
            <Button 
              :label="isCreating ? 'جاري الإضافة...' : 'إضافة الرحلة'"
              :icon-left="isCreating ? 'loader' : 'plus'"
              :loading="isCreating"
              type="submit"
            />
          </div>
        </div>
      </form>
    </div>
  
    <!-- Trips Table -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">رقم الرحلة</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">وقت المغادرة</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">المركبة</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">السائق</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">عدد التوقفات</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الحالة</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">الإجراءات</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="trip in filteredTrips" :key="trip.name" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ trip.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ formatDateTime(trip.departure_time) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ getVehiclePlate(trip.vehicle) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ getDriverName(trip.driver) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">{{ trip.delivery_stops?.length || 0 }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-right">
                <span :class="getStatusClass(trip.status)">
                  {{ getStatusArabic(trip.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex flex-wrap gap-2 justify-end">
                  <Button 
                    label="عرض"
                    icon-left="eye"
                    appearance="minimal"
                    @click="viewTrip(trip.name)"
                  />
                  
                  <Button 
                    v-if="trip.status === 'Draft'"
                    label="ترحيل"
                    icon-left="check"
                    appearance="minimal"
                    :loading="isSubmitting"
                    @click="submitTrip(trip.name)"
                  />
                  
                  <Button 
                    v-if="trip.status !== 'Cancelled' && trip.docstatus === 1"
                    label="إلغاء"
                    icon-left="ban"
                    appearance="minimal"
                    :loading="isCancelling"
                    @click="cancelTrip(trip.name)"
                  />
                  
                  <Button 
                    v-if="trip.status === 'Draft' || trip.status === 'Cancelled'"
                    label="حذف"
                    icon-left="trash-2"
                    appearance="minimal"
                    :loading="isDeleting"
                    @click="deleteTrip(trip.name)"
                  />
                </div>
              </td>
            </tr>
            <tr v-if="filteredTrips.length === 0 && !isLoading">
              <td colspan="7" class="px-6 py-4 text-center text-gray-500">
                لا توجد رحلات
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  
    <!-- Loading State -->
    <div v-if="isLoading" class="text-center my-8 py-8">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      <h5 class="mt-3 text-gray-600">جاري تحميل الرحلات...</h5>
    </div>
    
    <!-- Error Message -->
    <div v-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mt-4 rounded">
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
  
    <!-- Success Message -->
    <div v-if="successMessage" class="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mt-4 rounded">
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
  </template>
  
  <script setup>
  import { Button, createResource, createListResource } from 'frappe-ui';
  import { ref, computed, reactive } from 'vue';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  
  // State
  const trips = ref([]);
  const drivers = ref([]);
  const vehicles = ref([]);
  const customers = ref([]);
  const searchQuery = ref('');
  const isLoading = ref(false);
  const isCreating = ref(false);
  const isSubmitting = ref(false);
  const isCancelling = ref(false);
  const isDeleting = ref(false);
  const error = ref(null);
  const successMessage = ref('');
  const showCreateForm = ref(false);
  
  const newTrip = reactive({
    departure_time: new Date().toISOString().slice(0, 16),
    vehicle: "",
    driver: "",
    delivery_stops: [{ customer: "" }]
  });
  
  // Resources
  const tripsResource = createListResource({
    doctype: 'Delivery Trip',
    fields: ['name', 'departure_time', 'vehicle', 'driver', 'status', 'docstatus', 'delivery_stops.customer'],
    auto: true,
    onSuccess(data) {
      trips.value = data;
    },
    onError(err) {
      error.value = handleApiError(err);
    }
  });
  
  const driversResource = createListResource({
    doctype: 'Driver',
    fields: ['name', 'full_name'],
    auto: true,
    onSuccess(data) {
      drivers.value = data;
    }
  });
  
  const vehiclesResource = createListResource({
    doctype: 'Vehicle',
    fields: ['name', 'license_plate'],
    auto: true,
    onSuccess(data) {
      vehicles.value = data;
    }
  });
  
  const customersResource = createListResource({
    doctype: 'Customer',
    fields: ['name', 'customer_name'],
    auto: true,
    onSuccess(data) {
      customers.value = data;
    }
  });
  
  // Methods
  const fetchTrips = () => {
    isLoading.value = true;
    tripsResource.reload().finally(() => {
      isLoading.value = false;
    });
  };
  
  const createTrip = () => {
    isCreating.value = true;
    error.value = null;
    
    const tripResource = createResource({
      url: 'frappe.client.insert',
      params: {
        doc: {
          doctype: 'Delivery Trip',
          ...newTrip,
          status: "Draft",
          delivery_stops: newTrip.delivery_stops.map(stop => ({
            customer: stop.customer
          }))
        }
      },
      onSuccess() {
        resetTripForm();
        fetchTrips();
        showCreateForm.value = false;
        successMessage.value = 'تم إنشاء رحلة التوصيل بنجاح!';
      },
      onError(err) {
        error.value = handleApiError(err);
      },
      auto: true
    });
    
    tripResource.insert.finally(() => {
      isCreating.value = false;
    });
  };
  
  const submitTrip = (id) => {
    if (!confirm('هل أنت متأكد أنك تريد ترحيل هذه الرحلة؟ لا يمكن تعديل الرحلات المُرحلة.')) {
      return;
    }
  
    isSubmitting.value = true;
    error.value = null;
    successMessage.value = '';
  
    const submitResource = createResource({
      url: 'frappe.client.set_value',
      params: {
        doctype: 'Delivery Trip',
        name: id,
        fieldname: 'docstatus',
        value: 1
      },
      onSuccess() {
        successMessage.value = 'تم ترحيل الرحلة بنجاح!';
        fetchTrips();
      },
      onError(err) {
        error.value = handleSubmitError(err);
      },
      auto: true
    });
  
    submitResource.set_value.finally(() => {
      isSubmitting.value = false;
    });
  };
  
  const cancelTrip = (id) => {
    if (!confirm('هل أنت متأكد أنك تريد إلغاء هذه الرحلة؟')) {
      return;
    }
  
    isCancelling.value = true;
    error.value = null;
    successMessage.value = '';
  
    const cancelResource = createResource({
      url: 'frappe.client.set_value',
      params: {
        doctype: 'Delivery Trip',
        name: id,
        fieldname: 'status',
        value: 'Cancelled'
      },
      onSuccess() {
        successMessage.value = 'تم إلغاء الرحلة بنجاح!';
        fetchTrips();
      },
      onError(err) {
        error.value = err.message;
      },
      auto: true
    });
  
    cancelResource.set_value.finally(() => {
      isCancelling.value = false;
    });
  };
  
  const deleteTrip = (id) => {
    if (confirm('هل أنت متأكد أنك تريد حذف هذه الرحلة نهائياً؟')) {
      isDeleting.value = true;
      error.value = null;
      
      const deleteResource = createResource({
        url: 'frappe.client.delete',
        params: {
          doctype: 'Delivery Trip',
          name: id
        },
        onSuccess() {
          successMessage.value = 'تم حذف الرحلة بنجاح!';
          fetchTrips();
        },
        onError(err) {
          error.value = handleApiError(err);
        },
        auto: true
      });
  
      deleteResource.delete.finally(() => {
        isDeleting.value = false;
      });
    }
  };
  
  const viewTrip = (id) => {
    router.push(`/delivery-trips/${id}`);
  };
  
  const addStop = () => {
    newTrip.delivery_stops.push({ customer: "" });
  };
  
  const removeStop = (index) => {
    if (newTrip.delivery_stops.length > 1) {
      newTrip.delivery_stops.splice(index, 1);
    }
  };
  
  const resetTripForm = () => {
    newTrip.departure_time = new Date().toISOString().slice(0, 16);
    newTrip.vehicle = "";
    newTrip.driver = "";
    newTrip.delivery_stops = [{ customer: "" }];
  };
  
  // Helper functions
  const handleApiError = (err) => {
    if (err.response) {
      return err.response.data?.message || `خطأ في الخادم: ${err.response.status}`;
    } else if (err.request) {
      return "لم يتم استلام رد من الخادم. تحقق من اتصالك بالشبكة.";
    } else {
      return err.message || "خطأ في إعداد الطلب";
    }
  };
  
  const handleSubmitError = (err) => {
    if (err.response) {
      const serverMsg = err.response.data?.message || err.response.data?.exc;
      
      if (serverMsg?.includes('Cannot edit submitted document')) {
        return 'لا يمكن ترحيل رحلة مُرحّلة بالفعل';
      }
      if (serverMsg?.includes('Mandatory fields missing')) {
        return 'الحقول المطلوبة مفقودة في الرحلة';
      }
      return serverMsg || `خطأ في الخادم: ${err.response.status}`;
    }
    return err.message || 'فشل ترحيل الرحلة';
  };
  
  // Computed properties
  const filteredTrips = computed(() => {
    if (!searchQuery.value) return trips.value;
    const query = searchQuery.value.toLowerCase();
    return trips.value.filter(trip => (
      (trip.name && trip.name.toLowerCase().includes(query)) ||
      (trip.departure_time && formatDateTime(trip.departure_time).toLowerCase().includes(query)) ||
      (trip.vehicle && getVehiclePlate(trip.vehicle).toLowerCase().includes(query)) ||
      (trip.driver && getDriverName(trip.driver).toLowerCase().includes(query)) ||
      (trip.status && getStatusArabic(trip.status).toLowerCase().includes(query))
    ));
  });
  
  const getDriverName = (driverId) => {
    const driver = drivers.value.find(d => d.name === driverId);
    return driver ? (driver.full_name || driver.name) : driverId;
  };
  
  const getVehiclePlate = (vehicleId) => {
    const vehicle = vehicles.value.find(v => v.name === vehicleId);
    return vehicle ? (vehicle.license_plate || vehicle.name) : vehicleId;
  };
  
  const formatDateTime = (dateTimeString) => {
    if (!dateTimeString) return '';
    const date = new Date(dateTimeString);
    return date.toLocaleString('ar-SA', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };
  
  const getStatusClass = (status) => {
    const statusClasses = {
      'Draft': 'bg-gray-200 text-gray-800 px-2 py-1 rounded-full text-xs',
      'Submitted': 'bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs',
      'Cancelled': 'bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs'
    };
    return statusClasses[status] || 'bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs';
  };
  
  const getStatusArabic = (status) => {
    const statusMap = {
      'Draft': 'مسودة',
      'Submitted': 'مُرحلة',
      'Cancelled': 'ملغية'
    };
    return statusMap[status] || status;
  };
  
  const getArabicError = (error) => {
    const errorMap = {
      'Cannot modify submitted trip!': 'لا يمكن تعديل رحلة مُرحّلة!',
      'No response received from server. Check your connection.': 'لم يتم استلام رد من الخادم. تحقق من اتصالك بالشبكة.',
      'Request setup error': 'خطأ في إعداد الطلب',
      'Trip is already submitted': 'الرحلة مُرحّلة بالفعل',
      'Cannot submit trip in its current status': 'لا يمكن ترحيل الرحلة في حالتها الحالية',
      'Submission failed: Document status not updated': 'فشل الترحيل: لم يتم تحديث حالة المستند',
      'Cannot submit an already submitted trip': 'لا يمكن ترحيل رحلة مُرحّلة بالفعل',
      'Required fields are missing in the trip': 'الحقول المطلوبة مفقودة في الرحلة',
      'Failed to submit trip': 'فشل ترحيل الرحلة',
      'Trip is already cancelled': 'الرحلة ملغية بالفعل',
      'Failed to cancel trip': 'فشل إلغاء الرحلة'
    };
    return errorMap[error] || error;
  };
  
  const getArabicSuccess = (success) => {
    const successMap = {
      'Delivery trip created successfully!': 'تم إنشاء رحلة التوصيل بنجاح!',
      'Trip submitted successfully!': 'تم ترحيل الرحلة بنجاح!',
      'Trip cancelled successfully!': 'تم إلغاء الرحلة بنجاح!',
      'Trip deleted successfully!': 'تم حذف الرحلة بنجاح!'
    };
    return successMap[success] || success;
  };
  </script>
  
  <style scoped>
  /* Arabic font and RTL support */
  @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
  
  body, * {
    font-family: 'Tajawal', sans-serif;
  }
  
  /* RTL table adjustments */
  table {
    direction: rtl;
  }
  
  th {
    text-align: right;
  }
  
  /* Status badge styles */
  .bg-gray-200, .bg-blue-100, .bg-red-100 {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 500;
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