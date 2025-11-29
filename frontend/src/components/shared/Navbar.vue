<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
      <router-link class="navbar-brand" :to="dashboardRoute">
        <i class="bi bi-car-front-fill me-2"></i>
        Vehicle Parking App
      </router-link>
      
      <button 
        class="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <template v-if="isAdmin">
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'admin-tab', params: { tab: 'dashboard' } }">
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'admin-tab', params: { tab: 'lots' } }">
                Parking Lots
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'admin-tab', params: { tab: 'users' } }">
                Users
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'admin-tab', params: { tab: 'charts' } }">
                Charts
              </router-link>
            </li>
          </template>
          
          <template v-if="isUser">
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'user-tab', params: { tab: 'dashboard' } }">
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'user-tab', params: { tab: 'book' } }">
                Book Spot
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'user-tab', params: { tab: 'history' } }">
                History
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :to="{ name: 'user-tab', params: { tab: 'profile' } }">
                Profile
              </router-link>
            </li>
          </template>
        </ul>
        
        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a 
              class="nav-link dropdown-toggle" 
              href="#" 
              id="userDropdown" 
              role="button" 
              data-bs-toggle="dropdown"
            >
              <i class="bi bi-person-circle me-1"></i>
              {{ userName }}
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li>
                <span class="dropdown-item-text text-muted small">
                  {{ userRole }}
                </span>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li>
                <a class="dropdown-item" href="#" @click.prevent="handleLogout">
                  <i class="bi bi-box-arrow-right me-2"></i>
                  Logout
                </a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../../composables/useAuth'

export default {
  name: 'Navbar',
  setup() {
    const router = useRouter()
    const { user, isAdmin, isUser, logout } = useAuth()
    
    const userName = computed(() => {
      return user.value?.full_name || user.value?.username || 'User'
    })
    
    const userRole = computed(() => {
      return user.value?.role === 'admin' ? 'Administrator' : 'User'
    })
    
    const dashboardRoute = computed(() => {
      return isAdmin.value ? { name: 'admin' } : { name: 'user' }
    })
    
    const handleLogout = async () => {
      await logout()
      router.push({ name: 'login' })
    }
    
    return {
      user,
      isAdmin,
      isUser,
      userName,
      userRole,
      dashboardRoute,
      handleLogout
    }
  }
}
</script>

<style scoped>
.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-weight: 600;
}

.nav-link.active {
  font-weight: 500;
}
</style>
