# Vehicle Parking App V2 - Setup & Run Guide (VS Code)

## 📋 Prerequisites

Make sure you have the following installed on your system:

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **Redis Server** - [Download](https://redis.io/download) or use Redis in WSL/Docker
- **Git** (optional) - [Download](https://git-scm.com/)

### Verify Installation

```bash
python --version
node --version
redis-cli --version
```

---

## 🚀 Quick Start (5 Minutes)

### 1. Clone/Open Project in VS Code

```bash
cd /path/to/parking-app
code .
```

### 2. Start Redis Server

**On Windows (if using WSL):**
```bash
wsl redis-server
```

**On macOS/Linux:**
```bash
redis-server
```

**Or using Docker:**
```bash
docker run -d -p 6379:6379 redis:latest
```

### 3. Install Python Dependencies

Open VS Code terminal and run:

```bash
# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 5. Start Backend (Terminal 1)

```bash
cd backend
python app.py
```

**Expected Output:**
```
* Running on http://127.0.0.1:5001
* Debug mode: on
```

### 6. Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

**Expected Output:**
```
VITE v5.4.21 ready in 500 ms
➜  Local:   http://localhost:5000/
```

### 7. Access the Application

Open your browser and go to:
```
http://localhost:5000
```

---

## 📝 Detailed Setup Instructions

### Step 1: Install Backend Dependencies

1. Open VS Code Terminal (Ctrl + `)
2. Navigate to project root
3. Create Python virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

4. Install requirements:

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- Flask (web framework)
- Flask-SQLAlchemy (database ORM)
- Flask-JWT-Extended (authentication)
- Celery (background jobs)
- Redis (caching & job queue)
- ReportLab (PDF generation)
- Chart.js (frontend charts)

### Step 2: Install Frontend Dependencies

```bash
cd frontend
npm install
```

This installs:
- Vue 3
- Vite (build tool)
- Bootstrap 5
- Chart.js
- Vue Router
- Vuex

### Step 3: Configure Environment Variables (Optional)

Create `.env` file in project root if you want to customize:

```env
# Backend
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///parking.db
REDIS_URL=redis://localhost:6379/0

# Email (Gmail SMTP)
GMAIL_EMAIL=your-email@gmail.com
GMAIL_PASSWORD=your-app-password

# JWT
JWT_SECRET_KEY=your-secret-key-here
```

---

## 🔧 Running the Application

### Option A: Manual (Separate Terminals)

**Terminal 1 - Redis:**
```bash
redis-server
```

**Terminal 2 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 4 - Celery Worker (for background jobs):**
```bash
cd backend
celery -A celery_app worker --loglevel=info
```

**Terminal 5 - Celery Beat (for scheduled tasks):**
```bash
cd backend
celery -A celery_app beat --loglevel=info
```

### Option B: Automated (Single Command)

Run the combined startup script:

```bash
# From project root
redis-server --daemonize yes && cd backend && python app.py & sleep 2 && cd ../frontend && npm run dev
```

---

## 🌐 Access Points

| Component | URL | Purpose |
|-----------|-----|---------|
| Frontend (SPA) | http://localhost:5000 | Main application UI |
| Backend API | http://localhost:5001 | API endpoints |
| Health Check | http://localhost:5001/api/health | Verify backend is running |

---

## 👤 Default Login Credentials

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Role:** Admin (full access)

### Create User Account
- Click "Register" on login page
- Fill in username, password, vehicle number
- Login as user (limited access)

---

## 📊 Database

The database is **automatically created** on first run. No manual setup needed!

### Database Location
```
backend/instance/parking.db  (SQLite)
```

### Database Features
- Automatically initialized with admin user
- 7 tables for users, parking lots, bookings, etc.
- No manual migration needed

---

## 🛠️ Useful Commands

### Backend Commands

```bash
# Start backend only
cd backend
python app.py

# Start with debug mode
FLASK_DEBUG=1 python app.py

# Run Celery worker
celery -A celery_app worker --loglevel=info

# Run Celery beat scheduler
celery -A celery_app beat --loglevel=info

# Check Redis connection
redis-cli ping
```

### Frontend Commands

```bash
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Redis Commands

```bash
# Start Redis server
redis-server

# Connect to Redis CLI
redis-cli

# Check Redis status
redis-cli ping
# Output: PONG (means it's running)

# View all keys
redis-cli KEYS '*'

# Flush all data
redis-cli FLUSHALL
```

---

## 🧪 Testing the Application

### 1. Test Admin Login

```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123","role":"admin"}'
```

### 2. Test User Registration

```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123","vehicle_number":"MH01AB1234"}'
```

### 3. Test Parking Lots Endpoint

```bash
curl http://localhost:5001/api/parking-lots
```

---

## ⚠️ Troubleshooting

### "Port 5000/5001 Already in Use"
```bash
# Find process using port
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### "Redis Connection Failed"
```bash
# Check if Redis is running
redis-cli ping

# If not running, start it
redis-server
```

### "Module Not Found" (Python)
```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Then install requirements again
pip install -r requirements.txt
```

### "npm: command not found"
- Install Node.js from https://nodejs.org/
- Restart VS Code after installation

### Frontend shows "Cannot find module"
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Database errors
```bash
# Delete old database and restart
rm -f backend/instance/parking.db
python app.py  # Will recreate database
```

---

## 🐛 Debug Mode

### Enable Flask Debug Mode

Set environment variable before running:

```bash
# macOS/Linux
export FLASK_DEBUG=1
python app.py

# Windows
set FLASK_DEBUG=1
python app.py
```

### View Network Requests

Open browser Developer Tools (F12) and check:
- **Network tab** - API calls to backend
- **Console tab** - JavaScript errors
- **Application tab** - LocalStorage (tokens)

---

## 🎯 Project Structure

```
parking-app/
├── backend/
│   ├── app.py              # Main Flask app
│   ├── models.py           # Database models
│   ├── config.py           # Configuration
│   ├── celery_app.py       # Background jobs
│   ├── instance/           # Database folder
│   └── requirements.txt    # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/          # Page views
│   │   ├── services/       # API client
│   │   ├── store/          # State management
│   │   └── main.js         # Entry point
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
│
└── SETUP_AND_RUN.md        # This file
```

---

## 📚 API Documentation

### Authentication
- `POST /api/auth/login` - Login user
- `POST /api/auth/register` - Register new user
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/refresh` - Refresh token

### Admin APIs
- `GET /api/admin/dashboard` - Dashboard stats
- `GET /api/admin/parking-lots` - View all lots
- `POST /api/admin/parking-lots` - Create lot
- `GET /api/admin/users` - View all users
- `GET /api/admin/parking-lots/:id/spots` - View lot spots

### User APIs
- `GET /api/user/profile` - Get user profile
- `GET /api/user/bookings` - Get active bookings
- `POST /api/user/bookings` - Book a spot
- `POST /api/user/bookings/:id/release` - Release spot
- `GET /api/user/bookings/history` - Booking history

---

## 🚀 Next Steps

1. **Run the application** (follow Quick Start above)
2. **Login as admin** - Username: `admin`, Password: `admin123`
3. **Create a parking lot** - Admin dashboard → Parking Lots
4. **Register as user** - Click Register
5. **Book a spot** - User dashboard → Book Spot
6. **View booking summary** - Release spot to see completion page

---

## 📞 Support

If you encounter issues:

1. Check that all services are running (Redis, Backend, Frontend)
2. Verify ports are not in use (5000, 5001, 6379)
3. Check terminal output for error messages
4. View browser console (F12) for frontend errors
5. Restart all services if something goes wrong

---

**Application is ready to run! 🎉**

For more details, see `replit.md` in the project root.
