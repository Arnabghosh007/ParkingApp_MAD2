<template>
  <div class="card border-0 modern-card">
    <div class="card-header modern-header d-flex justify-content-between align-items-center">
      <h5 class="mb-0">
        <i class="bi bi-clock-history me-2"></i>
        Booking History
      </h5>
      <button class="btn btn-outline-primary btn-sm" @click="exportHistory" :disabled="exporting">
        <span v-if="exporting" class="spinner-border spinner-border-sm me-1"></span>
        <i v-else class="bi bi-download me-1"></i>
        Export CSV
      </button>
    </div>
    <div class="card-body">
      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border text-primary"></div>
      </div>
      
      <div v-else-if="bookings.length === 0" class="text-center py-4 text-muted">
        <i class="bi bi-clock-history display-4"></i>
        <p class="mt-2">No booking history found.</p>
      </div>
      
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Spot</th>
              <th>Vehicle</th>
              <th>Parking Time</th>
              <th>Leaving Time</th>
              <th>Duration</th>
              <th>Cost</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="booking in bookings" :key="booking.id">
              <td>{{ booking.id }}</td>
              <td>Spot #{{ booking.spot_id }}</td>
              <td>
                <span class="badge bg-secondary">{{ booking.vehicle_number }}</span>
              </td>
              <td>{{ formatDate(booking.parking_timestamp) }}</td>
              <td>{{ booking.leaving_timestamp ? formatDate(booking.leaving_timestamp) : '-' }}</td>
              <td>{{ getDuration(booking) }}</td>
              <td>
                <span v-if="booking.parking_cost" class="text-success">
                  ₹{{ booking.parking_cost }}
                </span>
                <span v-else class="text-muted">-</span>
              </td>
              <td>
                <span class="badge" :class="booking.leaving_timestamp ? 'bg-success' : 'bg-warning'">
                  {{ booking.leaving_timestamp ? 'Completed' : 'Active' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div v-if="bookings.length > 0" class="mt-3">
        <div class="row text-center">
          <div class="col-md-4">
            <div class="p-3 bg-light rounded">
              <h4 class="mb-0">{{ bookings.length }}</h4>
              <small class="text-muted">Total Bookings</small>
            </div>
          </div>
          <div class="col-md-4">
            <div class="p-3 bg-light rounded">
              <h4 class="mb-0 text-success">₹{{ totalSpent }}</h4>
              <small class="text-muted">Total Spent</small>
            </div>
          </div>
          <div class="col-md-4">
            <div class="p-3 bg-light rounded">
              <h4 class="mb-0 text-primary">{{ totalHours }}h</h4>
              <small class="text-muted">Total Hours Parked</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { userApi } from '../../services/api'
import { showToast } from '../shared/Toast.vue'

export default {
  name: 'BookingHistory',
  setup() {
    const bookings = ref([])
    const loading = ref(false)
    const exporting = ref(false)
    
    const fetchHistory = async () => {
      loading.value = true
      try {
        const response = await userApi.getBookingHistory()
        bookings.value = response
      } catch (error) {
        showToast('Failed to load booking history', 'error')
      } finally {
        loading.value = false
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
    
    const getDuration = (booking) => {
      const start = new Date(booking.parking_timestamp)
      const end = booking.leaving_timestamp ? new Date(booking.leaving_timestamp) : new Date()
      const diff = Math.floor((end - start) / 1000)
      
      const hours = Math.floor(diff / 3600)
      const minutes = Math.floor((diff % 3600) / 60)
      
      return `${hours}h ${minutes}m`
    }
    
    const totalSpent = computed(() => {
      return bookings.value
        .reduce((sum, b) => sum + (b.parking_cost || 0), 0)
        .toFixed(2)
    })
    
    const totalHours = computed(() => {
      let total = 0
      bookings.value.forEach(b => {
        const start = new Date(b.parking_timestamp)
        const end = b.leaving_timestamp ? new Date(b.leaving_timestamp) : new Date()
        total += (end - start) / (1000 * 60 * 60)
      })
      return Math.round(total)
    })
    
    const exportHistory = async () => {
      exporting.value = true
      try {
        const response = await userApi.triggerExport()
        const job = response.job
        
        const downloadFile = (blob) => {
          const url = window.URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = 'parking_history.csv'
          a.click()
          window.URL.revokeObjectURL(url)
        }
        
        if (job.status === 'completed') {
          const blob = await userApi.downloadExport(job.id)
          downloadFile(blob)
          showToast('Export downloaded successfully', 'success')
        } else {
          showToast('Export started. Please wait...', 'info')
          setTimeout(async () => {
            try {
              const statusResponse = await userApi.getExportStatus(job.id)
              if (statusResponse.status === 'completed') {
                const blob = await userApi.downloadExport(job.id)
                downloadFile(blob)
                showToast('Export downloaded successfully', 'success')
              } else {
                showToast('Export is still processing', 'info')
              }
            } catch (e) {
              showToast('Export is still processing', 'info')
            }
          }, 3000)
        }
      } catch (error) {
        showToast('Failed to export history', 'error')
      } finally {
        exporting.value = false
      }
    }
    
    onMounted(fetchHistory)
    
    return {
      bookings,
      loading,
      exporting,
      formatDate,
      getDuration,
      totalSpent,
      totalHours,
      exportHistory
    }
  }
}
</script>

<style scoped>
.modern-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  overflow: hidden;
}

.modern-header {
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
  border-bottom: 2px solid #667eea20;
  padding: 1rem 1.5rem;
}

.table-hover tbody tr:hover {
  background-color: rgba(102, 126, 234, 0.05) !important;
}

.badge {
  border-radius: 6px;
  padding: 0.4rem 0.8rem;
  font-weight: 600;
}

.bg-light {
  background-color: rgba(102, 126, 234, 0.08) !important;
  border-radius: 8px;
}
</style>
