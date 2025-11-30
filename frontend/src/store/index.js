import { createStore } from 'vuex'

const store = createStore({
  state() {
    const storedUser = localStorage.getItem('user')
    let user = null
    
    if (storedUser) {
      try {
        user = JSON.parse(storedUser)
      } catch (e) {
        localStorage.removeItem('user')
      }
    }
    
    return {
      user,
      accessToken: localStorage.getItem('access_token') || null,
      refreshToken: localStorage.getItem('refresh_token') || null,
      loading: false,
      error: null
    }
  },
  
  getters: {
    isAuthenticated: (state) => !!state.user && !!state.accessToken,
    isAdmin: (state) => state.user?.role === 'admin',
    isUser: (state) => state.user?.role === 'user',
    currentUser: (state) => state.user,
    authLoading: (state) => state.loading,
    authError: (state) => state.error
  },
  
  mutations: {
    setUser(state, user) {
      state.user = user
      if (user) {
        localStorage.setItem('user', JSON.stringify(user))
      } else {
        localStorage.removeItem('user')
      }
    },
    
    setAccessToken(state, token) {
      state.accessToken = token
      if (token) {
        localStorage.setItem('access_token', token)
      } else {
        localStorage.removeItem('access_token')
      }
    },
    
    setRefreshToken(state, token) {
      state.refreshToken = token
      if (token) {
        localStorage.setItem('refresh_token', token)
      } else {
        localStorage.removeItem('refresh_token')
      }
    },
    
    setLoading(state, loading) {
      state.loading = loading
    },
    
    setError(state, error) {
      state.error = error
    },
    
    clearAuth(state) {
      state.user = null
      state.accessToken = null
      state.refreshToken = null
      state.error = null
      localStorage.removeItem('user')
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  },
  
  actions: {
    async login({ commit }, { username, password, role = 'user' }) {
      commit('setLoading', true)
      commit('setError', null)
      
      try {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password, role })
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.error || 'Login failed')
        }
        
        const data = await response.json()
        const { access_token, refresh_token, user: userData } = data
        
        commit('setAccessToken', access_token)
        commit('setRefreshToken', refresh_token)
        commit('setUser', { ...userData, role })
        
        return { success: true, user: { ...userData, role } }
      } catch (err) {
        const errorMsg = err.message || 'Login failed'
        commit('setError', errorMsg)
        return { success: false, error: errorMsg }
      } finally {
        commit('setLoading', false)
      }
    },
    
    async register({ commit }, userData) {
      commit('setLoading', true)
      commit('setError', null)
      
      try {
        const response = await fetch('/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(userData)
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.error || 'Registration failed')
        }
        
        const data = await response.json()
        const { access_token, refresh_token, user: newUser } = data
        
        commit('setAccessToken', access_token)
        commit('setRefreshToken', refresh_token)
        commit('setUser', { ...newUser, role: 'user' })
        
        return { success: true, user: { ...newUser, role: 'user' } }
      } catch (err) {
        const errorMsg = err.message || 'Registration failed'
        commit('setError', errorMsg)
        return { success: false, error: errorMsg }
      } finally {
        commit('setLoading', false)
      }
    },
    
    async logout({ commit }) {
      try {
        const token = localStorage.getItem('access_token')
        if (token) {
          await fetch('/api/auth/logout', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
          })
        }
      } catch (err) {
        console.error('Logout error:', err)
      } finally {
        commit('clearAuth')
      }
    },
    
    checkAuth({ commit }) {
      const token = localStorage.getItem('access_token')
      const storedUser = localStorage.getItem('user')
      
      if (token && storedUser) {
        try {
          const user = JSON.parse(storedUser)
          commit('setAccessToken', token)
          commit('setUser', user)
          return true
        } catch (e) {
          commit('clearAuth')
          return false
        }
      }
      return false
    }
  }
})

export default store
