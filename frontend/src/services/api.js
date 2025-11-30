import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const response = await axios.post('/api/auth/refresh', {}, {
            headers: { Authorization: `Bearer ${refreshToken}` }
          })
          
          const { access_token } = response.data
          localStorage.setItem('access_token', access_token)
          
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return api(originalRequest)
        } catch (refreshError) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user')
          window.location.href = '/login'
          return Promise.reject(refreshError)
        }
      } else {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        window.location.href = '/login'
      }
    }
    
    return Promise.reject(error)
  }
)

export const authApi = {
  login: (username, password, role = 'user') => 
    api.post('/auth/login', { username, password, role }),
  
  register: (userData) => 
    api.post('/auth/register', userData),
  
  logout: () => 
    api.post('/auth/logout'),
  
  refresh: () => 
    api.post('/auth/refresh')
}

export const adminApi = {
  getDashboard: () => 
    api.get('/admin/dashboard'),
  
  getUsers: () => 
    api.get('/admin/users'),
  
  getParkingLots: () => 
    api.get('/admin/parking-lots'),
  
  createParkingLot: (data) => 
    api.post('/admin/parking-lots', data),
  
  updateParkingLot: (id, data) => 
    api.put(`/admin/parking-lots/${id}`, data),
  
  deleteParkingLot: (id) => 
    api.delete(`/admin/parking-lots/${id}`),
  
  getLotSpots: (id) => 
    api.get(`/admin/parking-lots/${id}/spots`),
  
  getStatsSummary: () => 
    api.get('/admin/stats/summary')
}

export const userApi = {
  getProfile: () => 
    api.get('/user/profile'),
  
  updateProfile: (data) => 
    api.put('/user/profile', data),
  
  getActiveBookings: () => 
    api.get('/user/bookings'),
  
  bookSpot: (data) => 
    api.post('/user/bookings', data),
  
  releaseSpot: (bookingId) => 
    api.post(`/user/bookings/${bookingId}/release`),
  
  getBookingHistory: () => 
    api.get('/user/bookings/history'),
  
  getStatsSummary: () => 
    api.get('/user/stats/summary'),
  
  triggerExport: () => 
    api.post('/user/export'),
  
  getExportStatus: (jobId) => 
    api.get(`/user/export/${jobId}`),
  
  downloadExport: async (jobId) => {
    const response = await api.get(`/user/export/${jobId}/download`, { responseType: 'blob' })
    return response.data
  }
}

export const sharedApi = {
  getParkingLots: () => 
    api.get('/parking-lots'),
  
  getParkingLotDetail: (id) => 
    api.get(`/parking-lots/${id}`)
}

export default api
