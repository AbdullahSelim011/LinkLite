<template>
  <div>
    <Navbar />
    <div
      class="grid grid-cols-4 items-stretch w-full grid-flow-col-dense bg-surface-white shadow"
      dir="rtl" >
      <div class="flex h-full col-span-1">
        
      <Sidebar
        :header="{
          title: 'جود النقل',
          logo: '/src/assets/logo.png',
          menuItems: [
            {
              label: 'تبديل الثيم',
              icon: Moon,
              iconClass: 'luxury-icon',
              onClick: toggleTheme,
            },
          ],
        }"
        :sections="[
          {
            label: 'الوحدات الرئيسية',
            items: [
              {
                label: 'لوحة التحكم',
                icon: PieChart,
                to: '/dashboard',
                iconClass: 'luxury-icon',
              },
              {
                label: 'إدارة الرحلات',
                icon: CalendarCheck,
                to: '/deliverytrip',
                iconClass: 'luxury-icon',
              },
              {
                label: 'إدارة السائقين',
                icon: Users,
                to: '/driver',
                iconClass: 'luxury-icon',
              },
              {
                label: 'إدارة الحسابات',
                icon: FileText,
                to: '/salesinvoice',
                iconClass: 'luxury-icon',
              },
              {
                label: 'إدارة العملاء',
                icon: User,
                to: '/customer',
                iconClass: 'luxury-icon',
              },
              {
                label: 'العناوين',
                icon: PieChart,
                to: '/address',
                iconClass: 'luxury-icon',
              },
            ],
          },
          {
            label: 'إدارة السيارات',
            items: [
              {
                label: 'مطالبات السيارات',
                icon: AlertCircle,
                to: '/vehicle',
                iconClass: 'luxury-icon',
              },
            ],
          },
        ]"
      />
      </div>
      <div class="flex h-full col-span-3 ">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { Sidebar } from 'frappe-ui'
import { useStorage } from '@vueuse/core'
import Navbar from './components/Navbar.vue'
// استيراد الأيقونات
import {
  Moon,
  CalendarCheck,
  Users,
  FileText,
  User,
  PieChart,
  AlertCircle,
} from 'lucide-vue-next'

const userTheme = useStorage('user-theme', 'light')

onMounted(() => {
  document.documentElement.setAttribute('data-theme', userTheme.value)
})

function toggleTheme() {
  const currentTheme = userTheme.value
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark'
  document.documentElement.setAttribute('data-theme', newTheme)
  userTheme.value = newTheme
}
</script>

<style>
/* تخصيصات للواجهة العربية */
[dir='rtl'] .sidebar-item {
  text-align: right;
  padding-right: 1rem;
}

.sidebar-section-label {
  font-weight: 600;
  color: #4b5563;
  padding: 0.5rem 1rem;
  margin-top: 1rem;
  border-bottom: 1px solid #e5e7eb;
  letter-spacing: 0.5px;
}

.sidebar-logo img {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

/* أنماط فاخرة للأيقونات */
.luxury-icon {
  font-size: 1.2rem;
  color: #8b5a2b;
  /* لون برونزي فاخر */
  transition: all 0.3s ease;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  padding: 8px;
  border-radius: 50%;
  background: linear-gradient(145deg, #f9f9f9, #ffffff);
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06),
    inset 0 -2px 4px rgba(255, 255, 255, 0.8);
}

.luxury-icon:hover {
  color: #d4af37;
  /* لون ذهبي عند التحويم */
  transform: translateY(-2px);
  box-shadow:
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05),
    inset 0 -2px 4px rgba(255, 255, 255, 0.8);
}

/* تأثيرات خاصة للوضع الليلي */
[data-theme='dark'] .luxury-icon {
  color: #d4af37;
  /* لون ذهبي في الوضع المظلم */
  background: linear-gradient(145deg, #2d3748, #4a5568);
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.3),
    0 2px 4px -1px rgba(0, 0, 0, 0.2),
    inset 0 -2px 4px rgba(0, 0, 0, 0.5);
}

[data-theme='dark'] .luxury-icon:hover {
  color: #ffd700;
  /* لون ذهبي فاتح عند التحويم */
}

/* تحسينات إضافية للفخامة */
.sidebar-item {
  transition: all 0.3s ease;
  margin: 4px 0;
  border-radius: 8px;
}

.sidebar-item:hover {
  background: rgba(139, 90, 43, 0.1);
  /* خلفية بنية فاتحة عند التحويم */
  transform: translateX(-2px);
}

[data-theme='dark'] .sidebar-item:hover {
  background: rgba(212, 175, 55, 0.1);
  /* خلفية ذهبية فاتحة في الوضع المظلم */
}
</style>
