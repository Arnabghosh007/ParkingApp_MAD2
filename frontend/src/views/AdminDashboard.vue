<template>
  <div class="dashboard-container">
    <div class="container-fluid">
      
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
