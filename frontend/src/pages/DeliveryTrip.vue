<template>
  <div :class="{ 'page-shrink': showSidebar }">
    <h2 class="font-bold text-ink-gray-8">إدارة رحلات التوصيل</h2>


  <div class="flex justify-between items-center mb-4">
    <Button :label="showCreateForm ? 'إخفاء النموذج' : 'إضافة رحلة جديدة'" :icon-left="showCreateForm ? 'x' : 'plus'"
      @click="showCreateForm = !showCreateForm"></Button>

    <div class="relative w-72">
      <input v-model="searchQuery" type="text"
        class="w-full pr-4 pl-10 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="ابحث في الرحلات..." />
      <button class="absolute left-0 top-0 h-full px-3 text-gray-500 hover:text-gray-700" @click="fetchTrips">
        <i class="fas fa-search"></i>
      </button>
    </div>
  </div>

  <div v-if="showCreateForm" class="bg-white rounded-lg shadow-md mb-4 p-6">
    <h3 class="text-lg font-semibold mb-4">إضافة رحلة توصيل جديدة</h3>

    <form @submit.prevent="createTrip">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">وقت المغادرة</label>
          <input v-model="newTrip.departure_time" type="datetime-local"
            class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">المركبة</label>
          <select v-model="newTrip.vehicle"
            class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
            <option value="" disabled>اختر المركبة</option>
            <option v-for="vehicle in vehicles" :key="vehicle.name" :value="vehicle.name">
              {{ vehicle.license_plate || vehicle.name }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">السائق</label>
          <select v-model="newTrip.driver"
            class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
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
              <select v-model="stop.customer" @change="loadCustomerAddresses(stop)"
                class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                <option value="" disabled>اختر العميل</option>
                <option v-for="customer in customers" :key="customer.name" :value="customer.name">
                  {{ customer.customer_name || customer.name }}
                </option>
              </select>
            </div>

            <div class="col-span-10 md:col-span-5">
              <label class="block text-sm font-medium text-gray-700 mb-1">العنوان</label>
              <select v-model="stop.address"
                class="w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="" disabled>اختر العنوان</option>
                <option v-for="address in stop.addresses || []" :key="address.name" :value="address.name">
                  {{ address.address_title || address.name }}
                </option>
              </select>
            </div>

            <div class="col-span-2 md:col-span-1 flex items-end">
              <Button icon="trash-2" appearance="minimal" @click="removeStop(index)" />
            </div>
          </div>

          <Button label="إضافة توقف" icon-left="plus" appearance="minimal" @click="addStop" />
        </div>

        <div class="col-span-2 flex justify-end space-x-2">
          <Button label="إعادة تعيين" appearance="secondary" @click="resetTripForm" />
          <Button :label="isCreating ? 'جاري الإضافة...' : 'إضافة الرحلة'" :icon-left="isCreating ? 'loader' : 'plus'"
            :loading="isCreating" type="submit" />
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
              رقم الرحلة
            </th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              وقت المغادرة
            </th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              المركبة
            </th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              السائق
            </th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              عدد التوقفات
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
          <tr v-for="trip in filteredTrips" :key="trip.name" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-right">{{ trip.name }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-right">
              {{ formatDateTime(trip.departure_time) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right">
              {{ getVehiclePlate(trip.vehicle) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right">
              {{ getDriverName(trip.driver) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right">
              {{ trip.delivery_stops?.length || 0 }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right">
              <span :class="getStatusClass(trip.status)">
                {{ getStatusArabic(trip.status) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex flex-wrap gap-2 justify-end">
                <Button label="عرض" icon-left="eye" appearance="minimal" @click="fetchTripDetails(trip.name)" />

                <Button v-if="trip.status === 'Draft'" label="ترحيل" icon-left="check" appearance="minimal"
                  :loading="isSubmitting" @click="submitTrip(trip.name)" />

                <Button v-if="trip.status !== 'Cancelled' && trip.docstatus === 1" label="إلغاء" icon-left="ban"
                  appearance="minimal" :loading="isCancelling" @click="cancelTrip(trip.name)" />

                <Button v-if="trip.status === 'Draft' || trip.status === 'Cancelled'" label="حذف" icon-left="trash-2"
                  appearance="minimal" :loading="isDeleting" @click="deleteTrip(trip.name)" />
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

  <div v-if="isLoading" class="text-center my-8 py-8">
    <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    <h5 class="mt-3 text-gray-600">جاري تحميل الرحلات...</h5>
  </div>

  <div v-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mt-4 rounded">
    <div class="flex justify-between items-center">
      <div class="flex items-center">
        <i class="fas fa-exclamation-triangle ml-2"></i>
        <strong>خطأ!</strong> {{ error }}
      </div>
      <button type="button" class="text-red-700" @click="error = null">
        <i class="fas fa-times"></i>
      </button>
    </div>
  </div>

  <div v-if="successMessage" class="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 mt-4 rounded">
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

  <!-- Sidebar -->

    <Sidebar
      v-if="showSidebar"
      :record="selectedTrip"
      title="تفاصيل الرحلة"
      @close="showSidebar = false"
    />
  </div>
</template>

<script setup>
import { createResource } from 'frappe-ui';
import { ref, reactive, computed, onMounted } from 'vue';
import { frappe } from '@/plugins/frappe'
const trips = ref([]);
const vehicles = ref([]);
const drivers = ref([]);
const customers = ref([]);
const searchQuery = ref('');
const isLoading = ref(false);
const isCreating = ref(false);
const isSubmitting = ref(false);
const isCancelling = ref(false);
const isDeleting = ref(false);
const error = ref(null);
const call = frappe.call()
const successMessage = ref('');
const showCreateForm = ref(false);

import Sidebar from "@/components/Sidebar.vue"
import DeleveryTripDetailsModal from "@/components/deleveryTrip/DeleveryTripDetailsModal.vue"

const deliveryTrips = ref([])
const selectedTrip = ref({})
const showSidebar = ref(false)
const newTrip = reactive({
  departure_time: new Date().toISOString().slice(0, 16),
  vehicle: '',
  driver: '',
  delivery_stops: [{ customer: '', address: '', addresses: [] }],
});

// Helper functions
const formatDateTime = (datetime) => {
  if (!datetime) return '';
  const date = new Date(datetime);
  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  };
  return new Intl.DateTimeFormat('ar-EG', options).format(date);
};

const getVehiclePlate = (vehicleName) => {
  const vehicle = vehicles.value.find((v) => v.name === vehicleName);
  return vehicle ? vehicle.license_plate || vehicle.name : vehicleName;
};

const getDriverName = (driverName) => {
  const driver = drivers.value.find((d) => d.name === driverName);
  return driver ? driver.full_name || driver.name : driverName;
};

const getStatusClass = (status) => {
  switch (status) {
    case 'Draft':
      return 'bg-gray-200 text-gray-800 px-2 py-1 rounded-full';
    case 'Submitted':
      return 'bg-blue-100 text-blue-800 px-2 py-1 rounded-full';
    case 'Completed':
      return 'bg-green-100 text-green-800 px-2 py-1 rounded-full';
    case 'Cancelled':
      return 'bg-red-100 text-red-800 px-2 py-1 rounded-full';
    default:
      return 'bg-gray-200 text-gray-800 px-2 py-1 rounded-full';
  }
};

const getStatusArabic = (status) => {
  switch (status) {
    case 'Draft':
      return 'مسودة';
    case 'Submitted':
      return 'مرحّلة';
    case 'Completed':
      return 'مكتملة';
    case 'Cancelled':
      return 'ملغاة';
    default:
      return status;
  }
};

const addStop = () => {
  newTrip.delivery_stops.push({ customer: '', address: '', addresses: [] });
};

const removeStop = (index) => {
  newTrip.delivery_stops.splice(index, 1);
};

const loadCustomerAddresses = async (stop) => {
  if (!stop.customer) {
    stop.addresses = [];
    return;
  }

  try {
    const resource = createResource({
      url: 'linklite.api.get_customer_addresses',
      params: { customer: stop.customer },
    });

    const data = await resource.fetch();
    stop.addresses = data || [];
    stop.address = ''; // Reset address selection
  } catch (err) {
    console.error('Failed to load addresses', err);
    stop.addresses = [];
  }
};

const fetchTrips = async () => {
  try {
    const res = await call.get("linklite.api.get_delivery_trips");
    console.log(res);
    trips.value = res.message;
  } catch (error) {
    console.log(error);
    error.value = error.message || 'حدث خطأ أثناء تحميل الرحلات';
  } finally {
    isLoading.value = false;
  }

};

const fetchDependencies = () => {
  // Fetch vehicles
  createResource({
    url: 'linklite.api.get_vehicles',
    onSuccess(data) {
      vehicles.value = data;
    },
    onError(err) {
      error.value = err.message;
    },
  }).fetch();

  // Fetch drivers
  createResource({
    url: 'linklite.api.get_drivers',
    onSuccess(data) {
      drivers.value = data;
    },
    onError(err) {
      error.value = err.message;
    },
  }).fetch();

  // Fetch customers
  createResource({
    url: 'linklite.api.get_customers',
    onSuccess(data) {
      customers.value = data;
    },
    onError(err) {
      error.value = err.message;
    },
  }).fetch();
};

const createTrip = () => {
  isCreating.value = true;
  error.value = null;

  // Validate inputs
  if (!newTrip.departure_time || !newTrip.vehicle || !newTrip.driver) {
    error.value = "يجب إدخال جميع الحقول المطلوبة";
    isCreating.value = false;
    return;
  }

  if (newTrip.delivery_stops.length === 0 ||
    newTrip.delivery_stops.some(stop => !stop.customer)) {
    error.value = "يجب إدخال عميل لكل توقف";
    isCreating.value = false;
    return;
  }

  const resource = createResource({
    url: 'linklite.api.create_delivery_trip',
    params: {
      departure_time: newTrip.departure_time,
      vehicle: newTrip.vehicle,
      driver: newTrip.driver,
      delivery_stops: newTrip.delivery_stops.map(stop => ({
        customer: stop.customer,
        address: stop.address || ''
      }))
    },
    onSuccess(data) {
      resetTripForm();
      fetchTrips();
      showCreateForm.value = false;
      successMessage.value = data.message || 'تم إنشاء الرحلة بنجاح!';
    },
    onError(err) {
      error.value = err.message;
    },
  });

  resource.fetch().finally(() => {
    isCreating.value = false;
  });
};

const submitTrip = (name) => {
  if (!confirm('هل تريد ترحيل هذه الرحلة؟')) return;
  isSubmitting.value = true;
  const resource = createResource({
    url: 'linklite.api.submit_delivery_trip',
    params: { name },
    onSuccess() {
      successMessage.value = 'تم ترحيل الرحلة بنجاح!';
      fetchTrips();
    },
    onError(err) {
      error.value = err.message;
    },
  });
  resource.fetch().finally(() => {
    isSubmitting.value = false;
  });
};

const cancelTrip = (name) => {
  if (!confirm('هل تريد إلغاء هذه الرحلة؟')) return;
  isCancelling.value = true;
  const resource = createResource({
    url: 'linklite.api.cancel_delivery_trip',
    params: { name },
    onSuccess() {
      successMessage.value = 'تم إلغاء الرحلة بنجاح!';
      fetchTrips();
    },
    onError(err) {
      error.value = err.message;
    },
  });
  resource.fetch().finally(() => {
    isCancelling.value = false;
  });
};

const deleteTrip = (name) => {
  if (!confirm('هل تريد حذف هذه الرحلة نهائياً؟')) return;
  isDeleting.value = true;
  const resource = createResource({
    url: 'linklite.api.delete_delivery_trip',
    params: { name },
    onSuccess() {
      successMessage.value = 'تم حذف الرحلة بنجاح!';
      fetchTrips();
    },
    onError(err) {
      error.value = err.message;
    },
  });
  resource.fetch().finally(() => {
    isDeleting.value = false;
  });
};

const viewTrip = (name) => {
  // يمكنك توجيه المستخدم إلى صفحة عرض الرحلة
  window.open(`/app/delivery-trip/${name}`, '_blank');
};

const resetTripForm = () => {
  newTrip.departure_time = new Date().toISOString().slice(0, 16);
  newTrip.vehicle = '';
  newTrip.driver = '';
  newTrip.delivery_stops = [{ customer: '', address: '', addresses: [] }];
};

const filteredTrips = computed(() => {
  if (!searchQuery.value) return trips.value;
  const q = searchQuery.value.toLowerCase();
  return trips.value.filter(
    (t) =>
      (t.name && t.name.toLowerCase().includes(q)) ||
      (t.vehicle && getVehiclePlate(t.vehicle).toLowerCase().includes(q)) ||
      (t.driver && getDriverName(t.driver).toLowerCase().includes(q)) ||
      (t.status && getStatusArabic(t.status).toLowerCase().includes(q))
  );
});

// Fetch initial data
onMounted(() => {
  fetchTrips();
  fetchDependencies();
});


async function fetchTripDetails(tripName) {
  const resource = createResource({
    url: "frappe.client.get",
    params: {
      doctype: "Delivery Trip",
      name: tripName,
    },
    onSuccess(data) {
      selectedTrip.value = data
      showSidebar.value = true
    },
    onError(err) {
      console.error("❌ Error fetching trip:", err)
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

/* Status badge styles */
.bg-gray-200,
.bg-blue-100,
.bg-red-100,
.bg-green-100 {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

/* Page shrink effect when sidebar is visible */
.page-shrink {
  margin-left: 400px;
  transition: margin-right 0.3s ease;
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