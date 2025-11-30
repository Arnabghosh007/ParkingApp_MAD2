<template>
  <div class="card border-0 modern-card">
    <div class="card-header modern-header">
      <h5 class="mb-0">
        <i class="bi bi-credit-card me-2"></i>
        Payment Portal
      </h5>
    </div>
    <div class="card-body p-4">
      <form @submit.prevent="processPayment">
        <div class="row">
          <div class="col-md-6">
            <div class="mb-3">
              <label class="form-label">Amount (₹)</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="formData.amount" 
                placeholder="Enter amount"
                step="0.01"
                required
              >
            </div>
          </div>
          <div class="col-md-6">
            <div class="mb-3">
              <label class="form-label">Booking ID (Optional)</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="formData.booking_id" 
                placeholder="Link to booking"
              >
            </div>
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label">Card Number</label>
          <input 
            type="text" 
            class="form-control" 
            v-model="formData.card_number" 
            placeholder="1234 5678 9012 3456"
            maxlength="16"
            required
          >
          <small class="text-muted">16 digits only</small>
        </div>

        <div class="row">
          <div class="col-md-6">
            <div class="mb-3">
              <label class="form-label">Expiry Date</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formData.expiry" 
                placeholder="MM/YY"
                maxlength="5"
                required
              >
            </div>
          </div>
          <div class="col-md-6">
            <div class="mb-3">
              <label class="form-label">CVV</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="formData.cvv" 
                placeholder="123"
                maxlength="4"
                required
              >
            </div>
          </div>
        </div>

        <div v-if="errorMessage" class="alert alert-danger py-2">
          {{ errorMessage }}
        </div>

        <div v-if="successMessage" class="alert alert-success py-2">
          {{ successMessage }}
        </div>

        <button 
          type="submit" 
          class="btn btn-primary w-100" 
          :disabled="loading"
        >
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          {{ loading ? 'Processing...' : 'Pay Now' }}
        </button>
      </form>

      <hr class="my-4">

      <div v-if="payments.length > 0">
        <h6 class="mb-3">Recent Transactions</h6>
        <div class="table-responsive">
          <table class="table table-sm table-hover">
            <thead class="table-light">
              <tr>
                <th>Amount</th>
                <th>Card</th>
                <th>Transaction ID</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="payment in payments" :key="payment.id">
                <td><strong>₹{{ payment.amount }}</strong></td>
                <td>{{ payment.card_number }}</td>
                <td><small>{{ payment.transaction_id }}</small></td>
                <td><small>{{ formatDate(payment.created_at) }}</small></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else class="text-center text-muted py-4">
        <i class="bi bi-inbox display-4"></i>
        <p class="mt-2">No payment transactions yet</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { userApi } from '../../services/api'
import { showToast } from '../shared/Toast.vue'

export default {
  name: 'PaymentForm',
  setup() {
    const formData = ref({
      amount: '',
      booking_id: null,
      card_number: '',
      expiry: '',
      cvv: ''
    })
    const payments = ref([])
    const loading = ref(false)
    const errorMessage = ref('')
    const successMessage = ref('')

    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      return new Date(dateStr).toLocaleDateString('en-IN')
    }

    const processPayment = async () => {
      errorMessage.value = ''
      successMessage.value = ''
      loading.value = true

      try {
        const response = await userApi.makePayment(formData.value)
        successMessage.value = 'Payment successful! Transaction ID: ' + response.data.payment.transaction_id
        showToast('Payment processed successfully', 'success')
        
        formData.value = {
          amount: '',
          booking_id: null,
          card_number: '',
          expiry: '',
          cvv: ''
        }
        
        await fetchPayments()
      } catch (error) {
        errorMessage.value = error.response?.data?.error || 'Payment failed'
        showToast(errorMessage.value, 'error')
      } finally {
        loading.value = false
      }
    }

    const fetchPayments = async () => {
      try {
        const response = await userApi.getPayments()
        payments.value = response.data.payments
      } catch (error) {
        console.error('Failed to load payments:', error)
      }
    }

    onMounted(fetchPayments)

    return {
      formData,
      payments,
      loading,
      errorMessage,
      successMessage,
      processPayment,
      formatDate
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

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  transform: translateY(-2px);
}

.table-hover tbody tr:hover {
  background-color: rgba(102, 126, 234, 0.05) !important;
}
</style>
