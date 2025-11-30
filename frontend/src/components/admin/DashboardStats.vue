<template>
  <div class="row g-4">
    <div class="col-md-3">
      <div class="card stat-card border-0">
        <div class="card-body d-flex align-items-center">
          <div class="stat-icon bg-primary bg-opacity-10 text-primary me-3">
            <i class="bi bi-geo-alt-fill"></i>
          </div>
          <div>
            <h6 class="text-muted mb-1">Parking Lots</h6>
            <h3 class="mb-0">{{ stats.total_lots }}</h3>
          </div>
        </div>
      </div>
    </div>
    
    <div class="col-md-3">
      <div class="card stat-card border-0">
        <div class="card-body d-flex align-items-center">
          <div class="stat-icon bg-success bg-opacity-10 text-success me-3">
            <i class="bi bi-p-square-fill"></i>
          </div>
          <div>
            <h6 class="text-muted mb-1">Total Spots</h6>
            <h3 class="mb-0">{{ stats.total_spots }}</h3>
          </div>
        </div>
      </div>
    </div>
    
    <div class="col-md-3">
      <div class="card stat-card border-0">
        <div class="card-body d-flex align-items-center">
          <div class="stat-icon bg-warning bg-opacity-10 text-warning me-3">
            <i class="bi bi-car-front-fill"></i>
          </div>
          <div>
            <h6 class="text-muted mb-1">Occupied</h6>
            <h3 class="mb-0">{{ stats.occupied_spots }}</h3>
          </div>
        </div>
      </div>
    </div>
    
    <div class="col-md-3">
      <div class="card stat-card border-0">
        <div class="card-body d-flex align-items-center">
          <div class="stat-icon bg-info bg-opacity-10 text-info me-3">
            <i class="bi bi-check-circle-fill"></i>
          </div>
          <div>
            <h6 class="text-muted mb-1">Available</h6>
            <h3 class="mb-0">{{ stats.available_spots }}</h3>
          </div>
        </div>
      </div>
    </div>
    
    <div class="col-md-3">
      <div class="card stat-card border-0">
        <div class="card-body d-flex align-items-center">
          <div class="stat-icon bg-secondary bg-opacity-10 text-secondary me-3">
            <i class="bi bi-people-fill"></i>
          </div>
          <div>
            <h6 class="text-muted mb-1">Total Users</h6>
            <h3 class="mb-0">{{ stats.total_users }}</h3>
          </div>
        </div>
      </div>
    </div>
    
    <div class="col-md-3">
      <div class="card stat-card border-0">
        <div class="card-body d-flex align-items-center">
          <div class="stat-icon bg-danger bg-opacity-10 text-danger me-3">
            <i class="bi bi-calendar-check-fill"></i>
          </div>
          <div>
            <h6 class="text-muted mb-1">Today's Bookings</h6>
            <h3 class="mb-0">{{ stats.today_bookings }}</h3>
          </div>
        </div>
      </div>
    </div>
    
    <div class="col-md-3">
      <div class="card stat-card border-0">
        <div class="card-body d-flex align-items-center">
          <div class="stat-icon bg-success bg-opacity-10 text-success me-3">
            <i class="bi bi-currency-rupee"></i>
          </div>
          <div>
            <h6 class="text-muted mb-1">Total Revenue</h6>
            <h3 class="mb-0">₹{{ stats.total_revenue }}</h3>
          </div>
        </div>
      </div>
    </div>
    
    <div class="col-md-3">
      <div class="card stat-card border-0">
        <div class="card-body d-flex align-items-center">
          <div class="stat-icon bg-primary bg-opacity-10 text-primary me-3">
            <i class="bi bi-pie-chart-fill"></i>
          </div>
          <div>
            <h6 class="text-muted mb-1">Occupancy Rate</h6>
            <h3 class="mb-0">{{ stats.occupancy_rate }}%</h3>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stat-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  background: white;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}
</style>

<script>
import { ref, onMounted } from 'vue'
import { adminApi } from '../../services/api'
import { showToast } from '../shared/Toast.vue'

export default {
  name: 'DashboardStats',
  setup() {
    const stats = ref({
      total_lots: 0,
      total_spots: 0,
      available_spots: 0,
      occupied_spots: 0,
      total_users: 0,
      today_bookings: 0,
      total_revenue: 0,
      occupancy_rate: 0
    })
    
    const loading = ref(false)
    
    const fetchStats = async () => {
      loading.value = true
      try {
        const response = await adminApi.getDashboard()
        stats.value = response
      } catch (error) {
        showToast('Failed to load dashboard stats', 'error')
      } finally {
        loading.value = false
      }
    }
    
    onMounted(fetchStats)
    
    return {
      stats,
      loading
    }
  }
}
</script>
