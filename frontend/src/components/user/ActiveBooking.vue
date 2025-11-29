<template>
  <div class="card border-0 modern-card">
    <div class="card-header modern-header">
      <h5 class="mb-0">
        <i class="bi bi-car-front-fill me-2"></i>
        Active Booking
      </h5>
    </div>
    <div class="card-body">
      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border text-primary"></div>
      </div>
      
      <div v-else-if="!activeBooking" class="text-center py-4">
        <i class="bi bi-p-circle display-4 text-muted"></i>
        <p class="mt-2 text-muted">No active booking</p>
        <router-link :to="{ name: 'user-tab', params: { tab: 'book' } }" class="btn btn-primary">
          Book a Spot Now
        </router-link>
      </div>
      
      <div v-else>
        <div class="row g-3">
          <div class="col-md-6">
            <div class="p-3 bg-light rounded">
              <small class="text-muted d-block">Parking Location</small>
              <strong>{{ activeBooking.lot_name || 'Parking Lot' }}</strong>
            </div>
          </div>
          
          <div class="col-md-6">
            <div class="p-3 bg-light rounded">
              <small class="text-muted d-block">Spot Number</small>
              <strong>Spot #{{ activeBooking.spot_id }}</strong>
            </div>
          </div>
          
          <div class="col-md-6">
            <div class="p-3 bg-light rounded">
              <small class="text-muted d-block">Vehicle Number</small>
              <strong>{{ activeBooking.vehicle_number }}</strong>
            </div>
          </div>
          
          <div class="col-md-6">
            <div class="p-3 bg-light rounded">
              <small class="text-muted d-block">Parked Since</small>
              <strong>{{ formatDate(activeBooking.parking_timestamp) }}</strong>
            </div>
          </div>
          
          <div class="col-12">
            <div class="p-3 bg-primary bg-opacity-10 rounded">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <small class="text-muted d-block">Duration</small>
                  <strong class="text-primary fs-4">{{ getDuration() }}</strong>
                </div>
                <div class="text-end">
                  <small class="text-muted d-block">Estimated Cost</small>
                  <strong class="text-primary fs-4">₹{{ getEstimatedCost() }}</strong>
                </div>
              </div>
            </div>
          </div>
          
          <div class="col-12 text-center mt-3">
            <button 
              class="btn btn-danger btn-lg" 
              @click="releaseSpot"
              :disabled="releasing"
            >
              <span v-if="releasing" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-box-arrow-right me-2"></i>
              Release Spot & Pay
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { userApi, sharedApi } from '../../services/api'
import { showToast } from '../shared/Toast.vue'

export default {
  name: 'ActiveBooking',
  emits: ['released'],
  setup(props, { emit }) {
    const loading = ref(false)
    const releasing = ref(false)
    const activeBooking = ref(null)
    const lotPrice = ref(0)
    let updateInterval = null
    
    const fetchActiveBooking = async () => {
      loading.value = true
      try {
        const response = await userApi.getActiveBookings()
        if (response.data && response.data.length > 0) {
          activeBooking.value = response.data[0]
          await fetchLotInfo()
        } else {
          activeBooking.value = null
        }
      } catch (error) {
        console.error('Failed to fetch active booking:', error)
      } finally {
        loading.value = false
      }
    }
    
    const fetchLotInfo = async () => {
      if (!activeBooking.value) return
      try {
        const response = await sharedApi.getParkingLots()
        const lots = response.data
        for (const lot of lots) {
          if (lot.parking_spots && lot.parking_spots.some(s => s.id === activeBooking.value.spot_id)) {
            lotPrice.value = lot.price
            activeBooking.value.lot_name = lot.prime_location_name
            break
          }
        }
      } catch (error) {
        console.error('Failed to fetch lot info:', error)
      }
    }
    
    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    const getDuration = () => {
      if (!activeBooking.value) return '0h 0m'
      const start = new Date(activeBooking.value.parking_timestamp)
      const now = new Date()
      const diff = Math.floor((now - start) / 1000)
      
      const hours = Math.floor(diff / 3600)
      const minutes = Math.floor((diff % 3600) / 60)
      
      return `${hours}h ${minutes}m`
    }
    
    const getEstimatedCost = () => {
      if (!activeBooking.value) return '0.00'
      const start = new Date(activeBooking.value.parking_timestamp)
      const now = new Date()
      const hours = (now - start) / (1000 * 60 * 60)
      return (hours * lotPrice.value).toFixed(2)
    }
    
    const releaseSpot = async () => {
      if (!activeBooking.value) return
      
      releasing.value = true
      try {
        const response = await userApi.releaseSpot(activeBooking.value.id)
        showToast(`Spot released! Total cost: ₹${response.data.cost}`, 'success')
        activeBooking.value = null
        emit('released')
      } catch (error) {
        showToast(error.response?.data?.error || 'Failed to release spot', 'error')
      } finally {
        releasing.value = false
      }
    }
    
    onMounted(() => {
      fetchActiveBooking()
      updateInterval = setInterval(() => {
        if (activeBooking.value) {
          activeBooking.value = { ...activeBooking.value }
        }
      }, 60000)
    })
    
    onUnmounted(() => {
      if (updateInterval) clearInterval(updateInterval)
    })
    
    return {
      loading,
      releasing,
      activeBooking,
      formatDate,
      getDuration,
      getEstimatedCost,
      releaseSpot
    }
  }
}
</script>

<style scoped>
.modern-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.modern-header {
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
  border-bottom: 2px solid #667eea20;
  padding: 1rem 1.5rem;
}

.btn-danger {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border: none;
  font-weight: 600;
}

.btn-danger:hover {
  background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
  transform: translateY(-2px);
}
</style>
