<template>
  <div class="card shadow-lg" style="width: 400px;">
    <div class="card-body p-4">
      <div class="text-center mb-4">
        <i class="bi bi-car-front-fill text-primary" style="font-size: 3rem;"></i>
        <h3 class="mt-2">Vehicle Parking App</h3>
        <p class="text-muted">Sign in to your account</p>
      </div>
      
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label class="form-label">Login As</label>
          <div class="btn-group w-100" role="group">
            <input 
              type="radio" 
              class="btn-check" 
              name="role" 
              id="roleUser" 
              value="user" 
              v-model="role"
            >
            <label class="btn btn-outline-primary" for="roleUser">User</label>
            
            <input 
              type="radio" 
              class="btn-check" 
              name="role" 
              id="roleAdmin" 
              value="admin" 
              v-model="role"
            >
            <label class="btn btn-outline-primary" for="roleAdmin">Admin</label>
          </div>
        </div>
        
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input 
            type="text" 
            class="form-control" 
            id="username" 
            v-model="username" 
            required
            placeholder="Enter your username"
          >
        </div>
        
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input 
            type="password" 
            class="form-control" 
            id="password" 
            v-model="password" 
            required
            placeholder="Enter your password"
          >
        </div>
        
        <div v-if="errorMessage" class="alert alert-danger py-2">
          {{ errorMessage }}
        </div>
        
        <button 
          type="submit" 
          class="btn btn-primary w-100" 
          :disabled="loading"
        >
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          Sign In
        </button>
      </form>
      
      <div class="text-center mt-3">
        <p class="text-muted mb-0">
          Don't have an account? 
          <router-link to="/register" class="text-primary">Register here</router-link>
        </p>
      </div>
      
      <div class="text-center mt-3 pt-3 border-top">
        <small class="text-muted">
          Admin: admin / admin123
        </small>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../../composables/useAuth'
import { showToast } from '../shared/Toast.vue'

export default {
  name: 'LoginForm',
  setup() {
    const router = useRouter()
    const { login, loading } = useAuth()
    
    const username = ref('')
    const password = ref('')
    const role = ref('user')
    const errorMessage = ref('')
    
    const handleLogin = async () => {
      errorMessage.value = ''
      
      const result = await login(username.value, password.value, role.value)
      
      if (result.success) {
        showToast('Login successful!', 'success')
        
        if (result.user.role === 'admin') {
          router.push({ name: 'admin' })
        } else {
          router.push({ name: 'user' })
        }
      } else {
        errorMessage.value = result.error
        showToast(result.error, 'error')
      }
    }
    
    return {
      username,
      password,
      role,
      loading,
      errorMessage,
      handleLogin
    }
  }
}
</script>
