<template>
  <div class="dashboard-container">
    <div class="container-fluid">
      
      <div class="tab-content">
        <div v-if="activeTab === 'dashboard'" class="row g-4">
          <div class="col-12">
            <UserStats :key="statsKey" />
          </div>
          <div class="col-12">
            <BookingSummary v-if="bookingSummary" :summary="bookingSummary" @reset="resetBookingSummary" :key="summaryKey" />
            <ActiveBooking v-else :key="bookingKey" @released="handleBookingChange" @booking-summary="handleBookingSummary" />
          </div>
        </div>
        
        <BookSpot 
          v-else-if="activeTab === 'book'" 
          :key="bookSpotKey" 
          @booked="handleBookingChange" 
        />
        <BookingHistory v-else-if="activeTab === 'history'" :key="historyKey" />
        <UserProfile v-else-if="activeTab === 'profile'" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import ActiveBooking from '../components/user/ActiveBooking.vue'
import BookSpot from '../components/user/BookSpot.vue'
import BookingHistory from '../components/user/BookingHistory.vue'
import UserStats from '../components/user/UserStats.vue'
import UserProfile from '../components/user/UserProfile.vue'
import BookingSummary from '../components/user/BookingSummary.vue'

export default {
  name: 'UserDashboard',
  components: {
    ActiveBooking,
    BookSpot,
    BookingHistory,
    UserStats,
    UserProfile,
    BookingSummary
  },
  setup() {
    const route = useRoute()
    
    const statsKey = ref(0)
    const bookingKey = ref(0)
    const bookSpotKey = ref(0)
    const historyKey = ref(0)
    const summaryKey = ref(0)
    const bookingSummary = ref(null)
    
    const activeTab = computed(() => {
      return route.params.tab || 'dashboard'
    })
    
    const handleBookingChange = () => {
      statsKey.value++
      bookingKey.value++
      bookSpotKey.value++
      historyKey.value++
      bookingSummary.value = null
    }
    
    const handleBookingSummary = (summary) => {
      bookingSummary.value = summary
      summaryKey.value++
    }
    
    const resetBookingSummary = () => {
      bookingSummary.value = null
      handleBookingChange()
    }
    
    return {
      activeTab,
      statsKey,
      bookingKey,
      bookSpotKey,
      historyKey,
      summaryKey,
      bookingSummary,
      handleBookingChange,
      handleBookingSummary,
      resetBookingSummary
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

.old-style {
  display: none;
}

.nav-tabs .nav-link {
  color: #6c757d;
  border: none;
  border-bottom: 3px solid transparent;
  padding: 0.75rem 1.25rem;
}

.nav-tabs .nav-link:hover {
  border-color: transparent;
  color: #0d6efd;
}

.nav-tabs .nav-link.active {
  color: #0d6efd;
  background: transparent;
  border-color: transparent;
  border-bottom-color: #0d6efd;
}
</style>
