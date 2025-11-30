<template>
  <div class="card border-0 modern-card">
    <div class="card-header modern-header">
      <h5 class="mb-0">
        <i class="bi bi-people-fill me-2"></i>Registered Users
      </h5>
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
              <th>Action</th>
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
              <td>
                <button 
                  class="btn btn-danger btn-sm" 
                  @click="deleteUser(user.id)"
                  :disabled="deleting === user.id"
                  title="Delete user"
                >
                  <span v-if="deleting === user.id" class="spinner-border spinner-border-sm me-1"></span>
                  <i v-else class="bi bi-trash me-1"></i>
                  Delete
                </button>
              </td>
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
    const deleting = ref(null)
    
    const fetchUsers = async () => {
      loading.value = true
      try {
        const response = await adminApi.getUsers()
        users.value = response
      } catch (error) {
        showToast('Failed to load users', 'error')
      } finally {
        loading.value = false
      }
    }
    
    const deleteUser = async (userId) => {
      if (!confirm('Are you sure you want to delete this user?')) return
      
      deleting.value = userId
      try {
        await adminApi.deleteUser(userId)
        users.value = users.value.filter(u => u.id !== userId)
        showToast('User deleted successfully', 'success')
      } catch (error) {
        showToast(error.response?.data?.error || 'Failed to delete user', 'error')
      } finally {
        deleting.value = null
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
      deleting,
      formatDate,
      deleteUser
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
</style>
