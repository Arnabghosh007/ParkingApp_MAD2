<template>
  <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 9999;">
    <div 
      v-for="(toast, index) in toasts" 
      :key="toast.id" 
      class="toast show" 
      :class="toastClass(toast.type)"
      role="alert"
    >
      <div class="toast-header" :class="headerClass(toast.type)">
        <i :class="iconClass(toast.type)" class="me-2"></i>
        <strong class="me-auto">{{ toast.title }}</strong>
        <button 
          type="button" 
          class="btn-close btn-close-white" 
          @click="removeToast(index)"
        ></button>
      </div>
      <div class="toast-body">
        {{ toast.message }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

const toasts = ref([])
let toastId = 0

export function showToast(message, type = 'info', title = null, duration = 3000) {
  const id = ++toastId
  
  const titles = {
    success: 'Success',
    error: 'Error',
    warning: 'Warning',
    info: 'Info'
  }
  
  toasts.value.push({
    id,
    message,
    type,
    title: title || titles[type] || 'Notification'
  })
  
  if (duration > 0) {
    setTimeout(() => {
      const index = toasts.value.findIndex(t => t.id === id)
      if (index > -1) {
        toasts.value.splice(index, 1)
      }
    }, duration)
  }
}

export default {
  name: 'Toast',
  setup() {
    const removeToast = (index) => {
      toasts.value.splice(index, 1)
    }
    
    const toastClass = (type) => {
      const classes = {
        success: 'border-success',
        error: 'border-danger',
        warning: 'border-warning',
        info: 'border-info'
      }
      return classes[type] || 'border-info'
    }
    
    const headerClass = (type) => {
      const classes = {
        success: 'bg-success text-white',
        error: 'bg-danger text-white',
        warning: 'bg-warning text-dark',
        info: 'bg-info text-white'
      }
      return classes[type] || 'bg-info text-white'
    }
    
    const iconClass = (type) => {
      const icons = {
        success: 'bi bi-check-circle-fill',
        error: 'bi bi-x-circle-fill',
        warning: 'bi bi-exclamation-triangle-fill',
        info: 'bi bi-info-circle-fill'
      }
      return icons[type] || 'bi bi-info-circle-fill'
    }
    
    return {
      toasts,
      removeToast,
      toastClass,
      headerClass,
      iconClass
    }
  }
}
</script>

<style scoped>
.toast {
  min-width: 300px;
}
</style>
