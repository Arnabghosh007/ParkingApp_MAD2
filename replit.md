# Vehicle Parking App V2

## Overview
A multi-user vehicle parking management application built with Flask API backend and Vue.js frontend. The app manages different parking lots, parking spots, and parked vehicles for 4-wheeler parking.

## Project Architecture

### Backend (Flask API)
- **Location**: `/backend/`
- **Main App**: `backend/app.py`
- **Models**: `backend/models.py`
- **Configuration**: `backend/config.py`
- **Celery Tasks**: `backend/celery_app.py`

### Frontend (Vue.js with Bootstrap)
- **Location**: `/frontend/public/`
- **Entry Point**: `frontend/public/index.html`
- **Vue App**: `frontend/public/app.js`

### Database
- **SQLite**: `backend/parking.db` (auto-created)

## Key Features

### Core Functionalities
1. **Authentication**
   - JWT-based token authentication
   - Admin login (username: admin, password: admin123)
   - User registration/login
   - Role-based access control

2. **Admin Dashboard**
   - Create/Edit/Delete parking lots (spots auto-created)
   - View parking spot status
   - View registered users
   - Summary charts (occupancy, revenue)

3. **User Dashboard**
   - Book parking spot (auto-allocation)
   - Release parking spot
   - View parking history
   - Summary charts

4. **Background Jobs (Celery)**
   - Daily reminders (18:00)
   - Monthly activity reports (1st of month)
   - CSV export (user-triggered)

5. **Caching (Redis)**
   - Parking lots caching
   - API performance optimization

## API Endpoints

### Authentication
- POST `/api/auth/login` - Login
- POST `/api/auth/register` - Register
- POST `/api/auth/logout` - Logout (revokes token)
- POST `/api/auth/refresh` - Refresh token

### Admin
- GET `/api/admin/dashboard` - Dashboard stats
- GET `/api/admin/users` - List all users
- GET/POST `/api/admin/parking-lots` - CRUD parking lots
- PUT/DELETE `/api/admin/parking-lots/<id>` - Update/Delete lot
- GET `/api/admin/parking-lots/<id>/spots` - View lot spots
- GET `/api/admin/stats/summary` - Summary stats

### User
- GET/PUT `/api/user/profile` - User profile
- GET `/api/user/bookings` - Active bookings
- POST `/api/user/bookings` - Book a spot
- POST `/api/user/bookings/<id>/release` - Release spot
- GET `/api/user/bookings/history` - Booking history
- GET `/api/user/stats/summary` - User stats
- POST `/api/user/export` - Trigger CSV export

## Running the Application

### Start Command
```bash
redis-server --daemonize yes; python run.py
```

### Celery Worker (for background jobs)
```bash
cd backend && celery -A celery_app worker --loglevel=info
```

### Celery Beat (for scheduled tasks)
```bash
cd backend && celery -A celery_app beat --loglevel=info
```

## Default Admin Credentials
- Username: `admin`
- Password: `admin123`

## Frameworks Used
- Flask (API)
- Vue.js 3 (CDN)
- Bootstrap 5
- SQLite
- Redis (Caching)
- Celery (Background Jobs)
- Chart.js (Charts)
- Flask-JWT-Extended (Authentication)
- Flask-Caching (Redis Cache)
- Flask-CORS
- Flask-SQLAlchemy

## Recent Changes
- Initial V2 implementation (November 2025)
- Converted from Jinja2 templates to Vue.js SPA
- Added JWT authentication
- Added Redis caching
- Added Celery background jobs
- Added Chart.js visualizations
