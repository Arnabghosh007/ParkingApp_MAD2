<template>
  <div class="card shadow-lg" style="width: 450px; max-height: 90vh; overflow-y: auto;">
    <div class="card-body p-4">
      <div class="text-center mb-4">
        <i class="bi bi-car-front-fill text-primary" style="font-size: 3rem;"></i>
        <h3 class="mt-2">Create Account</h3>
        <p class="text-muted">Register for a new account</p>
      </div>
      
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
        
        <div class="mb-3">
          <label for="address" class="form-label">Address</label>
          <textarea 
            class="form-control" 
            id="address" 
            v-model="formData.address" 
            rows="2"
          ></textarea>
        </div>
        
        <div class="mb-3">
          <label for="pinCode" class="form-label">PIN Code</label>
          <input 
            type="text" 
            class="form-control" 
            id="pinCode" 
            v-model="formData.pin_code"
            maxlength="6"
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
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../../composables/useAuth'
import { showToast } from '../shared/Toast.vue'

export default {
  name: 'RegisterForm',
  setup() {
    const router = useRouter()
    const { register, loading } = useAuth()
    
    const formData = reactive({
      username: '',
      password: '',
      email: '',
      full_name: '',
      vehicle_number: '',
      phone: '',
      address: '',
      pin_code: ''
    })
    
    const confirmPassword = ref('')
    const errorMessage = ref('')
    
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
      
      const result = await register(formData)
      
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
