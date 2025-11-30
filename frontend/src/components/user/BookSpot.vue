<template>
  <div class="card border-0 shadow-sm">
    <div class="card-header bg-white">
      <h5 class="mb-0">
        <i class="bi bi-geo-alt-fill text-primary me-2"></i>
        Book a Parking Spot
      </h5>
    </div>
    <div class="card-body">
      <div v-if="hasActiveBooking" class="alert alert-warning">
        <i class="bi bi-exclamation-triangle me-2"></i>
        You already have an active booking. Please release it before booking a new spot.
      </div>
      
      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border text-primary"></div>
      </div>
      
      <div v-else-if="lots.length === 0" class="text-center py-4 text-muted">
        <i class="bi bi-geo-alt display-4"></i>
        <p class="mt-2">No parking lots available at the moment.</p>
      </div>
      
      <div v-else class="row g-4">
        <div class="col-md-6 col-lg-4" v-for="lot in lots" :key="lot.id">
          <div class="card h-100" :class="{ 'border-primary': selectedLot?.id === lot.id }">
            <div class="card-body">
              <h5 class="card-title">{{ lot.prime_location_name }}</h5>
              <p class="card-text text-muted small">{{ lot.address }}</p>
              
              <div class="d-flex justify-content-between mb-2">
                <span class="text-muted">Price:</span>
                <strong class="text-primary">₹{{ lot.price }}/hour</strong>
              </div>
              
              <div class="d-flex justify-content-between mb-3">
                <span class="text-muted">Available:</span>
                <span class="badge" :class="lot.available_spots > 0 ? 'bg-success' : 'bg-danger'">
                  {{ lot.available_spots }} / {{ lot.number_of_spots }}
                </span>
              </div>
              
              <button 
                class="btn w-100"
                :class="lot.available_spots > 0 ? 'btn-primary' : 'btn-secondary'"
                :disabled="lot.available_spots === 0 || hasActiveBooking"
                @click="selectLot(lot)"
              >
                {{ lot.available_spots > 0 ? 'Select' : 'Full' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <div class="modal fade" :class="{ show: showBookingModal }" 
       :style="{ display: showBookingModal ? 'block' : 'none' }"
       tabindex="-1" @click.self="showBookingModal = false">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Confirm Booking</h5>
          <button type="button" class="btn-close" @click="showBookingModal = false"></button>
        </div>
        <div class="modal-body">
          <div v-if="selectedLot" class="mb-3">
            <h6>Parking Lot</h6>
            <p class="text-muted mb-0">{{ selectedLot.prime_location_name }}</p>
            <small class="text-muted">{{ selectedLot.address }}</small>
          </div>
          
          <div class="mb-3">
            <h6>Rate</h6>
            <p class="text-primary mb-0">₹{{ selectedLot?.price }}/hour</p>
          </div>
          
          <div class="mb-3">
            <label class="form-label">
              Vehicle Number
              <span v-if="userVehicleNumber" class="badge bg-success ms-2">Registered</span>
            </label>
            <div v-if="userVehicleNumber && !vehicleNumber" class="alert alert-info py-2 mb-2">
              <i class="bi bi-info-circle me-1"></i>
              Using your registered vehicle: <strong>{{ userVehicleNumber }}</strong>
            </div>
            <input 
              type="text" 
              class="form-control" 
              v-model="vehicleNumber"
              :placeholder="userVehicleNumber ? `Current: ${userVehicleNumber}` : 'e.g., MH12AB1234'"
            >
            <small v-if="!userVehicleNumber && !vehicleNumber" class="text-danger">
              <i class="bi bi-exclamation-circle me-1"></i>
              Please enter a vehicle number to continue
            </small>
            <small v-else class="text-muted">Leave empty to use registered vehicle number</small>
          </div>
          
          <div class="alert alert-info small">
            <i class="bi bi-info-circle me-1"></i>
            A spot will be automatically allocated for you.
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="showBookingModal = false">Cancel</button>
          <button type="button" class="btn btn-primary" @click="confirmBooking" :disabled="booking">
            <span v-if="booking" class="spinner-border spinner-border-sm me-1"></span>
            Confirm Booking
          </button>
        </div>
      </div>
    </div>
  </div>
  <div v-if="showBookingModal" class="modal-backdrop fade show"></div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { sharedApi, userApi } from '../../services/api'
import { showToast } from '../shared/Toast.vue'

export default {
  name: 'BookSpot',
  emits: ['booked'],
  setup(props, { emit }) {
    const lots = ref([])
    const loading = ref(false)
    const booking = ref(false)
    const hasActiveBooking = ref(false)
    
    const selectedLot = ref(null)
    const showBookingModal = ref(false)
    const vehicleNumber = ref('')
    const userVehicleNumber = ref('')
    
    const fetchLots = async () => {
      loading.value = true
      try {
        const response = await sharedApi.getParkingLots()
        lots.value = response
      } catch (error) {
        showToast('Failed to load parking lots', 'error')
      } finally {
        loading.value = false
      }
    }
    
    const checkActiveBooking = async () => {
      try {
        const response = await userApi.getActiveBookings()
        hasActiveBooking.value = response && response.length > 0
      } catch (error) {
        console.error('Failed to check active booking:', error)
      }
    }
    
    const loadUserProfile = async () => {
      try {
        const response = await userApi.getProfile()
        userVehicleNumber.value = response.vehicle_number || ''
        vehicleNumber.value = ''
      } catch (error) {
        console.error('Failed to load user profile:', error)
      }
    }
    
    const selectLot = (lot) => {
      selectedLot.value = lot
      showBookingModal.value = true
    }
    
    const confirmBooking = async () => {
      if (!selectedLot.value) return
      
      const finalVehicleNumber = vehicleNumber.value || userVehicleNumber.value
      
      if (!finalVehicleNumber) {
        showToast('Please enter a vehicle number to continue', 'error')
        return
      }
      
      booking.value = true
      try {
        const data = {
          lot_id: selectedLot.value.id,
          vehicle_number: finalVehicleNumber
        }
        
        const response = await userApi.bookSpot(data)
        showToast('Spot booked successfully!', 'success')
        showBookingModal.value = false
        selectedLot.value = null
        vehicleNumber.value = ''
        hasActiveBooking.value = true
        emit('booked')
        fetchLots()
      } catch (error) {
        showToast(error.response?.data?.error || 'Booking failed', 'error')
      } finally {
        booking.value = false
      }
    }
    
    onMounted(() => {
      fetchLots()
      checkActiveBooking()
      loadUserProfile()
    })
    
    return {
      lots,
      loading,
      booking,
      hasActiveBooking,
      selectedLot,
      showBookingModal,
      vehicleNumber,
      userVehicleNumber,
      selectLot,
      confirmBooking
    }
  }
}
</script>
