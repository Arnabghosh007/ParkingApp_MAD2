# Vehicle Parking App V2

## Overview
A multi-user vehicle parking management application built with Flask API backend and Vue.js 3 SPA frontend with Vite. The app manages different parking lots, parking spots, and parked vehicles for 4-wheeler parking.

## Project Architecture

### Backend (Flask API)
- **Location**: `/backend/`
- **Main App**: `backend/app.py`
- **Models**: `backend/models.py`
- **Configuration**: `backend/config.py`
- **Celery Tasks**: `backend/celery_app.py`
- **Runs on**: Port 5000

### Frontend (Vue.js 3 with Vite)
- **Location**: `/frontend/src/`
- **Build Tool**: Vite 5
- **Entry Point**: `frontend/src/main.js`
- **Components**: Vue single-file components (.vue)
- **Built Output**: `frontend/dist/` (served from `frontend/public/`)
- **Router**: Vue Router 4 with role-based redirects

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
redis-server --daemonize yes 2>/dev/null; python backend/run.py &  sleep 2 && cd frontend && npm run dev
```

### Frontend Development
```bash
cd frontend && npm run dev    # Run Vite dev server on port 5000
```

### Frontend Production Build
```bash
cd frontend && npm run build  # Build to dist/, outputs to public/
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

## Frontend Structure
- **Components**: `src/components/` (auth, admin, user, shared)
- **Views**: `src/views/` (LoginView, RegisterView, AdminDashboard, UserDashboard)
- **Router**: `src/router/index.js` (route definitions with guards)
- **Services**: `src/services/api.js` (API client with axios)
- **Composables**: `src/composables/useAuth.js` (auth state management)
- **Build Config**: `vite.config.js` (Vue + Vite configuration)

## Frameworks Used
- **Backend**: Flask, Flask-JWT-Extended, Flask-Caching, Flask-CORS, Flask-SQLAlchemy
- **Frontend**: Vue.js 3, Vue Router 4, Axios, Vite 5, Bootstrap 5
- **Database**: SQLite
- **Caching & Jobs**: Redis, Celery
- **Charts**: Chart.js
- **Icons**: Bootstrap Icons

## Recent Changes (November 2025)
- ✅ Converted from Jinja2 templates to Vue.js 3 SPA with Vite build tool
- ✅ Set up proper Vue component file structure with Vue Router
- ✅ Implemented JWT authentication with role-based access control
- ✅ Added Redis caching for API performance
- ✅ Added Celery background jobs (daily reminders, monthly reports)
- ✅ Added logout endpoint with token revocation via Redis blocklist
- ✅ Built Vue app with Vite and configured Flask to serve production build
- ✅ Fixed Chart.js rendering: Revenue, Bookings, Availability, Usage charts now fully functional
- ✅ Added comprehensive Parking Spots page - view all parking spots by lot with occupancy status
- ✅ Integrated Parking Spots link in navigation for admins and users

## Charts & Parking Spots
- **Admin Charts**: Revenue, Total Bookings, Available Spots, Occupied Spots - displays per parking lot
- **User Charts**: Total Bookings, Active/Completed bookings, Total spent, Lot usage breakdown
- **Parking Spots Page**: Shows all lots with real-time availability, occupancy percentage, expandable spot details
- Charts automatically update when parking lots are created or bookings are made
