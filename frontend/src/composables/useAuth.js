import { ref, computed } from 'vue'
import { authApi } from '../services/api'

const user = ref(null)
const loading = ref(false)
const error = ref(null)

const storedUser = localStorage.getItem('user')
if (storedUser) {
  try {
    user.value = JSON.parse(storedUser)
  } catch (e) {
    localStorage.removeItem('user')
  }
}

export function useAuth() {
  const isAuthenticated = computed(() => !!user.value && !!localStorage.getItem('access_token'))
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isUser = computed(() => user.value?.role === 'user')
  
  const login = async (username, password, role = 'user') => {
    loading.value = true
    error.value = null
    
    try {
      const response = await authApi.login(username, password, role)
      const { access_token, refresh_token, user: userData } = response.data
      
      // Ensure the role from the backend response is used if available
      const userRole = userData?.role || role
      
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      localStorage.setItem('user', JSON.stringify({ ...userData, role: userRole }))
      
      user.value = { ...userData, role: userRole }
      
      return { success: true, user: user.value }
    } catch (err) {
      console.error('Login error:', err)
      error.value = err.response?.data?.error || err.message || 'Login failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }
  
  const register = async (userData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await authApi.register(userData)
      const { access_token, refresh_token, user: newUser } = response.data
      
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      localStorage.setItem('user', JSON.stringify({ ...newUser, role: 'user' }))
      
      user.value = { ...newUser, role: 'user' }
      
      return { success: true, user: user.value }
    } catch (err) {
      error.value = err.response?.data?.error || 'Registration failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }
  
  const logout = async () => {
    loading.value = true
    
    try {
      await authApi.logout()
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      user.value = null
      loading.value = false
    }
  }
  
  const checkAuth = () => {
    const token = localStorage.getItem('access_token')
    const storedUser = localStorage.getItem('user')
    
    if (token && storedUser) {
      try {
        user.value = JSON.parse(storedUser)
        return true
      } catch (e) {
        localStorage.removeItem('user')
        return false
      }
    }
    return false
  }
  
  const getUser = () => user.value
  
  return {
    user,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    isUser,
    login,
    register,
    logout,
    checkAuth,
    getUser
  }
}
