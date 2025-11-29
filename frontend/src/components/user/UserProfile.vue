<template>
  <div class="row g-4">
    <div class="col-md-4">
      <div class="card border-0 shadow-sm text-center">
        <div class="card-body py-4">
          <div class="rounded-circle bg-primary bg-opacity-10 d-inline-flex align-items-center justify-content-center" 
               style="width: 100px; height: 100px;">
            <i class="bi bi-person-fill text-primary" style="font-size: 48px;"></i>
          </div>
          <h4 class="mt-3 mb-1">{{ profile.full_name || profile.username }}</h4>
          <p class="text-muted mb-0">@{{ profile.username }}</p>
          <span class="badge bg-primary mt-2">User</span>
        </div>
      </div>
    </div>
    
    <div class="col-md-8">
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white d-flex justify-content-between align-items-center">
          <h5 class="mb-0">Profile Information</h5>
          <button class="btn btn-outline-primary btn-sm" @click="editMode = !editMode">
            <i :class="editMode ? 'bi bi-x' : 'bi bi-pencil'" class="me-1"></i>
            {{ editMode ? 'Cancel' : 'Edit' }}
          </button>
        </div>
        <div class="card-body">
          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border text-primary"></div>
          </div>
          
          <form v-else @submit.prevent="saveProfile">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label text-muted small">Full Name</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="formData.full_name"
                  :readonly="!editMode"
                  :class="{ 'form-control-plaintext': !editMode }"
                >
              </div>
              
              <div class="col-md-6">
                <label class="form-label text-muted small">Email</label>
                <input 
                  type="email" 
                  class="form-control" 
                  v-model="formData.email"
                  :readonly="!editMode"
                  :class="{ 'form-control-plaintext': !editMode }"
                >
              </div>
              
              <div class="col-md-6">
                <label class="form-label text-muted small">Vehicle Number</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="formData.vehicle_number"
                  :readonly="!editMode"
                  :class="{ 'form-control-plaintext': !editMode }"
                >
              </div>
              
              <div class="col-md-6">
                <label class="form-label text-muted small">Phone</label>
                <input 
                  type="tel" 
                  class="form-control" 
                  v-model="formData.phone"
                  :readonly="!editMode"
                  :class="{ 'form-control-plaintext': !editMode }"
                >
              </div>
              
              <div class="col-12">
                <label class="form-label text-muted small">Address</label>
                <textarea 
                  class="form-control" 
                  v-model="formData.address"
                  :readonly="!editMode"
                  :class="{ 'form-control-plaintext': !editMode }"
                  rows="2"
                ></textarea>
              </div>
              
              <div class="col-md-6">
                <label class="form-label text-muted small">PIN Code</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="formData.pin_code"
                  :readonly="!editMode"
                  :class="{ 'form-control-plaintext': !editMode }"
                  maxlength="6"
                >
              </div>
              
              <div class="col-md-6">
                <label class="form-label text-muted small">Member Since</label>
                <input 
                  type="text" 
                  class="form-control form-control-plaintext" 
                  :value="formatDate(profile.created_at)"
                  readonly
                >
              </div>
            </div>
            
            <div v-if="editMode" class="mt-4">
              <button type="submit" class="btn btn-primary" :disabled="saving">
                <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
                Save Changes
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, watch } from 'vue'
import { userApi } from '../../services/api'
import { showToast } from '../shared/Toast.vue'

export default {
  name: 'UserProfile',
  setup() {
    const loading = ref(false)
    const saving = ref(false)
    const editMode = ref(false)
    
    const profile = ref({
      username: '',
      full_name: '',
      email: '',
      vehicle_number: '',
      phone: '',
      address: '',
      pin_code: '',
      created_at: ''
    })
    
    const formData = reactive({
      full_name: '',
      email: '',
      vehicle_number: '',
      phone: '',
      address: '',
      pin_code: ''
    })
    
    const fetchProfile = async () => {
      loading.value = true
      try {
        const response = await userApi.getProfile()
        profile.value = response.data
        Object.assign(formData, {
          full_name: response.data.full_name || '',
          email: response.data.email || '',
          vehicle_number: response.data.vehicle_number || '',
          phone: response.data.phone || '',
          address: response.data.address || '',
          pin_code: response.data.pin_code || ''
        })
      } catch (error) {
        showToast('Failed to load profile', 'error')
      } finally {
        loading.value = false
      }
    }
    
    const saveProfile = async () => {
      saving.value = true
      try {
        const response = await userApi.updateProfile(formData)
        profile.value = response.data
        editMode.value = false
        showToast('Profile updated successfully', 'success')
        
        const storedUser = localStorage.getItem('user')
        if (storedUser) {
          const user = JSON.parse(storedUser)
          user.full_name = formData.full_name
          localStorage.setItem('user', JSON.stringify(user))
        }
      } catch (error) {
        showToast(error.response?.data?.error || 'Failed to update profile', 'error')
      } finally {
        saving.value = false
      }
    }
    
    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    watch(editMode, (newVal) => {
      if (!newVal) {
        Object.assign(formData, {
          full_name: profile.value.full_name || '',
          email: profile.value.email || '',
          vehicle_number: profile.value.vehicle_number || '',
          phone: profile.value.phone || '',
          address: profile.value.address || '',
          pin_code: profile.value.pin_code || ''
        })
      }
    })
    
    onMounted(fetchProfile)
    
    return {
      loading,
      saving,
      editMode,
      profile,
      formData,
      saveProfile,
      formatDate
    }
  }
}
</script>
