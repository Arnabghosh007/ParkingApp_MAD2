<template>
  <div class="row g-4">
    <div class="col-md-3">
      <div class="card stat-card border-0">
        <div class="card-body d-flex align-items-center">
          <div class="stat-icon bg-primary bg-opacity-10 text-primary me-3">
            <i class="bi bi-calendar-check-fill"></i>
          </div>
          <div>
            <h6 class="text-muted mb-1">Total Bookings</h6>
            <h3 class="mb-0">{{ stats.total_bookings }}</h3>
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
            <h6 class="text-muted mb-1">Active Bookings</h6>
            <h3 class="mb-0">{{ stats.active_bookings }}</h3>
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
            <h6 class="text-muted mb-1">Total Spent</h6>
            <h3 class="mb-0">₹{{ stats.total_spent }}</h3>
          </div>
        </div>
      </div>
    </div>
    
    <div class="col-md-3">
      <div class="card stat-card border-0">
        <div class="card-body d-flex align-items-center">
          <div class="stat-icon bg-info bg-opacity-10 text-info me-3">
            <i class="bi bi-clock-fill"></i>
          </div>
          <div>
            <h6 class="text-muted mb-1">Total Hours</h6>
            <h3 class="mb-0">{{ stats.total_hours }}h</h3>
          </div>
        </div>
      </div>
    </div>
    
    <div class="col-md-6">
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white">
          <h5 class="mb-0">Parking Lot Usage</h5>
        </div>
        <div class="card-body">
          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border text-primary"></div>
          </div>
          <div v-else class="position-relative" style="height: 250px;">
            <canvas ref="usageChartRef"></canvas>
          </div>
        </div>
      </div>
    </div>
    
    <div class="col-md-6">
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white">
          <h5 class="mb-0">Booking Summary</h5>
        </div>
        <div class="card-body">
          <div v-if="loading" class="text-center py-4">
            <div class="spinner-border text-primary"></div>
          </div>
          <div v-else class="position-relative" style="height: 250px;">
            <canvas ref="summaryChartRef"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { Chart, registerables } from 'chart.js'
import { userApi } from '../../services/api'

Chart.register(...registerables)

export default {
  name: 'UserStats',
  setup() {
    const loading = ref(false)
    const stats = ref({
      total_bookings: 0,
      active_bookings: 0,
      completed_bookings: 0,
      total_spent: 0,
      total_hours: 0,
      lot_usage: {}
    })
    
    const usageChartRef = ref(null)
    const summaryChartRef = ref(null)
    
    let usageChart = null
    let summaryChart = null
    
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
        const response = await userApi.getStatsSummary()
        stats.value = response.data
        setTimeout(() => renderCharts(), 100)
      } catch (error) {
        console.error('Failed to load statistics:', error)
      } finally {
        loading.value = false
      }
    }
    
    const renderCharts = () => {
      const lotUsage = stats.value.lot_usage || {}
      const lotLabels = Object.keys(lotUsage)
      const lotData = Object.values(lotUsage)
      
      if (usageChartRef.value && lotLabels.length > 0) {
        if (usageChart) usageChart.destroy()
        usageChart = new Chart(usageChartRef.value, {
          type: 'doughnut',
          data: {
            labels: lotLabels,
            datasets: [{
              data: lotData,
              backgroundColor: colors.slice(0, lotLabels.length)
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
      
      if (summaryChartRef.value) {
        if (summaryChart) summaryChart.destroy()
        summaryChart = new Chart(summaryChartRef.value, {
          type: 'bar',
          data: {
            labels: ['Total', 'Completed', 'Active'],
            datasets: [{
              label: 'Bookings',
              data: [
                stats.value.total_bookings,
                stats.value.completed_bookings,
                stats.value.active_bookings
              ],
              backgroundColor: [
                'rgba(54, 162, 235, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(255, 206, 86, 0.8)'
              ]
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false }
            },
            scales: {
              y: { beginAtZero: true }
            }
          }
        })
      }
    }
    
    onMounted(fetchStats)
    
    onUnmounted(() => {
      if (usageChart) usageChart.destroy()
      if (summaryChart) summaryChart.destroy()
    })
    
    return {
      loading,
      stats,
      usageChartRef,
      summaryChartRef
    }
  }
}
</script>
