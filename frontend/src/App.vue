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
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  background: #f5f7fc;
}

.auth-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.auth-page::before {
  content: '';
  position: absolute;
  width: 400px;
  height: 400px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  top: -100px;
  left: -100px;
  animation: float 20s infinite ease-in-out;
}

.auth-page::after {
  content: '';
  position: absolute;
  width: 300px;
  height: 300px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 50%;
  bottom: -50px;
  right: -50px;
  animation: float 25s infinite ease-in-out reverse;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(20px); }
}

.dashboard-container {
  padding: 30px 20px;
  background: linear-gradient(135deg, #f5f7fc 0%, #f0f3ff 100%);
  min-height: calc(100vh - 56px);
}

.stat-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
  border: 1px solid rgba(102, 126, 234, 0.1);
  overflow: hidden;
  position: relative;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.stat-card:hover::before {
  transform: scaleX(1);
}

.stat-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.15);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.1) 100%);
  transition: all 0.3s ease;
}

.stat-card:hover .stat-icon {
  transform: scale(1.1) rotate(-5deg);
}

/* Global Button Styles */
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  letter-spacing: 0.5px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.btn-primary:active {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
}

.btn-outline-primary {
  color: #667eea;
  border-color: #667eea;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  letter-spacing: 0.5px;
}

.btn-outline-primary:hover {
  background: #667eea;
  border-color: #667eea;
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}

/* Card Styles */
.card {
  border: 1px solid rgba(102, 126, 234, 0.1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  border-radius: 16px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
}

.card:hover {
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.12);
  transform: translateY(-4px);
}

/* Form Styles */
.form-control {
  border: 1.5px solid #e5e7eb;
  border-radius: 12px;
  padding: 0.85rem 1.1rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
  font-weight: 500;
}

.form-control::placeholder {
  color: #a0aec0;
  font-weight: 400;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.3rem rgba(102, 126, 234, 0.15);
  background: white;
}

.form-label {
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.65rem;
  font-size: 0.95rem;
  letter-spacing: 0.3px;
}

/* Badge Styles */
.badge {
  padding: 0.65rem 1rem;
  border-radius: 8px;
  font-weight: 700;
  letter-spacing: 0.5px;
  font-size: 0.85rem;
}

/* Alert Styles */
.alert {
  border: none;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  border-left: 4px solid;
  transition: all 0.3s ease;
}

.alert-info {
  background: linear-gradient(135deg, #e3f2fd 0%, #e0f7ff 100%);
  color: #0d47a1;
  border-left-color: #1976d2;
}

.alert-success {
  background: linear-gradient(135deg, #e8f5e9 0%, #e0f9e8 100%);
  color: #1b5e20;
  border-left-color: #388e3c;
}

.alert-danger {
  background: linear-gradient(135deg, #ffebee 0%, #ffe0e0 100%);
  color: #b71c1c;
  border-left-color: #d32f2f;
}

.alert-warning {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe8cc 100%);
  color: #e65100;
  border-left-color: #f57c00;
}

/* Smooth Scrolling */
html {
  scroll-behavior: smooth;
}

/* Better Typography */
h1, h2, h3, h4, h5, h6 {
  letter-spacing: -0.5px;
  font-weight: 700;
}

p {
  line-height: 1.6;
  color: #4b5563;
}
</style>
