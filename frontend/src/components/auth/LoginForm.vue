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
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(102, 126, 234, 0.2);
  overflow: hidden;
  background: white;
  animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.modern-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.02) 0%, rgba(118, 75, 162, 0.02) 100%);
  pointer-events: none;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2.5rem 1.5rem 1.5rem;
  border-bottom: none;
  position: relative;
  overflow: hidden;
}

.card-header::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 300px;
  height: 300px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.icon-container {
  width: 70px;
  height: 70px;
  background: rgba(255, 255, 255, 0.25);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.2rem;
  margin: 0 auto;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
}

.icon-container:hover {
  transform: scale(1.1) rotate(-5deg);
  background: rgba(255, 255, 255, 0.35);
}

.card-header h3 {
  font-weight: 800;
  margin-bottom: 0.25rem;
  font-size: 1.8rem;
  position: relative;
  z-index: 1;
}

.subtitle {
  opacity: 0.95;
  font-size: 0.95rem;
  font-weight: 500;
  position: relative;
  z-index: 1;
}

.btn-group {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.btn-check:checked + .btn-outline-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
  transform: translateY(-2px);
}

.btn-outline-primary {
  border-radius: 10px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-width: 1.5px;
}

.btn-outline-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
}
</style>
