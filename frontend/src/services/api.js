// Fetch API wrapper with automatic token management
async function fetchWithAuth(url, options = {}) {
  const token = localStorage.getItem('access_token')
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  }
  
  if (token) {
    headers.Authorization = `Bearer ${token}`
  }
  
  let response = await fetch(url, { ...options, headers })
  
  // Handle token refresh on 401
  if (response.status === 401 && token) {
    const refreshToken = localStorage.getItem('refresh_token')
    if (refreshToken) {
      try {
        const refreshResponse = await fetch('/api/auth/refresh', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${refreshToken}` }
        })
        
        if (refreshResponse.ok) {
          const data = await refreshResponse.json()
          localStorage.setItem('access_token', data.access_token)
          
          // Retry original request with new token
          headers.Authorization = `Bearer ${data.access_token}`
          response = await fetch(url, { ...options, headers })
        } else {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user')
          window.location.href = '/login'
        }
      } catch (err) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        window.location.href = '/login'
      }
    }
  }
  
  return response
}

// Helper to handle JSON responses
async function handleResponse(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Request failed' }))
    const err = new Error(error.error || 'Request failed')
    err.response = { status: response.status, data: error }
    throw err
  }
  
  const contentType = response.headers.get('content-type')
  if (contentType && contentType.includes('application/json')) {
    return response.json()
  }
  return response.blob()
}

// Auth API
export const authApi = {
  login: async (username, password, role = 'user') => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, role })
    })
    return handleResponse(response)
  },
  
  register: async (userData) => {
    const response = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    })
    return handleResponse(response)
  },
  
  logout: async () => {
    const response = await fetchWithAuth('/api/auth/logout', { method: 'POST' })
    return handleResponse(response)
  },
  
  refresh: async () => {
    const token = localStorage.getItem('refresh_token')
    const response = await fetch('/api/auth/refresh', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    return handleResponse(response)
  }
}

// Admin API
export const adminApi = {
  getDashboard: async () => {
    const response = await fetchWithAuth('/api/admin/dashboard')
    return handleResponse(response)
  },
  
  getUsers: async () => {
    const response = await fetchWithAuth('/api/admin/users')
    return handleResponse(response)
  },
  
  deleteUser: async (userId) => {
    const response = await fetchWithAuth(`/api/admin/users/${userId}`, { method: 'DELETE' })
    return handleResponse(response)
  },
  
  getParkingLots: async () => {
    const response = await fetchWithAuth('/api/admin/parking-lots')
    return handleResponse(response)
  },
  
  createParkingLot: async (data) => {
    const response = await fetchWithAuth('/api/admin/parking-lots', {
      method: 'POST',
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },
  
  updateParkingLot: async (id, data) => {
    const response = await fetchWithAuth(`/api/admin/parking-lots/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },
  
  deleteParkingLot: async (id) => {
    const response = await fetchWithAuth(`/api/admin/parking-lots/${id}`, { method: 'DELETE' })
    return handleResponse(response)
  },
  
  getLotSpots: async (id) => {
    const response = await fetchWithAuth(`/api/admin/parking-lots/${id}/spots`)
    return handleResponse(response)
  },
  
  getStatsSummary: async () => {
    const response = await fetchWithAuth('/api/admin/stats/summary')
    return handleResponse(response)
  }
}

// User API
export const userApi = {
  getProfile: async () => {
    const response = await fetchWithAuth('/api/user/profile')
    return handleResponse(response)
  },
  
  updateProfile: async (data) => {
    const response = await fetchWithAuth('/api/user/profile', {
      method: 'PUT',
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },
  
  getActiveBookings: async () => {
    const response = await fetchWithAuth('/api/user/bookings')
    return handleResponse(response)
  },
  
  bookSpot: async (data) => {
    const response = await fetchWithAuth('/api/user/bookings', {
      method: 'POST',
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },
  
  releaseSpot: async (bookingId) => {
    const response = await fetchWithAuth(`/api/user/bookings/${bookingId}/release`, {
      method: 'POST'
    })
    return handleResponse(response)
  },
  
  getBookingHistory: async () => {
    const response = await fetchWithAuth('/api/user/bookings/history')
    return handleResponse(response)
  },
  
  getStatsSummary: async () => {
    const response = await fetchWithAuth('/api/user/stats/summary')
    return handleResponse(response)
  },
  
  triggerExport: async () => {
    const response = await fetchWithAuth('/api/user/export', { method: 'POST' })
    return handleResponse(response)
  },
  
  getExportStatus: async (jobId) => {
    const response = await fetchWithAuth(`/api/user/export/${jobId}`)
    return handleResponse(response)
  },
  
  downloadExport: async (jobId) => {
    const response = await fetchWithAuth(`/api/user/export/${jobId}/download`)
    return handleResponse(response)
  },
  
  makePayment: async (data) => {
    const response = await fetchWithAuth('/api/user/payments', {
      method: 'POST',
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },
  
  getPaymentHistory: async () => {
    const response = await fetchWithAuth('/api/user/payments/history')
    return handleResponse(response)
  }
}

// Shared API
export const sharedApi = {
  getParkingLots: async () => {
    const response = await fetch('/api/parking-lots')
    return handleResponse(response)
  },
  
  getParkingSpots: async () => {
    const response = await fetch('/api/parking-spots')
    return handleResponse(response)
  }
}
