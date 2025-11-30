<template>
  <div class="card border-0 modern-card">
    <div class="card-header modern-header">
      <h5 class="mb-0">
        <i class="bi bi-check-circle-fill me-2 text-success"></i>
        Booking Completed
      </h5>
    </div>
    <div class="card-body p-5">
      <div v-if="!summary" class="text-center py-5">
        <i class="bi bi-p-circle display-4 text-muted"></i>
        <p class="mt-3 text-muted">No completed booking summary</p>
      </div>
      
      <div v-else>
        <div class="alert alert-success" role="alert">
          <i class="bi bi-check-circle me-2"></i>
          Your parking spot has been released successfully
        </div>
        
        <div class="row g-4 mt-3">
          <div class="col-md-6">
            <div class="summary-box">
              <small class="text-muted d-block mb-2">Parking Location</small>
              <h5 class="mb-0">{{ summary.lot_name || 'Parking Lot' }}</h5>
            </div>
          </div>
          
          <div class="col-md-6">
            <div class="summary-box">
              <small class="text-muted d-block mb-2">Spot Number</small>
              <h5 class="mb-0">Spot #{{ summary.spot_id }}</h5>
            </div>
          </div>
          
          <div class="col-md-6">
            <div class="summary-box">
              <small class="text-muted d-block mb-2">Vehicle Number</small>
              <h5 class="mb-0">{{ summary.vehicle_number }}</h5>
            </div>
          </div>
          
          <div class="col-md-6">
            <div class="summary-box">
              <small class="text-muted d-block mb-2">Check-in Time</small>
              <h5 class="mb-0">{{ formatDate(summary.parking_start) }}</h5>
            </div>
          </div>
          
          <div class="col-md-6">
            <div class="summary-box">
              <small class="text-muted d-block mb-2">Check-out Time</small>
              <h5 class="mb-0">{{ formatDate(summary.parking_end) }}</h5>
            </div>
          </div>
          
          <div class="col-md-6">
            <div class="summary-box">
              <small class="text-muted d-block mb-2">Parking Duration</small>
              <h5 class="mb-0">{{ summary.duration_hours }}h {{ summary.duration_minutes }}m</h5>
            </div>
          </div>
          
          <div class="col-12">
            <div class="summary-box bg-primary bg-opacity-10">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <small class="text-muted d-block mb-1">Hourly Rate</small>
                  <strong class="fs-5">₹{{ summary.hourly_rate }}/hour</strong>
                </div>
                <div class="text-end">
                  <small class="text-muted d-block mb-1">Total Amount</small>
                  <strong class="fs-3 text-primary">₹{{ summary.total_cost }}</strong>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="mt-4 text-center">
          <button class="btn btn-primary" @click="resetSummary">
            <i class="bi bi-arrow-left me-2"></i>
            Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  name: 'BookingSummary',
  props: {
    summary: {
      type: Object,
      default: null
    }
  },
  emits: ['reset'],
  setup(props, { emit }) {
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
    
    const resetSummary = () => {
      emit('reset')
    }
    
    return {
      formatDate,
      resetSummary
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
  background: linear-gradient(135deg, #51cf66 0%, #37b24d 100%);
  border-bottom: none;
  padding: 1.5rem;
  color: white;
}

.modern-header h5 {
  color: white;
  margin: 0;
}

.summary-box {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.summary-box h5 {
  color: #212529;
  font-weight: 600;
}

.summary-box small {
  color: #6c757d;
}

.bg-primary.bg-opacity-10 {
  border-left: 4px solid #667eea;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  padding: 0.75rem 2rem;
  font-weight: 600;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
</style>
