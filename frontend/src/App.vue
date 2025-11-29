<template>
  <div id="app-container">
    <Navbar v-if="showNavbar" />
    <Toast ref="toast" />
    <router-view />
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/shared/Navbar.vue'
import Toast from './components/shared/Toast.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    Toast
  },
  setup() {
    const route = useRoute()
    
    const showNavbar = computed(() => {
      const hideNavbarRoutes = ['login', 'register', 'landing']
      return !hideNavbarRoutes.includes(route.name)
    })
    
    return {
      showNavbar
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app-container {
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.auth-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.dashboard-container {
  padding: 20px;
  background-color: #f8f9fa;
  min-height: calc(100vh - 56px);
}

.stat-card {
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  background: white;
  border: none;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

/* Global Button Styles */
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 15px rgba(102, 126, 234, 0.4);
}

.btn-outline-primary {
  color: #667eea;
  border-color: #667eea;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  background: #667eea;
  border-color: #667eea;
  transform: translateY(-2px);
}

/* Card Styles */
.card {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

/* Form Styles */
.form-control {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.form-label {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

/* Badge Styles */
.badge {
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-weight: 600;
}

/* Alert Styles */
.alert {
  border: none;
  border-radius: 8px;
  padding: 1rem 1.25rem;
}

.alert-info {
  background: #e3f2fd;
  color: #1565c0;
}

.alert-success {
  background: #e8f5e9;
  color: #2e7d32;
}

.alert-danger {
  background: #ffebee;
  color: #c62828;
}

.alert-warning {
  background: #fff3e0;
  color: #e65100;
}
</style>
