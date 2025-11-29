<template>
  <div class="card border-0 shadow-sm">
    <div class="card-header bg-white">
      <h5 class="mb-0">Registered Users</h5>
    </div>
    <div class="card-body">
      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border text-primary"></div>
      </div>
      
      <div v-else-if="users.length === 0" class="text-center py-4 text-muted">
        <i class="bi bi-people display-4"></i>
        <p class="mt-2">No users registered yet.</p>
      </div>
      
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Full Name</th>
              <th>Email</th>
              <th>Vehicle Number</th>
              <th>Phone</th>
              <th>Last Visit</th>
              <th>Joined</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td><strong>{{ user.username }}</strong></td>
              <td>{{ user.full_name || '-' }}</td>
              <td>{{ user.email || '-' }}</td>
              <td>
                <span v-if="user.vehicle_number" class="badge bg-secondary">
                  {{ user.vehicle_number }}
                </span>
                <span v-else class="text-muted">-</span>
              </td>
              <td>{{ user.phone || '-' }}</td>
              <td>{{ formatDate(user.last_visit) }}</td>
              <td>{{ formatDate(user.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div v-if="users.length > 0" class="mt-3 text-muted small">
        Total: {{ users.length }} users
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { adminApi } from '../../services/api'
import { showToast } from '../shared/Toast.vue'

export default {
  name: 'UsersList',
  setup() {
    const users = ref([])
    const loading = ref(false)
    
    const fetchUsers = async () => {
      loading.value = true
      try {
        const response = await adminApi.getUsers()
        users.value = response.data
      } catch (error) {
        showToast('Failed to load users', 'error')
      } finally {
        loading.value = false
      }
    }
    
    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    onMounted(fetchUsers)
    
    return {
      users,
      loading,
      formatDate
    }
  }
}
</script>
