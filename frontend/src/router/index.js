import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import UserDashboard from '../views/UserDashboard.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { requiresGuest: true }
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/:tab?',
    name: 'admin-tab',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/user',
    name: 'user',
    component: UserDashboard,
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/:tab?',
    name: 'user-tab',
    component: UserDashboard,
    meta: { requiresAuth: true, role: 'user' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const storedUser = localStorage.getItem('user')
  let user = null
  
  if (storedUser) {
    try {
      user = JSON.parse(storedUser)
    } catch (e) {
      localStorage.removeItem('user')
    }
  }
  
  const isAuthenticated = !!token && !!user
  
  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      next({ name: 'login' })
      return
    }
    
    if (to.meta.role && user.role !== to.meta.role) {
      if (user.role === 'admin') {
        next({ name: 'admin' })
      } else {
        next({ name: 'user' })
      }
      return
    }
  }
  
  if (to.meta.requiresGuest && isAuthenticated) {
    if (user.role === 'admin') {
      next({ name: 'admin' })
    } else {
      next({ name: 'user' })
    }
    return
  }
  
  next()
})

export default router
