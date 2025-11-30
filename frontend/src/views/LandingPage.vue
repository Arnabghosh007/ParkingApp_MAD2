<template>
  <div class="landing-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container-fluid py-5">
        <div class="row align-items-center min-vh-100">
          <div class="col-lg-6">
            <div class="hero-content">
              <h1 class="hero-title mb-3">
                <i class="bi bi-car-front-fill text-primary"></i>
                Smart Parking Solutions
              </h1>
              <p class="hero-subtitle mb-4">
                Find, book, and manage parking spaces effortlessly with our intelligent parking application
              </p>
              <p class="hero-description mb-5">
                Experience the future of parking management. Real-time availability, instant bookings, and seamless payment solutions all in one platform.
              </p>
              <div class="cta-buttons">
                <router-link to="/register" class="btn btn-primary btn-lg me-3">
                  <i class="bi bi-play-circle me-2"></i>Get Started
                </router-link>
                <router-link to="/login" class="btn btn-outline-primary btn-lg">
                  <i class="bi bi-box-arrow-in-right me-2"></i>Sign In
                </router-link>
              </div>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="hero-visual">
              <div class="floating-card card-1">
                <i class="bi bi-p-square-fill"></i>
                <span>150+ Lots</span>
              </div>
              <div class="floating-card card-2">
                <i class="bi bi-check-circle-fill"></i>
                <span>Instant Booking</span>
              </div>
              <div class="floating-card card-3">
                <i class="bi bi-shield-check"></i>
                <span>Secure & Safe</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section py-5">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="section-title">Why Choose Us?</h2>
          <p class="section-subtitle">Everything you need for hassle-free parking</p>
        </div>
        
        <div class="row g-4">
          <div class="col-md-6 col-lg-4">
            <div class="feature-card">
              <div class="feature-icon bg-primary">
                <i class="bi bi-lightning-fill"></i>
              </div>
              <h5 class="feature-title">Lightning Fast</h5>
              <p class="feature-text">Book parking in seconds with our intuitive interface</p>
            </div>
          </div>
          
          <div class="col-md-6 col-lg-4">
            <div class="feature-card">
              <div class="feature-icon bg-success">
                <i class="bi bi-geo-alt-fill"></i>
              </div>
              <h5 class="feature-title">Real-time Availability</h5>
              <p class="feature-text">See available spots instantly across all parking lots</p>
            </div>
          </div>
          
          <div class="col-md-6 col-lg-4">
            <div class="feature-card">
              <div class="feature-icon bg-info">
                <i class="bi bi-graph-up"></i>
              </div>
              <h5 class="feature-title">Track History</h5>
              <p class="feature-text">Monitor your parking usage and spending patterns</p>
            </div>
          </div>
          
          <div class="col-md-6 col-lg-4">
            <div class="feature-card">
              <div class="feature-icon bg-warning">
                <i class="bi bi-bell-fill"></i>
              </div>
              <h5 class="feature-title">Smart Notifications</h5>
              <p class="feature-text">Get reminders and alerts for your bookings</p>
            </div>
          </div>
          
          <div class="col-md-6 col-lg-4">
            <div class="feature-card">
              <div class="feature-icon bg-danger">
                <i class="bi bi-shield-lock"></i>
              </div>
              <h5 class="feature-title">Secure Payments</h5>
              <p class="feature-text">Safe and encrypted payment processing</p>
            </div>
          </div>
          
          <div class="col-md-6 col-lg-4">
            <div class="feature-card">
              <div class="feature-icon bg-secondary">
                <i class="bi bi-bar-chart-fill"></i>
              </div>
              <h5 class="feature-title">Detailed Analytics</h5>
              <p class="feature-text">Get insights into parking trends and costs</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section py-5 bg-light">
      <div class="container">
        <div class="row text-center">
          <div class="col-md-3 col-6 mb-4">
            <div class="stat-item">
              <h3 class="stat-number">150+</h3>
              <p class="stat-label">Parking Lots</p>
            </div>
          </div>
          <div class="col-md-3 col-6 mb-4">
            <div class="stat-item">
              <h3 class="stat-number">5000+</h3>
              <p class="stat-label">Total Spots</p>
            </div>
          </div>
          <div class="col-md-3 col-6 mb-4">
            <div class="stat-item">
              <h3 class="stat-number">10K+</h3>
              <p class="stat-label">Active Users</p>
            </div>
          </div>
          <div class="col-md-3 col-6 mb-4">
            <div class="stat-item">
              <h3 class="stat-number">99.9%</h3>
              <p class="stat-label">Uptime</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section py-5">
      <div class="container text-center">
        <h2 class="section-title mb-3">Ready to Park Smarter?</h2>
        <p class="section-subtitle mb-4">Join thousands of users who trust us for their parking needs</p>
        <router-link to="/register" class="btn btn-primary btn-lg">
          <i class="bi bi-arrow-right me-2"></i>Start Free Today
        </router-link>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer bg-dark text-light py-4 mt-5">
      <div class="container text-center">
        <p class="mb-0">&copy; 2025 Vehicle Parking App. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'LandingPage'
}
</script>

