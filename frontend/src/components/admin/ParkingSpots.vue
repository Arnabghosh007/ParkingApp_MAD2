<template>
  <div class="parking-spots-container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h4>
        <i class="bi bi-p-square-fill me-2 text-primary"></i>
        All Parking Spots
      </h4>
      <div class="input-group" style="max-width: 300px;">
        <input 
          v-model="searchLot" 
          type="text" 
          class="form-control" 
          placeholder="Filter by lot..."
        >
      </div>
    </div>
    
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary"></div>
    </div>
    
    <div v-else-if="filteredLots.length === 0" class="alert alert-info">
      No parking lots found
    </div>
    
    <div v-else class="row g-4">
      <div v-for="lot in filteredLots" :key="lot.id" class="col-md-6 col-lg-4">
        <div class="card h-100">
          <div class="card-header bg-light">
            <h6 class="mb-2">{{ lot.prime_location_name }}</h6>
            <small class="text-muted">₹{{ lot.price }}/hour • {{ getLotStats(lot.id).total }} total spots</small>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <div class="d-flex justify-content-between mb-2">
                <span class="small text-muted">Occupancy</span>
                <span class="badge" :class="getOccupancyBadge(lot.id)">
                  {{ getOccupancyPercent(lot.id) }}%
                </span>
              </div>
              <div class="progress" style="height: 20px;">
                <div 
                  class="progress-bar" 
                  :class="getOccupancyClass(lot.id)"
                  :style="{ width: getOccupancyPercent(lot.id) + '%' }"
                >
                </div>
              </div>
            </div>
            
            <div class="row text-center">
              <div class="col-6">
                <div class="stat-box">
                  <div class="stat-value text-success">{{ getLotStats(lot.id).available }}</div>
                  <div class="stat-label small text-muted">Available</div>
                </div>
              </div>
              <div class="col-6">
                <div class="stat-box">
                  <div class="stat-value text-danger">{{ getLotStats(lot.id).occupied }}</div>
                  <div class="stat-label small text-muted">Occupied</div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="expandedLots.includes(lot.id)" class="card-body border-top">
            <h6 class="mb-3 small text-muted">All Parking Spots</h6>
            <div class="row g-2">
              <div 
                v-for="spot in getSpotsByLot(lot.id)" 
                :key="spot.id"
                class="col-4"
              >
                <div 
                  class="spot-badge text-center p-2 rounded"
                  :class="spot.status === 'A' ? 'bg-success-light text-success' : 'bg-danger-light text-danger'"
                >
                  <div class="small fw-bold">Spot #{{ spot.id }}</div>
                  <div class="text-xs">
                    <i :class="spot.status === 'A' ? 'bi bi-check-circle' : 'bi bi-x-circle'"></i>
                    {{ spot.status === 'A' ? 'Available' : 'Occupied' }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="card-footer bg-white">
            <button 
              class="btn btn-sm btn-outline-primary w-100"
              @click="toggleSpots(lot.id)"
            >
              <i class="bi" :class="expandedLots.includes(lot.id) ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
              {{ expandedLots.includes(lot.id) ? 'Hide' : 'Show' }} Spots
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { adminApi } from '../../services/api'

export default {
  name: 'ParkingSpots',
  setup() {
    const loading = ref(false)
    const lots = ref([])
    const spots = ref([])
    const searchLot = ref('')
    const expandedLots = ref([])
    
    const filteredLots = computed(() => {
      return lots.value.filter(lot => 
        lot.prime_location_name.toLowerCase().includes(searchLot.value.toLowerCase())
      )
    })
    
    const fetchData = async () => {
      loading.value = true
      try {
        const [lotsRes, allSpots] = await Promise.all([
          adminApi.getParkingLots(),
          Promise.all([])
        ])
        lots.value = lotsRes.data
        
        // Fetch spots for each lot
        const allSpotsData = []
        for (const lot of lots.value) {
          const spotRes = await adminApi.getLotSpots(lot.id)
          allSpotsData.push(...spotRes.data.spots)
        }
        spots.value = allSpotsData
      } catch (error) {
        console.error('Failed to load data:', error)
      } finally {
        loading.value = false
      }
    }
    
    const getSpotsByLot = (lotId) => {
      return spots.value.filter(s => s.lot_id === lotId)
    }
    
    const getLotStats = (lotId) => {
      const lotSpots = getSpotsByLot(lotId)
      const available = lotSpots.filter(s => s.status === 'A').length
      const occupied = lotSpots.filter(s => s.status === 'O').length
      return {
        total: lotSpots.length,
        available,
        occupied
      }
    }
    
    const getOccupancyPercent = (lotId) => {
      const stats = getLotStats(lotId)
      if (stats.total === 0) return 0
      return Math.round((stats.occupied / stats.total) * 100)
    }
    
    const getOccupancyClass = (lotId) => {
      const percent = getOccupancyPercent(lotId)
      if (percent >= 80) return 'bg-danger'
      if (percent >= 50) return 'bg-warning'
      return 'bg-success'
    }
    
    const getOccupancyBadge = (lotId) => {
      const percent = getOccupancyPercent(lotId)
      if (percent >= 80) return 'bg-danger'
      if (percent >= 50) return 'bg-warning'
      return 'bg-success'
    }
    
    const toggleSpots = (lotId) => {
      const idx = expandedLots.value.indexOf(lotId)
      if (idx > -1) {
        expandedLots.value.splice(idx, 1)
      } else {
        expandedLots.value.push(lotId)
      }
    }
    
    onMounted(fetchData)
    
    return {
      loading,
      lots,
      spots,
      searchLot,
      expandedLots,
      filteredLots,
      getSpotsByLot,
      getLotStats,
      getOccupancyPercent,
      getOccupancyClass,
      getOccupancyBadge,
      toggleSpots
    }
  }
}
</script>

<style scoped>
.spot-badge {
  border: 2px solid currentColor;
  cursor: default;
}

.bg-success-light {
  background-color: rgba(25, 135, 84, 0.1) !important;
}

.bg-danger-light {
  background-color: rgba(220, 53, 69, 0.1) !important;
}

.stat-box {
  padding: 0.75rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
}

.stat-label {
  font-size: 0.75rem;
}
</style>
