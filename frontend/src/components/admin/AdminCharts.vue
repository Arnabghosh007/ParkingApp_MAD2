<template>
  <div class="row g-4">
    <div class="col-md-6">
      <div class="card border-0 modern-card">
        <div class="card-header modern-header">
          <h5 class="mb-0">
            <i class="bi bi-currency-rupee me-2"></i>Revenue by Parking Lot
          </h5>
        </div>
        <div class="card-body">
          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border text-primary"></div>
          </div>
          <div v-else class="position-relative" style="height: 300px;">
            <canvas ref="revenueChartRef"></canvas>
          </div>
        </div>
      </div>
    </div>
    
    <div class="col-md-6">
      <div class="card border-0 modern-card">
        <div class="card-header modern-header">
          <h5 class="mb-0">
            <i class="bi bi-bar-chart-fill me-2"></i>Bookings by Parking Lot
          </h5>
        </div>
        <div class="card-body">
          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border text-primary"></div>
          </div>
          <div v-else class="position-relative" style="height: 300px;">
            <canvas ref="bookingsChartRef"></canvas>
          </div>
        </div>
      </div>
    </div>
    
    <div class="col-md-6">
      <div class="card border-0 modern-card">
        <div class="card-header modern-header">
          <h5 class="mb-0">
            <i class="bi bi-pie-chart-fill me-2"></i>Spot Availability
          </h5>
        </div>
        <div class="card-body">
          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border text-primary"></div>
          </div>
          <div v-else class="position-relative" style="height: 300px;">
            <canvas ref="availabilityChartRef"></canvas>
          </div>
        </div>
      </div>
    </div>
    
    <div class="col-md-6">
      <div class="card border-0 modern-card">
        <div class="card-header modern-header">
          <h5 class="mb-0">
            <i class="bi bi-graph-up me-2"></i>Lot Statistics Summary
          </h5>
        </div>
        <div class="card-body">
          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border text-primary"></div>
          </div>
          <div v-else-if="lotStats.length === 0" class="text-center py-4 text-muted">
            <p>No data available</p>
          </div>
          <div v-else class="table-responsive">
            <table class="table table-sm">
              <thead>
                <tr>
                  <th>Lot</th>
                  <th>Bookings</th>
                  <th>Revenue</th>
                  <th>Occupancy</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="lot in lotStats" :key="lot.name">
                  <td>{{ lot.name }}</td>
                  <td>{{ lot.total_bookings }}</td>
                  <td>₹{{ lot.revenue }}</td>
                  <td>
                    <div class="progress" style="height: 20px;">
                      <div 
                        class="progress-bar" 
                        :class="getOccupancyClass(lot)"
                        :style="{ width: getOccupancyPercent(lot) + '%' }"
                      >
                        {{ getOccupancyPercent(lot) }}%
                      </div>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { Chart, registerables } from 'chart.js'
import { adminApi } from '../../services/api'

Chart.register(...registerables)

export default {
  name: 'AdminCharts',
  setup() {
    const loading = ref(false)
    const lotStats = ref([])
    
    const revenueChartRef = ref(null)
    const bookingsChartRef = ref(null)
    const availabilityChartRef = ref(null)
    
    let revenueChart = null
    let bookingsChart = null
    let availabilityChart = null
    
    const colors = [
      'rgba(54, 162, 235, 0.8)',
      'rgba(255, 99, 132, 0.8)',
      'rgba(75, 192, 192, 0.8)',
      'rgba(255, 206, 86, 0.8)',
      'rgba(153, 102, 255, 0.8)',
      'rgba(255, 159, 64, 0.8)'
    ]
    
    const fetchStats = async () => {
      loading.value = true
      try {
        const response = await adminApi.getStatsSummary()
        lotStats.value = response.data.lot_stats || []
        
        // Render charts when data is loaded and DOM is ready
        if (lotStats.value && lotStats.value.length > 0) {
          setTimeout(() => renderCharts(), 100)
        }
      } catch (error) {
        console.error('Failed to load statistics:', error)
        lotStats.value = []
      } finally {
        loading.value = false
      }
    }
    
    const renderCharts = () => {
      if (!lotStats.value || lotStats.value.length === 0) {
        console.log('No data to render charts')
        return
      }
      
      const labels = lotStats.value.map(l => l.name)
      const revenues = lotStats.value.map(l => l.revenue)
      const bookings = lotStats.value.map(l => l.total_bookings || 0)
      const available = lotStats.value.map(l => l.available || 0)
      const occupied = lotStats.value.map(l => l.occupied || 0)
      
      if (revenueChartRef.value) {
        if (revenueChart) revenueChart.destroy()
        revenueChart = new Chart(revenueChartRef.value, {
          type: 'bar',
          data: {
            labels,
            datasets: [{
              label: 'Revenue (₹)',
              data: revenues,
              backgroundColor: colors
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false }
            }
          }
        })
      }
      
      if (bookingsChartRef.value) {
        if (bookingsChart) bookingsChart.destroy()
        bookingsChart = new Chart(bookingsChartRef.value, {
          type: 'doughnut',
          data: {
            labels,
            datasets: [{
              data: bookings,
              backgroundColor: colors
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { position: 'bottom' }
            }
          }
        })
      }
      
      if (availabilityChartRef.value) {
        if (availabilityChart) availabilityChart.destroy()
        availabilityChart = new Chart(availabilityChartRef.value, {
          type: 'bar',
          data: {
            labels,
            datasets: [
              {
                label: 'Available',
                data: available,
                backgroundColor: 'rgba(75, 192, 192, 0.8)'
              },
              {
                label: 'Occupied',
                data: occupied,
                backgroundColor: 'rgba(255, 99, 132, 0.8)'
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: { stacked: true },
              y: { stacked: true }
            }
          }
        })
      }
    }
    
    const getOccupancyPercent = (lot) => {
      const total = lot.available + lot.occupied
      if (total === 0) return 0
      return Math.round((lot.occupied / total) * 100)
    }
    
    const getOccupancyClass = (lot) => {
      const percent = getOccupancyPercent(lot)
      if (percent >= 80) return 'bg-danger'
      if (percent >= 50) return 'bg-warning'
      return 'bg-success'
    }
    
    onMounted(fetchStats)
    
    onUnmounted(() => {
      if (revenueChart) revenueChart.destroy()
      if (bookingsChart) bookingsChart.destroy()
      if (availabilityChart) availabilityChart.destroy()
    })
    
    return {
      loading,
      lotStats,
      revenueChartRef,
      bookingsChartRef,
      availabilityChartRef,
      getOccupancyPercent,
      getOccupancyClass
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

.progress {
  border-radius: 6px;
  background-color: #e9ecef;
}

.progress-bar {
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.8rem;
}
</style>