<style scoped>
.landing-page {
  overflow-x: hidden;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  right: -50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 1.5rem;
}

.hero-subtitle {
  font-size: 1.5rem;
  font-weight: 300;
  opacity: 0.95;
}

.hero-description {
  font-size: 1.1rem;
  opacity: 0.9;
  line-height: 1.6;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.hero-visual {
  position: relative;
  height: 400px;
}

.floating-card {
  position: absolute;
  background: white;
  color: #667eea;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  animation: float 3s ease-in-out infinite;
}

.floating-card i {
  font-size: 2rem;
}

.card-1 {
  top: 20px;
  left: 20px;
  animation-delay: 0s;
}

.card-2 {
  top: 150px;
  right: 50px;
  animation-delay: 0.3s;
}

.card-3 {
  bottom: 20px;
  left: 100px;
  animation-delay: 0.6s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* Features Section */
.features-section {
  background: #f8f9fa;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a1a1a;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #6c757d;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  text-align: center;
  height: 100%;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: white;
  margin: 0 auto 1rem;
}

.feature-title {
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.feature-text {
  color: #6c757d;
  font-size: 0.95rem;
}

/* Stats Section */
.stat-item {
  padding: 2rem;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1rem;
  color: #6c757d;
  margin: 0;
}

/* CTA Section */
.cta-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

/* Footer */
.footer {
  background-color: #1a1a1a !important;
  border-top: 1px solid #333;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .hero-visual {
    height: 250px;
    margin-top: 2rem;
  }
  
  .floating-card {
    font-size: 0.9rem;
    padding: 1rem;
  }
  
  .cta-buttons {
    flex-direction: column;
  }
  
  .btn-lg {
    width: 100%;
  }
}

/* Hero Section Enhancements */
.hero-section {
  background: linear-gradient(135deg, #f5f7fc 0%, #f0f3ff 100%);
  position: relative;
  overflow: hidden;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1.5rem;
  letter-spacing: -1px;
}

.hero-subtitle {
  font-size: 1.4rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 1rem;
  line-height: 1.8;
}

.hero-description {
  font-size: 1.1rem;
  color: #4b5563;
  line-height: 1.8;
  max-width: 600px;
}

.cta-buttons {
  display: flex;
  gap: 1.5rem;
  margin-top: 2rem;
}

/* Feature Card Enhancements */
.feature-card {
  padding: 2.5rem 2rem;
  border-radius: 16px;
  background: white;
  border: 1px solid rgba(102, 126, 234, 0.1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  text-align: center;
  height: 100%;
}

.feature-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 15px 50px rgba(102, 126, 234, 0.2);
  border-color: rgba(102, 126, 234, 0.2);
}

.feature-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.2rem;
  color: white;
  margin: 0 auto 1.5rem;
  transition: all 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.15) rotate(10deg);
}

.feature-title {
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.8rem;
  font-size: 1.2rem;
  letter-spacing: -0.5px;
}

.feature-text {
  color: #6c757d;
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Floating Cards */
.floating-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  animation: float 6s ease-in-out infinite;
}

.floating-card i {
  font-size: 1.8rem;
  color: #667eea;
}

/* Stats */
.stat-item {
  padding: 2.5rem;
  text-align: center;
}

.stat-number {
  font-size: 3rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1rem;
  color: #6c757d;
  margin: 0;
  font-weight: 600;
}
</style>
