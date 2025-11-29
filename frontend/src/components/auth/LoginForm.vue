<template>
  <div class="modern-card" style="width: 400px;">
    <div class="card-header">
      <div class="text-center">
        <div class="icon-container">
          <i class="bi bi-car-front-fill"></i>
        </div>
        <h3 class="mt-3">Parking Hub</h3>
        <p class="subtitle">Sign in to your account</p>
      </div>
    </div>
    <div class="card-body p-4">
      
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
          <i class="bi bi-info-circle me-1"></i>
          Demo Admin: admin / admin123
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

<style scoped>
.modern-card {
  border: none;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  background: white;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem 1rem 1rem;
  border-bottom: none;
}

.icon-container {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  margin: 0 auto;
  backdrop-filter: blur(10px);
}

.card-header h3 {
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.subtitle {
  opacity: 0.9;
  font-size: 0.95rem;
}

.btn-group {
  display: flex;
  gap: 0.5rem;
}

.btn-check:checked + .btn-outline-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
}

.btn-outline-primary {
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  transform: translateY(-2px);
}
</style>
