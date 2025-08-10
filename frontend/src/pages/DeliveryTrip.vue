<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">رحلات التوصيل</h1>

    <!-- رسالة نجاح -->
    <div v-if="successMessage" class="p-2 mb-4 bg-green-100 text-green-700 rounded">
      {{ successMessage }}
    </div>

    <!-- رسالة خطأ -->
    <div v-if="error" class="p-2 mb-4 bg-red-100 text-red-700 rounded">
      {{ error }}
    </div>

    <!-- شريط البحث -->
    <input
      v-model="searchQuery"
      type="text"
      placeholder="بحث..."
      class="border rounded px-2 py-1 mb-4 w-full"
    />

    <!-- زر إضافة -->
    <button @click="showCreateForm = !showCreateForm" class="bg-blue-600 text-white px-4 py-2 rounded mb-4">
      {{ showCreateForm ? 'إغلاق النموذج' : 'إضافة رحلة جديدة' }}
    </button>

    <!-- نموذج إنشاء -->
    <div v-if="showCreateForm" class="mb-4 border p-4 rounded bg-gray-50">
      <label class="block mb-2">وقت المغادرة:</label>
      <input type="datetime-local" v-model="newTrip.departure_time" class="border rounded px-2 py-1 w-full mb-2" />

      <label class="block mb-2">المركبة:</label>
      <input type="text" v-model="newTrip.vehicle" class="border rounded px-2 py-1 w-full mb-2" />

      <label class="block mb-2">السائق:</label>
      <input type="text" v-model="newTrip.driver" class="border rounded px-2 py-1 w-full mb-2" />

      <label class="block mb-2">العميل:</label>
      <input type="text" v-model="newTrip.delivery_stops[0].customer" class="border rounded px-2 py-1 w-full mb-4" />

      <button @click="createTrip" :disabled="isCreating" class="bg-green-600 text-white px-4 py-2 rounded">
        {{ isCreating ? 'جاري الحفظ...' : 'حفظ' }}
      </button>
    </div>

    <!-- جدول الرحلات -->
    <table class="w-full border">
      <thead>
        <tr class="bg-gray-200">
          <th class="p-2 border">الاسم</th>
          <th class="p-2 border">وقت المغادرة</th>
          <th class="p-2 border">المركبة</th>
          <th class="p-2 border">السائق</th>
          <th class="p-2 border">الحالة</th>
          <th class="p-2 border">إجراءات</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="trip in filteredTrips" :key="trip.name">
          <td class="p-2 border">{{ trip.name }}</td>
          <td class="p-2 border">{{ trip.departure_time }}</td>
          <td class="p-2 border">{{ trip.vehicle }}</td>
          <td class="p-2 border">{{ trip.driver }}</td>
          <td class="p-2 border">{{ trip.status }}</td>
          <td class="p-2 border flex gap-2">
            <button @click="submitTrip(trip.name)" class="bg-blue-600 text-white px-2 py-1 rounded">ترحيل</button>
            <button @click="cancelTrip(trip.name)" class="bg-yellow-500 text-white px-2 py-1 rounded">إلغاء</button>
            <button @click="deleteTrip(trip.name)" class="bg-red-600 text-white px-2 py-1 rounded">حذف</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- تحميل -->
    <div v-if="isLoading" class="mt-4 text-gray-500">جاري تحميل البيانات...</div>
  </div>
</template>

<script setup>
import { createResource } from 'frappe-ui';
import { ref, reactive, computed } from 'vue';

const trips = ref([]);
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

const fetchTrips = () => {
  isLoading.value = true;
  const resource = createResource({
    url: 'linklite.api.get_delivery_trips',
    onSuccess(data) {
      trips.value = data;
    },
    onError(err) {
      error.value = err.message;
    }
  });
  resource.fetch().finally(() => {
    isLoading.value = false;
  });
};

const createTrip = () => {
  isCreating.value = true;
  const resource = createResource({
    url: 'linklite.api.create_delivery_trip',
    params: { ...newTrip },
    onSuccess() {
      resetTripForm();
      fetchTrips();
      showCreateForm.value = false;
      successMessage.value = 'تم إنشاء الرحلة بنجاح!';
    },
    onError(err) {
      error.value = err.message;
    }
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
    }
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
    }
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
    }
  });
  resource.fetch().finally(() => {
    isDeleting.value = false;
  });
};

const resetTripForm = () => {
  newTrip.departure_time = new Date().toISOString().slice(0, 16);
  newTrip.vehicle = "";
  newTrip.driver = "";
  newTrip.delivery_stops = [{ customer: "" }];
};

const filteredTrips = computed(() => {
  if (!searchQuery.value) return trips.value;
  const q = searchQuery.value.toLowerCase();
  return trips.value.filter(t =>
    (t.name && t.name.toLowerCase().includes(q)) ||
    (t.vehicle && t.vehicle.toLowerCase().includes(q)) ||
    (t.driver && t.driver.toLowerCase().includes(q)) ||
    (t.status && t.status.toLowerCase().includes(q))
  );
});

fetchTrips();
</script>
