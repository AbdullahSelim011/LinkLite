import { createRouter, createWebHistory } from 'vue-router'
import { session } from './data/session'
import { userResource } from '@/data/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
  },
  {
    path: '/driver',
    name: 'Driver',
    component: () => import('@/pages/Driver.vue'),
  },
  {
    path: '/deliverytrip',
    name: 'DeliveryTrip',
    component: () => import('@/pages/DeliveryTrip.vue'),
  },
  {
    path: '/customer',
    name: 'Customer',
    component: () => import('@/pages/Customer.vue'),
  },
  {
    path: '/salesinvoice',
    name: 'SalesInvoice',
    component: () => import('@/pages/SalesInvoice.vue'),
  },
  {
    path: '/vehicle',
    name: 'Vehicle',
    component: () => import('@/pages/Vehicle.vue'),
  },
  {
    path: '/address',
    name: 'Address',
    component: () => import('@/pages/Address.vue'),
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/pages/Dashboard.vue'),
  },
]

const router = createRouter({
  history: createWebHistory('/links'),
  routes,
})

router.beforeEach(async (to, from, next) => {
  let isLoggedIn = session.isLoggedIn
  try {
    await userResource.promise
  } catch (error) {
    isLoggedIn = false
  }

  if (to.name === 'Login' && isLoggedIn) {
    next({ name: '/Home' })
  } else if (to.name !== 'Login' && !isLoggedIn) {
    window.location.href = '/login'
  } else {
    next()
  }
})

export default router
