const API_BASE = '/api';

const api = {
    token: localStorage.getItem('token'),
    
    setToken(token) {
        this.token = token;
        if (token) {
            localStorage.setItem('token', token);
        } else {
            localStorage.removeItem('token');
        }
    },
    
    async request(endpoint, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers
        });
        
        if (response.status === 401) {
            this.setToken(null);
            window.location.reload();
            return;
        }
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }
        
        return data;
    },
    
    get(endpoint) {
        return this.request(endpoint);
    },
    
    post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    
    delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE'
        });
    }
};

const AdminDashboard = {
    template: `
        <div>
            <h2 class="mb-4">Admin Dashboard</h2>
            
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card stat-card">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <p class="mb-1">Total Lots</p>
                                    <div class="stat-number">{{ stats.total_lots }}</div>
                                </div>
                                <i class="bi bi-geo-alt" style="font-size: 2rem; opacity: 0.5;"></i>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stat-card blue">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <p class="mb-1">Total Spots</p>
                                    <div class="stat-number">{{ stats.total_spots }}</div>
                                </div>
                                <i class="bi bi-car-front" style="font-size: 2rem; opacity: 0.5;"></i>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stat-card orange">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <p class="mb-1">Available</p>
                                    <div class="stat-number">{{ stats.available_spots }}</div>
                                </div>
                                <i class="bi bi-check-circle" style="font-size: 2rem; opacity: 0.5;"></i>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stat-card purple">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <p class="mb-1">Occupied</p>
                                    <div class="stat-number">{{ stats.occupied_spots }}</div>
                                </div>
                                <i class="bi bi-x-circle" style="font-size: 2rem; opacity: 0.5;"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="text-muted mb-2">Total Users</h6>
                            <h3>{{ stats.total_users }}</h3>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="text-muted mb-2">Today's Bookings</h6>
                            <h3>{{ stats.today_bookings }}</h3>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="text-muted mb-2">Total Revenue</h6>
                            <h3>Rs. {{ stats.total_revenue }}</h3>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="text-muted mb-2">Occupancy Rate</h6>
                            <h3>{{ stats.occupancy_rate }}%</h3>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header">Parking Lots Overview</div>
                        <div class="card-body">
                            <div class="chart-container">
                                <canvas ref="lotsChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">Occupancy Status</div>
                        <div class="card-body">
                            <div class="chart-container">
                                <canvas ref="occupancyChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    props: ['api'],
    data() {
        return {
            stats: {
                total_lots: 0,
                total_spots: 0,
                available_spots: 0,
                occupied_spots: 0,
                total_users: 0,
                today_bookings: 0,
                total_revenue: 0,
                occupancy_rate: 0
            },
            lotStats: []
        };
    },
    async mounted() {
        await this.loadData();
        this.renderCharts();
    },
    methods: {
        async loadData() {
            try {
                this.stats = await this.api.get('/admin/dashboard');
                const summary = await this.api.get('/admin/stats/summary');
                this.lotStats = summary.lot_stats || [];
            } catch (error) {
                this.$emit('show-toast', { type: 'danger', message: error.message });
            }
        },
        renderCharts() {
            if (this.lotStats.length > 0) {
                new Chart(this.$refs.lotsChart, {
                    type: 'bar',
                    data: {
                        labels: this.lotStats.map(l => l.name),
                        datasets: [
                            {
                                label: 'Available',
                                data: this.lotStats.map(l => l.available),
                                backgroundColor: '#4CAF50'
                            },
                            {
                                label: 'Occupied',
                                data: this.lotStats.map(l => l.occupied),
                                backgroundColor: '#F44336'
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false
                    }
                });
            }
            
            new Chart(this.$refs.occupancyChart, {
                type: 'doughnut',
                data: {
                    labels: ['Available', 'Occupied'],
                    datasets: [{
                        data: [this.stats.available_spots, this.stats.occupied_spots],
                        backgroundColor: ['#4CAF50', '#F44336']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    }
};

const ParkingLotsManager = {
    template: `
        <div>
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>Parking Lots Management</h2>
                <button class="btn btn-primary" @click="showAddModal = true">
                    <i class="bi bi-plus-circle me-2"></i>Add New Lot
                </button>
            </div>
            
            <div class="row">
                <div class="col-md-4 mb-4" v-for="lot in lots" :key="lot.id">
                    <div class="card h-100">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <strong>{{ lot.prime_location_name }}</strong>
                            <div class="dropdown">
                                <button class="btn btn-sm btn-outline-secondary" data-bs-toggle="dropdown">
                                    <i class="bi bi-three-dots-vertical"></i>
                                </button>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item" href="#" @click.prevent="editLot(lot)">Edit</a></li>
                                    <li><a class="dropdown-item" href="#" @click.prevent="viewSpots(lot)">View Spots</a></li>
                                    <li><hr class="dropdown-divider"></li>
                                    <li><a class="dropdown-item text-danger" href="#" @click.prevent="deleteLot(lot)">Delete</a></li>
                                </ul>
                            </div>
                        </div>
                        <div class="card-body">
                            <p class="text-muted mb-2"><i class="bi bi-geo-alt me-2"></i>{{ lot.address }}</p>
                            <p class="mb-2"><i class="bi bi-tag me-2"></i>Rs. {{ lot.price }}/hour</p>
                            <p class="mb-2"><i class="bi bi-pin-map me-2"></i>{{ lot.pin_code }}</p>
                            <div class="d-flex justify-content-between mt-3">
                                <span class="badge bg-success">{{ lot.available_spots }} Available</span>
                                <span class="badge bg-danger">{{ lot.occupied_spots }} Occupied</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Add/Edit Modal -->
            <div class="modal" :class="{show: showAddModal || editingLot}" :style="{display: (showAddModal || editingLot) ? 'block' : 'none'}" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">{{ editingLot ? 'Edit Parking Lot' : 'Add New Parking Lot' }}</h5>
                            <button type="button" class="btn-close" @click="closeModal"></button>
                        </div>
                        <div class="modal-body">
                            <form @submit.prevent="saveLot">
                                <div class="mb-3">
                                    <label class="form-label">Location Name</label>
                                    <input type="text" class="form-control" v-model="lotForm.prime_location_name" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Price (per hour)</label>
                                    <input type="number" class="form-control" v-model="lotForm.price" step="0.01" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Address</label>
                                    <textarea class="form-control" v-model="lotForm.address" required></textarea>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Pin Code</label>
                                    <input type="text" class="form-control" v-model="lotForm.pin_code" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Number of Spots</label>
                                    <input type="number" class="form-control" v-model="lotForm.number_of_spots" required>
                                </div>
                                <button type="submit" class="btn btn-primary w-100">{{ editingLot ? 'Update' : 'Add' }} Parking Lot</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-backdrop fade show" v-if="showAddModal || editingLot" @click="closeModal"></div>
            
            <!-- Spots Modal -->
            <div class="modal" :class="{show: viewingLot}" :style="{display: viewingLot ? 'block' : 'none'}" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Parking Spots - {{ viewingLot?.prime_location_name }}</h5>
                            <button type="button" class="btn-close" @click="viewingLot = null"></button>
                        </div>
                        <div class="modal-body">
                            <div class="d-flex flex-wrap gap-2">
                                <div v-for="spot in spots" :key="spot.id" 
                                     class="parking-spot" 
                                     :class="spot.status === 'A' ? 'available' : 'occupied'"
                                     :title="spot.status === 'O' ? 'Vehicle: ' + (spot.vehicle_number || 'Unknown') : 'Available'">
                                    {{ spot.id }}
                                </div>
                            </div>
                            <div class="mt-3 d-flex gap-3">
                                <span><span class="badge bg-success">Available</span> {{ spots.filter(s => s.status === 'A').length }}</span>
                                <span><span class="badge bg-danger">Occupied</span> {{ spots.filter(s => s.status === 'O').length }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-backdrop fade show" v-if="viewingLot" @click="viewingLot = null"></div>
        </div>
    `,
    props: ['api'],
    data() {
        return {
            lots: [],
            spots: [],
            showAddModal: false,
            editingLot: null,
            viewingLot: null,
            lotForm: {
                prime_location_name: '',
                price: '',
                address: '',
                pin_code: '',
                number_of_spots: 10
            }
        };
    },
    async mounted() {
        await this.loadLots();
    },
    methods: {
        async loadLots() {
            try {
                this.lots = await this.api.get('/admin/parking-lots');
            } catch (error) {
                this.$emit('show-toast', { type: 'danger', message: error.message });
            }
        },
        editLot(lot) {
            this.editingLot = lot;
            this.lotForm = { ...lot };
        },
        async viewSpots(lot) {
            try {
                const data = await this.api.get(`/admin/parking-lots/${lot.id}/spots`);
                this.spots = data.spots;
                this.viewingLot = lot;
            } catch (error) {
                this.$emit('show-toast', { type: 'danger', message: error.message });
            }
        },
        closeModal() {
            this.showAddModal = false;
            this.editingLot = null;
            this.lotForm = {
                prime_location_name: '',
                price: '',
                address: '',
                pin_code: '',
                number_of_spots: 10
            };
        },
        async saveLot() {
            try {
                if (this.editingLot) {
                    await this.api.put(`/admin/parking-lots/${this.editingLot.id}`, this.lotForm);
                    this.$emit('show-toast', { type: 'success', message: 'Parking lot updated successfully' });
                } else {
                    await this.api.post('/admin/parking-lots', this.lotForm);
                    this.$emit('show-toast', { type: 'success', message: 'Parking lot added successfully' });
                }
                this.closeModal();
                await this.loadLots();
            } catch (error) {
                this.$emit('show-toast', { type: 'danger', message: error.message });
            }
        },
        async deleteLot(lot) {
            if (!confirm('Are you sure you want to delete this parking lot?')) return;
            try {
                await this.api.delete(`/admin/parking-lots/${lot.id}`);
                this.$emit('show-toast', { type: 'success', message: 'Parking lot deleted successfully' });
                await this.loadLots();
            } catch (error) {
                this.$emit('show-toast', { type: 'danger', message: error.message });
            }
        }
    }
};

const UsersList = {
    template: `
        <div>
            <h2 class="mb-4">Registered Users</h2>
            <div class="card">
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Username</th>
                                    <th>Full Name</th>
                                    <th>Email</th>
                                    <th>Vehicle Number</th>
                                    <th>Phone</th>
                                    <th>Last Visit</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="user in users" :key="user.id">
                                    <td>{{ user.id }}</td>
                                    <td>{{ user.username }}</td>
                                    <td>{{ user.full_name || '-' }}</td>
                                    <td>{{ user.email || '-' }}</td>
                                    <td>{{ user.vehicle_number || '-' }}</td>
                                    <td>{{ user.phone || '-' }}</td>
                                    <td>{{ user.last_visit ? new Date(user.last_visit).toLocaleDateString() : 'Never' }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    `,
    props: ['api'],
    data() {
        return { users: [] };
    },
    async mounted() {
        try {
            this.users = await this.api.get('/admin/users');
        } catch (error) {
            this.$emit('show-toast', { type: 'danger', message: error.message });
        }
    }
};

const AdminSummary = {
    template: `
        <div>
            <h2 class="mb-4">Summary & Statistics</h2>
            <div class="row">
                <div class="col-md-8">
                    <div class="card mb-4">
                        <div class="card-header">Revenue by Parking Lot</div>
                        <div class="card-body">
                            <div class="chart-container">
                                <canvas ref="revenueChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card mb-4">
                        <div class="card-header">Bookings by Lot</div>
                        <div class="card-body">
                            <div class="chart-container">
                                <canvas ref="bookingsChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-header">Parking Lot Statistics</div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Location</th>
                                    <th>Total Bookings</th>
                                    <th>Revenue</th>
                                    <th>Available</th>
                                    <th>Occupied</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="stat in lotStats" :key="stat.name">
                                    <td>{{ stat.name }}</td>
                                    <td>{{ stat.total_bookings }}</td>
                                    <td>Rs. {{ stat.revenue }}</td>
                                    <td><span class="badge bg-success">{{ stat.available }}</span></td>
                                    <td><span class="badge bg-danger">{{ stat.occupied }}</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    `,
    props: ['api'],
    data() {
        return { lotStats: [] };
    },
    async mounted() {
        try {
            const summary = await this.api.get('/admin/stats/summary');
            this.lotStats = summary.lot_stats || [];
            this.$nextTick(() => this.renderCharts());
        } catch (error) {
            this.$emit('show-toast', { type: 'danger', message: error.message });
        }
    },
    methods: {
        renderCharts() {
            if (this.lotStats.length === 0) return;
            
            new Chart(this.$refs.revenueChart, {
                type: 'bar',
                data: {
                    labels: this.lotStats.map(l => l.name),
                    datasets: [{
                        label: 'Revenue (Rs.)',
                        data: this.lotStats.map(l => l.revenue),
                        backgroundColor: '#4CAF50'
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
            
            new Chart(this.$refs.bookingsChart, {
                type: 'pie',
                data: {
                    labels: this.lotStats.map(l => l.name),
                    datasets: [{
                        data: this.lotStats.map(l => l.total_bookings),
                        backgroundColor: ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336']
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        }
    }
};

const UserDashboard = {
    template: `
        <div>
            <h2 class="mb-4">Welcome, {{ user.full_name || user.username }}!</h2>
            
            <div class="row mb-4" v-if="activeBooking">
                <div class="col-12">
                    <div class="card border-primary">
                        <div class="card-header bg-primary text-white">
                            <i class="bi bi-car-front me-2"></i>Active Booking
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <p><strong>Location:</strong> {{ activeBooking.lot_name }}</p>
                                    <p><strong>Spot ID:</strong> {{ activeBooking.spot_id }}</p>
                                    <p><strong>Vehicle:</strong> {{ activeBooking.vehicle_number }}</p>
                                </div>
                                <div class="col-md-6">
                                    <p><strong>Parked Since:</strong> {{ formatDate(activeBooking.parking_timestamp) }}</p>
                                    <p><strong>Duration:</strong> {{ calculateDuration(activeBooking.parking_timestamp) }}</p>
                                    <p><strong>Est. Cost:</strong> Rs. {{ calculateCost(activeBooking) }}</p>
                                </div>
                            </div>
                            <button class="btn btn-danger mt-3" @click="releaseSpot">
                                <i class="bi bi-x-circle me-2"></i>Release Spot
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card stat-card">
                        <div class="card-body text-center">
                            <h3>{{ stats.total_bookings }}</h3>
                            <p class="mb-0">Total Bookings</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stat-card blue">
                        <div class="card-body text-center">
                            <h3>{{ stats.total_hours }}</h3>
                            <p class="mb-0">Total Hours</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stat-card orange">
                        <div class="card-body text-center">
                            <h3>Rs. {{ stats.total_spent }}</h3>
                            <p class="mb-0">Total Spent</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stat-card purple">
                        <div class="card-body text-center">
                            <h3>{{ stats.active_bookings }}</h3>
                            <p class="mb-0">Active Now</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">Recent Parking History</div>
                        <div class="card-body">
                            <div v-if="recentBookings.length === 0" class="text-muted">No parking history yet</div>
                            <div v-else class="list-group list-group-flush">
                                <div v-for="booking in recentBookings.slice(0, 5)" :key="booking.id" class="list-group-item">
                                    <div class="d-flex justify-content-between">
                                        <div>
                                            <strong>{{ booking.lot_name }}</strong>
                                            <br><small class="text-muted">{{ formatDate(booking.parking_timestamp) }}</small>
                                        </div>
                                        <div class="text-end">
                                            <span v-if="booking.is_active" class="badge bg-primary">Active</span>
                                            <span v-else>Rs. {{ booking.parking_cost || 0 }}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">Parking Lots Usage</div>
                        <div class="card-body">
                            <div class="chart-container" style="height: 200px;">
                                <canvas ref="usageChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    props: ['api', 'user'],
    data() {
        return {
            activeBooking: null,
            stats: { total_bookings: 0, total_hours: 0, total_spent: 0, active_bookings: 0, lot_usage: {} },
            recentBookings: []
        };
    },
    async mounted() {
        await this.loadData();
    },
    methods: {
        async loadData() {
            try {
                const [bookings, stats, history] = await Promise.all([
                    this.api.get('/user/bookings'),
                    this.api.get('/user/stats/summary'),
                    this.api.get('/user/bookings/history')
                ]);
                this.activeBooking = bookings.length > 0 ? bookings[0] : null;
                this.stats = stats;
                this.recentBookings = history;
                this.$nextTick(() => this.renderChart());
            } catch (error) {
                this.$emit('show-toast', { type: 'danger', message: error.message });
            }
        },
        formatDate(dateStr) {
            return new Date(dateStr).toLocaleString();
        },
        calculateDuration(startStr) {
            const start = new Date(startStr);
            const now = new Date();
            const hours = Math.floor((now - start) / 3600000);
            const mins = Math.floor(((now - start) % 3600000) / 60000);
            return `${hours}h ${mins}m`;
        },
        calculateCost(booking) {
            const start = new Date(booking.parking_timestamp);
            const now = new Date();
            const hours = (now - start) / 3600000;
            return (hours * 50).toFixed(2);
        },
        async releaseSpot() {
            if (!this.activeBooking) return;
            try {
                const result = await this.api.post(`/user/bookings/${this.activeBooking.id}/release`);
                this.$emit('show-toast', { type: 'success', message: `Spot released! Total cost: Rs. ${result.cost}` });
                await this.loadData();
            } catch (error) {
                this.$emit('show-toast', { type: 'danger', message: error.message });
            }
        },
        renderChart() {
            if (!this.$refs.usageChart || Object.keys(this.stats.lot_usage).length === 0) return;
            new Chart(this.$refs.usageChart, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(this.stats.lot_usage),
                    datasets: [{
                        data: Object.values(this.stats.lot_usage),
                        backgroundColor: ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336']
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        }
    }
};

const BookSpot = {
    template: `
        <div>
            <h2 class="mb-4">Book a Parking Spot</h2>
            
            <div class="alert alert-warning" v-if="hasActiveBooking">
                <i class="bi bi-exclamation-triangle me-2"></i>
                You already have an active booking. Please release it before booking a new spot.
            </div>
            
            <div class="row" v-if="!hasActiveBooking">
                <div class="col-md-8">
                    <div class="card mb-4">
                        <div class="card-header">
                            <i class="bi bi-search me-2"></i>Search Parking Lots
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <input type="text" class="form-control" v-model="searchQuery" placeholder="Search by location or address...">
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-4" v-for="lot in filteredLots" :key="lot.id">
                            <div class="card h-100" :class="{'border-primary': selectedLot?.id === lot.id}">
                                <div class="card-body">
                                    <h5 class="card-title">{{ lot.prime_location_name }}</h5>
                                    <p class="text-muted"><i class="bi bi-geo-alt me-2"></i>{{ lot.address }}</p>
                                    <p><i class="bi bi-tag me-2"></i>Rs. {{ lot.price }}/hour</p>
                                    <div class="d-flex justify-content-between align-items-center">
                                        <span class="badge bg-success">{{ lot.available_spots }} spots available</span>
                                        <button class="btn btn-primary btn-sm" 
                                                :disabled="lot.available_spots === 0"
                                                @click="selectLot(lot)">
                                            Select
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="card" v-if="selectedLot">
                        <div class="card-header bg-primary text-white">
                            <i class="bi bi-car-front me-2"></i>Book Spot
                        </div>
                        <div class="card-body">
                            <h5>{{ selectedLot.prime_location_name }}</h5>
                            <p class="text-muted">{{ selectedLot.address }}</p>
                            <hr>
                            <form @submit.prevent="bookSpot">
                                <div class="mb-3">
                                    <label class="form-label">Vehicle Number</label>
                                    <input type="text" class="form-control" v-model="vehicleNumber" 
                                           :placeholder="user.vehicle_number || 'e.g., MH01AB1234'">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Price</label>
                                    <input type="text" class="form-control" :value="'Rs. ' + selectedLot.price + '/hour'" disabled>
                                </div>
                                <button type="submit" class="btn btn-success w-100">
                                    <i class="bi bi-check-circle me-2"></i>Confirm Booking
                                </button>
                            </form>
                        </div>
                    </div>
                    <div class="card" v-else>
                        <div class="card-body text-center text-muted">
                            <i class="bi bi-arrow-left-circle" style="font-size: 3rem;"></i>
                            <p class="mt-3">Select a parking lot to book a spot</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    props: ['api', 'user'],
    data() {
        return {
            lots: [],
            searchQuery: '',
            selectedLot: null,
            vehicleNumber: '',
            hasActiveBooking: false
        };
    },
    computed: {
        filteredLots() {
            if (!this.searchQuery) return this.lots;
            const query = this.searchQuery.toLowerCase();
            return this.lots.filter(lot => 
                lot.prime_location_name.toLowerCase().includes(query) ||
                lot.address.toLowerCase().includes(query)
            );
        }
    },
    async mounted() {
        try {
            const [lots, bookings] = await Promise.all([
                this.api.get('/parking-lots'),
                this.api.get('/user/bookings')
            ]);
            this.lots = lots;
            this.hasActiveBooking = bookings.length > 0;
            this.vehicleNumber = this.user.vehicle_number || '';
        } catch (error) {
            this.$emit('show-toast', { type: 'danger', message: error.message });
        }
    },
    methods: {
        selectLot(lot) {
            this.selectedLot = lot;
        },
        async bookSpot() {
            try {
                const result = await this.api.post('/user/bookings', {
                    lot_id: this.selectedLot.id,
                    vehicle_number: this.vehicleNumber || this.user.vehicle_number
                });
                this.$emit('show-toast', { type: 'success', message: `Spot ${result.spot.id} booked successfully!` });
                this.hasActiveBooking = true;
                this.selectedLot = null;
            } catch (error) {
                this.$emit('show-toast', { type: 'danger', message: error.message });
            }
        }
    }
};

const BookingHistory = {
    template: `
        <div>
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>Parking History</h2>
                <button class="btn btn-outline-primary" @click="exportCSV" :disabled="exporting">
                    <i class="bi bi-download me-2"></i>{{ exporting ? 'Exporting...' : 'Export CSV' }}
                </button>
            </div>
            
            <div class="card">
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Location</th>
                                    <th>Spot ID</th>
                                    <th>Vehicle</th>
                                    <th>Check In</th>
                                    <th>Check Out</th>
                                    <th>Cost</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="booking in bookings" :key="booking.id">
                                    <td>{{ booking.id }}</td>
                                    <td>{{ booking.lot_name }}</td>
                                    <td>{{ booking.spot_id }}</td>
                                    <td>{{ booking.vehicle_number }}</td>
                                    <td>{{ formatDate(booking.parking_timestamp) }}</td>
                                    <td>{{ booking.leaving_timestamp ? formatDate(booking.leaving_timestamp) : '-' }}</td>
                                    <td>{{ booking.parking_cost ? 'Rs. ' + booking.parking_cost : '-' }}</td>
                                    <td>
                                        <span v-if="booking.is_active" class="badge bg-primary">Active</span>
                                        <span v-else class="badge bg-secondary">Completed</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    `,
    props: ['api'],
    data() {
        return {
            bookings: [],
            exporting: false
        };
    },
    async mounted() {
        try {
            this.bookings = await this.api.get('/user/bookings/history');
        } catch (error) {
            this.$emit('show-toast', { type: 'danger', message: error.message });
        }
    },
    methods: {
        formatDate(dateStr) {
            return new Date(dateStr).toLocaleString();
        },
        async exportCSV() {
            this.exporting = true;
            try {
                const result = await this.api.post('/user/export');
                this.$emit('show-toast', { type: 'success', message: 'Export started! You will be notified when ready.' });
                
                if (result.job.status === 'completed') {
                    window.open(`/api/user/export/${result.job.id}/download`, '_blank');
                }
            } catch (error) {
                this.$emit('show-toast', { type: 'danger', message: error.message });
            } finally {
                this.exporting = false;
            }
        }
    }
};

const UserSummary = {
    template: `
        <div>
            <h2 class="mb-4">My Parking Summary</h2>
            
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card stat-card">
                        <div class="card-body text-center">
                            <h3>{{ stats.total_bookings }}</h3>
                            <p class="mb-0">Total Bookings</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stat-card blue">
                        <div class="card-body text-center">
                            <h3>{{ stats.completed_bookings }}</h3>
                            <p class="mb-0">Completed</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stat-card orange">
                        <div class="card-body text-center">
                            <h3>{{ stats.total_hours }}</h3>
                            <p class="mb-0">Total Hours</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stat-card purple">
                        <div class="card-body text-center">
                            <h3>Rs. {{ stats.total_spent }}</h3>
                            <p class="mb-0">Total Spent</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">Parking Lot Usage</div>
                        <div class="card-body">
                            <div class="chart-container">
                                <canvas ref="usageChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">Frequently Used Locations</div>
                        <div class="card-body">
                            <div class="list-group list-group-flush">
                                <div v-for="(count, name) in stats.lot_usage" :key="name" 
                                     class="list-group-item d-flex justify-content-between">
                                    <span>{{ name }}</span>
                                    <span class="badge bg-primary">{{ count }} visits</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    props: ['api'],
    data() {
        return {
            stats: { total_bookings: 0, completed_bookings: 0, total_hours: 0, total_spent: 0, lot_usage: {} }
        };
    },
    async mounted() {
        try {
            this.stats = await this.api.get('/user/stats/summary');
            this.$nextTick(() => this.renderChart());
        } catch (error) {
            this.$emit('show-toast', { type: 'danger', message: error.message });
        }
    },
    methods: {
        renderChart() {
            if (!this.$refs.usageChart || Object.keys(this.stats.lot_usage).length === 0) return;
            new Chart(this.$refs.usageChart, {
                type: 'bar',
                data: {
                    labels: Object.keys(this.stats.lot_usage),
                    datasets: [{
                        label: 'Visits',
                        data: Object.values(this.stats.lot_usage),
                        backgroundColor: '#4CAF50'
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        }
    }
};

const UserProfile = {
    template: `
        <div>
            <h2 class="mb-4">Edit Profile</h2>
            <div class="row">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-body">
                            <form @submit.prevent="saveProfile">
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Username</label>
                                        <input type="text" class="form-control" :value="user.username" disabled>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Full Name</label>
                                        <input type="text" class="form-control" v-model="form.full_name">
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Email</label>
                                        <input type="email" class="form-control" v-model="form.email">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Phone</label>
                                        <input type="tel" class="form-control" v-model="form.phone">
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Vehicle Number</label>
                                    <input type="text" class="form-control" v-model="form.vehicle_number">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Address</label>
                                    <textarea class="form-control" v-model="form.address" rows="2"></textarea>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Pin Code</label>
                                    <input type="text" class="form-control" v-model="form.pin_code">
                                </div>
                                <button type="submit" class="btn btn-primary">
                                    <i class="bi bi-save me-2"></i>Save Changes
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    props: ['api', 'user'],
    data() {
        return {
            form: {
                full_name: '',
                email: '',
                phone: '',
                vehicle_number: '',
                address: '',
                pin_code: ''
            }
        };
    },
    mounted() {
        this.form = {
            full_name: this.user.full_name || '',
            email: this.user.email || '',
            phone: this.user.phone || '',
            vehicle_number: this.user.vehicle_number || '',
            address: this.user.address || '',
            pin_code: this.user.pin_code || ''
        };
    },
    methods: {
        async saveProfile() {
            try {
                const updated = await this.api.put('/user/profile', this.form);
                this.$emit('update-user', updated);
                this.$emit('show-toast', { type: 'success', message: 'Profile updated successfully' });
            } catch (error) {
                this.$emit('show-toast', { type: 'danger', message: error.message });
            }
        }
    }
};

const { createApp } = Vue;

const app = createApp({
    data() {
        return {
            isAuthenticated: false,
            isLogin: true,
            user: null,
            currentView: 'dashboard',
            loading: false,
            toasts: [],
            loginForm: {
                username: '',
                password: '',
                role: 'user',
                email: '',
                full_name: '',
                vehicle_number: '',
                phone: '',
                address: '',
                pin_code: ''
            },
            api: api
        };
    },
    async mounted() {
        if (api.token) {
            await this.loadUser();
        }
    },
    methods: {
        async loadUser() {
            this.loading = true;
            try {
                const user = await api.get('/user/profile');
                this.user = user;
                this.isAuthenticated = true;
            } catch (error) {
                try {
                    const dashboard = await api.get('/admin/dashboard');
                    this.user = { role: 'admin', username: 'admin' };
                    this.isAuthenticated = true;
                } catch (e) {
                    api.setToken(null);
                }
            } finally {
                this.loading = false;
            }
        },
        async login() {
            this.loading = true;
            try {
                const result = await api.post('/auth/login', this.loginForm);
                api.setToken(result.access_token);
                this.user = result.user;
                this.isAuthenticated = true;
                this.showToast({ type: 'success', message: 'Login successful!' });
            } catch (error) {
                this.showToast({ type: 'danger', message: error.message });
            } finally {
                this.loading = false;
            }
        },
        async register() {
            this.loading = true;
            try {
                const result = await api.post('/auth/register', this.loginForm);
                api.setToken(result.access_token);
                this.user = result.user;
                this.isAuthenticated = true;
                this.showToast({ type: 'success', message: 'Registration successful!' });
            } catch (error) {
                this.showToast({ type: 'danger', message: error.message });
            } finally {
                this.loading = false;
            }
        },
        logout() {
            api.setToken(null);
            this.isAuthenticated = false;
            this.user = null;
            this.currentView = 'dashboard';
        },
        showToast(toast) {
            const id = Date.now();
            this.toasts.push({ ...toast, id });
            setTimeout(() => this.removeToast(id), 5000);
        },
        removeToast(id) {
            this.toasts = this.toasts.filter(t => t.id !== id);
        },
        updateUser(user) {
            this.user = user;
        }
    }
});

app.component('admin-dashboard', AdminDashboard);
app.component('parking-lots-manager', ParkingLotsManager);
app.component('users-list', UsersList);
app.component('admin-summary', AdminSummary);
app.component('user-dashboard', UserDashboard);
app.component('book-spot', BookSpot);
app.component('booking-history', BookingHistory);
app.component('user-summary', UserSummary);
app.component('user-profile', UserProfile);

app.mount('#app');
