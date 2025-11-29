<template>
  <div class="dashboard-container">
    <div class="container-fluid">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">
          <i class="bi bi-speedometer2 text-primary me-2"></i>
          Admin Dashboard
        </h2>
        <span class="badge bg-primary">Administrator</span>
      </div>
      
      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <router-link 
            class="nav-link" 
            :class="{ active: activeTab === 'dashboard' }"
            :to="{ name: 'admin-tab', params: { tab: 'dashboard' } }"
          >
            <i class="bi bi-graph-up me-1"></i> Dashboard
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            class="nav-link" 
            :class="{ active: activeTab === 'lots' }"
            :to="{ name: 'admin-tab', params: { tab: 'lots' } }"
          >
            <i class="bi bi-geo-alt me-1"></i> Parking Lots
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            class="nav-link" 
            :class="{ active: activeTab === 'users' }"
            :to="{ name: 'admin-tab', params: { tab: 'users' } }"
          >
            <i class="bi bi-people me-1"></i> Users
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            class="nav-link" 
            :class="{ active: activeTab === 'spots' }"
            :to="{ name: 'admin-tab', params: { tab: 'spots' } }"
          >
            <i class="bi bi-p-square-fill me-1"></i> Parking Spots
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            class="nav-link" 
            :class="{ active: activeTab === 'charts' }"
            :to="{ name: 'admin-tab', params: { tab: 'charts' } }"
          >
            <i class="bi bi-bar-chart me-1"></i> Charts
          </router-link>
        </li>
      </ul>
      
      <div class="tab-content">
        <DashboardStats v-if="activeTab === 'dashboard'" />
        <ParkingLotsManager v-else-if="activeTab === 'lots'" />
        <UsersList v-else-if="activeTab === 'users'" />
        <ParkingSpots v-else-if="activeTab === 'spots'" />
        <AdminCharts v-else-if="activeTab === 'charts'" />
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import DashboardStats from '../components/admin/DashboardStats.vue'
import ParkingLotsManager from '../components/admin/ParkingLotsManager.vue'
import UsersList from '../components/admin/UsersList.vue'
import ParkingSpots from '../components/admin/ParkingSpots.vue'
import AdminCharts from '../components/admin/AdminCharts.vue'

export default {
  name: 'AdminDashboard',
  components: {
    DashboardStats,
    ParkingLotsManager,
    UsersList,
    ParkingSpots,
    AdminCharts
  },
  setup() {
    const route = useRoute()
    
    const activeTab = computed(() => {
      return route.params.tab || 'dashboard'
    })
    
    return {
      activeTab
    }
  }
}
</script>

<style scoped>
.nav-tabs .nav-link {
  color: #6c757d;
  border: none;
  border-bottom: 3px solid transparent;
  padding: 0.75rem 1.25rem;
}

.nav-tabs .nav-link:hover {
  border-color: transparent;
  color: #0d6efd;
}

.nav-tabs .nav-link.active {
  color: #0d6efd;
  background: transparent;
  border-color: transparent;
  border-bottom-color: #0d6efd;
}
</style>
