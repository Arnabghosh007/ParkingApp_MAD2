<template>
  <div class="dashboard-container">
    <div class="container-fluid">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">
          <i class="bi bi-house-door-fill text-primary me-2"></i>
          My Dashboard
        </h2>
        <span class="badge bg-success">User</span>
      </div>
      
      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <router-link 
            class="nav-link" 
            :class="{ active: activeTab === 'dashboard' }"
            :to="{ name: 'user-tab', params: { tab: 'dashboard' } }"
          >
            <i class="bi bi-house-door me-1"></i> Dashboard
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            class="nav-link" 
            :class="{ active: activeTab === 'book' }"
            :to="{ name: 'user-tab', params: { tab: 'book' } }"
          >
            <i class="bi bi-plus-circle me-1"></i> Book Spot
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            class="nav-link" 
            :class="{ active: activeTab === 'history' }"
            :to="{ name: 'user-tab', params: { tab: 'history' } }"
          >
            <i class="bi bi-clock-history me-1"></i> History
          </router-link>
        </li>
        <li class="nav-item">
          <router-link 
            class="nav-link" 
            :class="{ active: activeTab === 'profile' }"
            :to="{ name: 'user-tab', params: { tab: 'profile' } }"
          >
            <i class="bi bi-person me-1"></i> Profile
          </router-link>
        </li>
      </ul>
      
      <div class="tab-content">
        <div v-if="activeTab === 'dashboard'" class="row g-4">
          <div class="col-12">
            <UserStats :key="statsKey" />
          </div>
          <div class="col-12">
            <ActiveBooking :key="bookingKey" @released="handleBookingChange" />
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

export default {
  name: 'UserDashboard',
  components: {
    ActiveBooking,
    BookSpot,
    BookingHistory,
    UserStats,
    UserProfile
  },
  setup() {
    const route = useRoute()
    
    const statsKey = ref(0)
    const bookingKey = ref(0)
    const bookSpotKey = ref(0)
    const historyKey = ref(0)
    
    const activeTab = computed(() => {
      return route.params.tab || 'dashboard'
    })
    
    const handleBookingChange = () => {
      statsKey.value++
      bookingKey.value++
      bookSpotKey.value++
      historyKey.value++
    }
    
    return {
      activeTab,
      statsKey,
      bookingKey,
      bookSpotKey,
      historyKey,
      handleBookingChange
    }
  }
}
</script>

<style scoped>
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
