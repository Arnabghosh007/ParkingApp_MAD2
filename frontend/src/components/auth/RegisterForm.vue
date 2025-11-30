<template>
  <div class="modern-card" style="width: 450px; max-height: 90vh; overflow-y: auto;">
    <div class="card-header">
      <div class="text-center">
        <div class="icon-container">
          <i class="bi bi-person-plus-fill"></i>
        </div>
        <h3 class="mt-3">Create Account</h3>
        <p class="subtitle">Join our parking community</p>
      </div>
    </div>
    <div class="card-body p-4">
      
      <form @submit.prevent="handleRegister">
        <div class="row">
          <div class="col-md-6 mb-3">
            <label for="username" class="form-label">Username *</label>
            <input 
              type="text" 
              class="form-control" 
              id="username" 
              v-model="formData.username" 
              required
            >
          </div>
          
          <div class="col-md-6 mb-3">
            <label for="email" class="form-label">Email</label>
            <input 
              type="email" 
              class="form-control" 
              id="email" 
              v-model="formData.email"
            >
          </div>
        </div>
        
        <div class="mb-3">
          <label for="password" class="form-label">Password *</label>
          <input 
            type="password" 
            class="form-control" 
            id="password" 
            v-model="formData.password" 
            required
            minlength="6"
          >
        </div>
        
        <div class="mb-3">
          <label for="confirmPassword" class="form-label">Confirm Password *</label>
          <input 
            type="password" 
            class="form-control" 
            id="confirmPassword" 
            v-model="confirmPassword" 
            required
          >
        </div>
        
        <div class="mb-3">
          <label for="fullName" class="form-label">Full Name</label>
          <input 
            type="text" 
            class="form-control" 
            id="fullName" 
            v-model="formData.full_name"
          >
        </div>
        
        <div class="row">
          <div class="col-md-6 mb-3">
            <label for="vehicleNumber" class="form-label">Vehicle Number</label>
            <input 
              type="text" 
              class="form-control" 
              id="vehicleNumber" 
              v-model="formData.vehicle_number"
              placeholder="e.g., MH12AB1234"
            >
          </div>
          
          <div class="col-md-6 mb-3">
            <label for="phone" class="form-label">Phone</label>
            <input 
              type="tel" 
              class="form-control" 
              id="phone" 
              v-model="formData.phone"
            >
          </div>
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
          Create Account
        </button>
      </form>
      
      <div class="text-center mt-3">
        <p class="text-muted mb-0">
          Already have an account? 
          <router-link to="/login" class="text-primary">Sign in here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { showToast } from '../shared/Toast.vue'

export default {
  name: 'RegisterForm',
  setup() {
    const router = useRouter()
    const store = useStore()
    
    const formData = reactive({
      username: '',
      password: '',
      email: '',
      full_name: '',
      vehicle_number: '',
      phone: ''
    })
    
    const confirmPassword = ref('')
    const errorMessage = ref('')
    
    const loading = computed(() => store.getters.authLoading)
    
    const handleRegister = async () => {
      errorMessage.value = ''
      
      if (formData.password !== confirmPassword.value) {
        errorMessage.value = 'Passwords do not match'
        return
      }
      
      if (formData.password.length < 6) {
        errorMessage.value = 'Password must be at least 6 characters'
        return
      }
      
      const result = await store.dispatch('register', formData)
      
      if (result.success) {
        showToast('Registration successful!', 'success')
        router.push({ name: 'user' })
      } else {
        errorMessage.value = result.error
        showToast(result.error, 'error')
      }
    }
    
    return {
      formData,
      confirmPassword,
      loading,
      errorMessage,
      handleRegister
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
</style>
