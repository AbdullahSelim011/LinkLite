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
	path: '/analytics',
	name: 'Analytics',
	component: () => import('@/pages/Analytics.vue'),
  },
  {
    path: '/deliverytrip',
    name: 'DeliveryTrip',
    component: () => import('@/pages/DeliveryTrip.vue'),
  }
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
    next({ name: 'Home' })
  } else if (to.name !== 'Login' && !isLoggedIn) {
    window.location.href = "/login"
  } else {
    next()
  }
})

export default router
