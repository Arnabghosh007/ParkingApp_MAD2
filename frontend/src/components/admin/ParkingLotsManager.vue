<template>
  <div class="card border-0 modern-card">
    <div class="card-header modern-header d-flex justify-content-between align-items-center">
      <h5 class="mb-0">
        <i class="bi bi-geo-alt-fill me-2"></i>Parking Lots Management
      </h5>
      <button class="btn btn-primary btn-sm" @click="showAddModal = true">
        <i class="bi bi-plus-lg me-1"></i> Add New Lot
      </button>
    </div>
    <div class="card-body">
      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border text-primary"></div>
      </div>
      
      <div v-else-if="lots.length === 0" class="text-center py-4 text-muted">
        <i class="bi bi-geo-alt display-4"></i>
        <p class="mt-2">No parking lots found. Add your first lot!</p>
      </div>
      
      <div v-else class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Location Name</th>
              <th>Address</th>
              <th>PIN Code</th>
              <th>Price/Hour</th>
              <th>Spots</th>
              <th>Available</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lot in lots" :key="lot.id">
              <td>{{ lot.id }}</td>
              <td><strong>{{ lot.prime_location_name }}</strong></td>
              <td>{{ lot.address }}</td>
              <td>{{ lot.pin_code }}</td>
              <td>₹{{ lot.price }}</td>
              <td>{{ lot.number_of_spots }}</td>
              <td>
                <span class="badge" :class="lot.available_spots > 0 ? 'bg-success' : 'bg-danger'">
                  {{ lot.available_spots }}
                </span>
              </td>
              <td>
                <button class="btn btn-sm btn-outline-primary me-1" @click="editLot(lot)">
                  <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" @click="confirmDelete(lot)">
                  <i class="bi bi-trash"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  
  <div class="modal fade" :class="{ show: showAddModal || showEditModal }" 
       :style="{ display: (showAddModal || showEditModal) ? 'block' : 'none' }"
       tabindex="-1" @click.self="closeModal">
    <div class="modal-dialog">
      <div class="modal-content modern-modal">
        <div class="modal-header modern-modal-header">
          <h5 class="modal-title">
            <i :class="editingLot ? 'bi bi-pencil' : 'bi bi-plus-lg'" class="me-2"></i>
            {{ editingLot ? 'Edit Parking Lot' : 'Add New Parking Lot' }}
          </h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>
        <form @submit.prevent="saveLot">
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Location Name *</label>
              <input type="text" class="form-control" v-model="formData.prime_location_name" required>
            </div>
            
            <div class="mb-3">
              <label class="form-label">Address *</label>
              <textarea class="form-control" v-model="formData.address" required rows="2"></textarea>
            </div>
            
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">PIN Code *</label>
                <input type="text" class="form-control" v-model="formData.pin_code" required maxlength="6">
              </div>
              
              <div class="col-md-6 mb-3">
                <label class="form-label">Price per Hour *</label>
                <input type="number" class="form-control" v-model="formData.price" required min="0" step="0.01">
              </div>
            </div>
            
            <div class="mb-3">
              <label class="form-label">Number of Spots *</label>
              <input type="number" class="form-control" v-model="formData.number_of_spots" required min="1">
              <small class="text-muted">Spots will be auto-created</small>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
            <button type="submit" class="btn btn-primary" :disabled="saving">
              <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
              {{ editingLot ? 'Update' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
  <div v-if="showAddModal || showEditModal" class="modal-backdrop fade show"></div>
  
  <div class="modal fade" :class="{ show: showDeleteModal }" 
       :style="{ display: showDeleteModal ? 'block' : 'none' }"
       tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Confirm Delete</h5>
          <button type="button" class="btn-close" @click="showDeleteModal = false"></button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete <strong>{{ deletingLot?.prime_location_name }}</strong>?</p>
          <p class="text-muted">This action cannot be undone.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">Cancel</button>
          <button type="button" class="btn btn-danger" @click="deleteLot" :disabled="deleting">
            <span v-if="deleting" class="spinner-border spinner-border-sm me-1"></span>
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
  <div v-if="showDeleteModal" class="modal-backdrop fade show"></div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { adminApi } from '../../services/api'
import { showToast } from '../shared/Toast.vue'

export default {
  name: 'ParkingLotsManager',
  setup() {
    const lots = ref([])
    const loading = ref(false)
    const saving = ref(false)
    const deleting = ref(false)
    
    const showAddModal = ref(false)
    const showEditModal = ref(false)
    const showDeleteModal = ref(false)
    
    const editingLot = ref(null)
    const deletingLot = ref(null)
    
    const formData = reactive({
      prime_location_name: '',
      address: '',
      pin_code: '',
      price: 0,
      number_of_spots: 1
    })
    
    const fetchLots = async () => {
      loading.value = true
      try {
        const response = await adminApi.getParkingLots()
        lots.value = response.data
      } catch (error) {
        showToast('Failed to load parking lots', 'error')
      } finally {
        loading.value = false
      }
    }
    
    const resetForm = () => {
      formData.prime_location_name = ''
      formData.address = ''
      formData.pin_code = ''
      formData.price = 0
      formData.number_of_spots = 1
    }
    
    const closeModal = () => {
      showAddModal.value = false
      showEditModal.value = false
      editingLot.value = null
      resetForm()
    }
    
    const editLot = (lot) => {
      editingLot.value = lot
      formData.prime_location_name = lot.prime_location_name
      formData.address = lot.address
      formData.pin_code = lot.pin_code
      formData.price = lot.price
      formData.number_of_spots = lot.number_of_spots
      showEditModal.value = true
    }
    
    const saveLot = async () => {
      saving.value = true
      try {
        if (editingLot.value) {
          await adminApi.updateParkingLot(editingLot.value.id, formData)
          showToast('Parking lot updated successfully', 'success')
        } else {
          await adminApi.createParkingLot(formData)
          showToast('Parking lot created successfully', 'success')
        }
        closeModal()
        fetchLots()
      } catch (error) {
        showToast(error.response?.data?.error || 'Operation failed', 'error')
      } finally {
        saving.value = false
      }
    }
    
    const confirmDelete = (lot) => {
      deletingLot.value = lot
      showDeleteModal.value = true
    }
    
    const deleteLot = async () => {
      deleting.value = true
      try {
        await adminApi.deleteParkingLot(deletingLot.value.id)
        showToast('Parking lot deleted successfully', 'success')
        showDeleteModal.value = false
        deletingLot.value = null
        fetchLots()
      } catch (error) {
        showToast(error.response?.data?.error || 'Delete failed', 'error')
      } finally {
        deleting.value = false
      }
    }
    
    onMounted(fetchLots)
    
    return {
      lots,
      loading,
      saving,
      deleting,
      showAddModal,
      showEditModal,
      showDeleteModal,
      editingLot,
      deletingLot,
      formData,
      closeModal,
      editLot,
      saveLot,
      confirmDelete,
      deleteLot
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

.modern-modal {
  border-radius: 12px;
  border: none;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.modern-modal-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
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
