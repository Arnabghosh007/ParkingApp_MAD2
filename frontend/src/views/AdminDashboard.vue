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
      
      <div class="modern-tabs mb-4">
        <router-link 
          class="tab-link" 
          :class="{ active: activeTab === 'dashboard' }"
          :to="{ name: 'admin-tab', params: { tab: 'dashboard' } }"
        >
          <i class="bi bi-graph-up me-2"></i> Dashboard
        </router-link>
        <router-link 
          class="tab-link" 
          :class="{ active: activeTab === 'lots' }"
          :to="{ name: 'admin-tab', params: { tab: 'lots' } }"
        >
          <i class="bi bi-geo-alt me-2"></i> Parking Lots
        </router-link>
        <router-link 
          class="tab-link" 
          :class="{ active: activeTab === 'users' }"
          :to="{ name: 'admin-tab', params: { tab: 'users' } }"
        >
          <i class="bi bi-people me-2"></i> Users
        </router-link>
        <router-link 
          class="tab-link" 
          :class="{ active: activeTab === 'spots' }"
          :to="{ name: 'admin-tab', params: { tab: 'spots' } }"
        >
          <i class="bi bi-p-square-fill me-2"></i> Parking Spots
        </router-link>
        <router-link 
          class="tab-link" 
          :class="{ active: activeTab === 'charts' }"
          :to="{ name: 'admin-tab', params: { tab: 'charts' } }"
        >
          <i class="bi bi-bar-chart me-2"></i> Charts
        </router-link>
      </div>
      
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
.modern-tabs {
  display: flex;
  gap: 0.5rem;
  border-bottom: 2px solid #e9ecef;
  overflow-x: auto;
}

.tab-link {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  color: #6c757d;
  text-decoration: none;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
  white-space: nowrap;
  font-weight: 500;
}

.tab-link:hover {
  color: #667eea;
  border-bottom-color: #667eea;
}

.tab-link.active {
  color: #667eea;
  border-bottom-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
}
</style>
