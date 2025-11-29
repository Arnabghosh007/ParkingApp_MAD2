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
      const hideNavbarRoutes = ['login', 'register']
      return !hideNavbarRoutes.includes(route.name)
    })
    
    return {
      showNavbar
    }
  }
}
</script>

<style>
#app-container {
  min-height: 100vh;
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
}

.stat-card:hover {
  transform: translateY(-5px);
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
</style>
