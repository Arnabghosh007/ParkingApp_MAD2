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

## 🚀 Quick Start (5 Minutes) - 3 Terminals Only!

### 1. Clone/Open Project in VS Code

```bash
cd /path/to/parking-app
code .
```

### 2. Install Python Dependencies

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

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 4. Start Services (3 Terminals)

**Terminal 1 - Redis:**
```bash
redis-server
```

**Terminal 2 - Backend API:**
```bash
cd backend
python app.py
```

**Terminal 3 - Frontend UI:**
```bash
cd frontend
npm run dev
```

### 5. Access the Application

Open your browser and go to:
```
http://localhost:5000
```

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

---

## ⚡ That's It! No Celery Worker Needed!

✅ Export works **instantly** (no background job needed)  
✅ App runs with just **3 terminals**  
✅ CSV downloads automatically when clicked  

**Celery is optional** - only needed for scheduled email reminders & monthly reports.

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

### Standard Setup (3 Terminals - Recommended)

**Terminal 1 - Redis (Cache & Session Storage):**
```bash
redis-server
```

**Terminal 2 - Backend API:**
```bash
cd backend
python app.py
```

**Terminal 3 - Frontend UI:**
```bash
cd frontend
npm run dev
```

That's all you need! The app will be available at http://localhost:5000

### Optional: Add Scheduled Email Jobs

If you want **daily reminders** and **monthly reports** via email:

**Terminal 4 - Celery Worker:**
```bash
cd backend
celery -A celery_app worker --loglevel=info
```

**Terminal 5 - Celery Beat (Scheduler):**
```bash
cd backend
celery -A celery_app beat --loglevel=info
```

Without Celery, the app works perfectly - you just won't get scheduled emails.

---

## 🔄 Celery - Background Jobs & Scheduling (Optional)

Celery handles **scheduled jobs** (recurring tasks). It's **optional** and only needed for email notifications.

⚠️ **Note:** CSV export now works **instantly without Celery**!

### Why Celery? (Optional Features Only)

- **Daily Reminders** - Automatically send emails at 6 PM to inactive users
- **Monthly Reports** - Generate PDF reports on the 1st of each month
- **Email Notifications** - Send automated emails without blocking the app

### Running Celery (Optional)

If you want scheduled emails, run TWO Celery components (in addition to Redis, Backend, and Frontend):

#### Terminal 4 - Celery Worker (Processes Jobs)

```bash
cd backend
celery -A celery_app worker --loglevel=info
```

**Expected Output:**
```
 -------------- celery@hostname v5.x.x
---- **** -----
--- * ***  * -- Linux-5.x.x-x-generic-x86_64 (...)
-- * - **** ---
- ** ---------- [config]
- ** ---------- .broker: redis://localhost:6379/0
- ** ---------- .concurrency: 4
- ** ---------- [queues]
-  *** ------- .celery: exchange:celery(direct) key:celery

[Tasks]
. celery_app.send_daily_reminders
. celery_app.send_monthly_reports
. celery_app.generate_csv_task

[2025-11-30 18:45:00,123: INFO/MainProcess] Ready to accept tasks!
```

#### Terminal 5 - Celery Beat (Scheduler - Triggers Scheduled Tasks)

```bash
cd backend
celery -A celery_app beat --loglevel=info
```

**Expected Output:**
```
celery beat v5.x.x is starting.
LocalTime -> 2025-11-30 18:45:00
Configuration:
    -> broker -> redis://localhost:6379/0
    -> app -> celery_app:0x...
    -> schedule -> celery.beat:PersistentScheduler
    -> app.conf.result_backend -> redis://localhost:6379/0
    -> app.conf.task_always_eager -> False

Celery Beat Scheduler
---------------------
SchedulingError: No module named 'celery_beat' -> using default
ScheduleEntry: Name: 'daily-reminder'
  Schedule: <crontab: 18 0 * * *> (at 18:00:00 every day)
  
ScheduleEntry: Name: 'monthly-report'
  Schedule: <crontab: 8 0 1 * *> (at 08:00:00 on day 1 of every month)

Scheduler started.
```

### Celery Jobs Available

#### 1. Daily Reminders (6 PM Every Day)

**Schedule:** 18:00 UTC daily

**What it does:**
- Sends email to inactive users (not visited in 24 hours)
- Notifies about new parking lots
- Encourages them to book a spot

**Code:** `backend/celery_app.py` - `send_daily_reminders()`

#### 2. Monthly Reports (1st of Month at 8 AM)

**Schedule:** 1st of each month at 08:00 UTC

**What it does:**
- Generates PDF report for each user
- Includes: total bookings, hours parked, money spent, most used lot
- Sends via email with PDF attachment

**Code:** `backend/celery_app.py` - `send_monthly_reports()`

### Complete Startup

**Minimum (3 Terminals - Everything Works):**

```bash
# Terminal 1: Redis (Cache & Session Storage)
redis-server

# Terminal 2: Backend API
cd backend
python app.py

# Terminal 3: Frontend UI
cd frontend
npm run dev
```

**With Scheduled Emails (5 Terminals):**

Add these if you want daily reminders & monthly reports:

```bash
# Terminal 4: Celery Worker (Process Email Jobs)
cd backend
celery -A celery_app worker --loglevel=info

# Terminal 5: Celery Beat (Schedule Email Jobs)
cd backend
celery -A celery_app beat --loglevel=info
```

### Celery Configuration

Located in `backend/celery_app.py`:

```python
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        'daily-reminder': {
            'task': 'celery_app.send_daily_reminders',
            'schedule': crontab(hour=18, minute=0),  # 6 PM UTC daily
        },
        'monthly-report': {
            'task': 'celery_app.send_monthly_reports',
            'schedule': crontab(day_of_month=1, hour=8, minute=0),  # 1st at 8 AM UTC
        },
    }
)
```

### Monitor Celery Tasks

#### Check Celery Status

```bash
# In a new terminal
cd backend
celery -A celery_app inspect active

# Shows active tasks being processed
celery -A celery_app inspect scheduled

# Shows scheduled tasks
celery -A celery_app inspect stats

# Shows worker stats
```

#### View Celery Logs

```bash
# Worker logs (Terminal 4)
# Shows task execution, errors, completions

# Beat logs (Terminal 5)
# Shows scheduled task triggers

# App logs (Terminal 2)
# Shows job queueing from API
```

### Testing Celery

#### Manually Trigger Daily Reminders

```bash
# From project root
cd backend
celery -A celery_app call celery_app.send_daily_reminders
```

#### Manually Trigger Monthly Reports

```bash
cd backend
celery -A celery_app call celery_app.send_monthly_reports
```

#### Trigger CSV Export from API

```bash
# First get user token
TOKEN=$(curl -s -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123","role":"admin"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Trigger export
curl -X POST -H "Authorization: Bearer $TOKEN" \
  http://localhost:5001/api/user/export
```

### Celery without Background Jobs

If you don't want to run Celery (optional):

1. Don't start Terminal 4 (Celery Worker)
2. Don't start Terminal 5 (Celery Beat)
3. Scheduled jobs won't run (daily reminders, monthly reports)
4. CSV export won't work
5. App still functions normally (just no async features)

### Email Configuration

For Celery jobs to send emails, you need Gmail credentials:

**Option 1: Environment Variables**

Create `.env` file:
```env
GMAIL_EMAIL=your-email@gmail.com
GMAIL_PASSWORD=your-app-password
```

**Option 2: Direct in Code**

Edit `backend/celery_app.py`:
```python
gmail_email = "your-email@gmail.com"
gmail_password = "your-app-password"
```

**Get Gmail App Password:**
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to App passwords
4. Select "Mail" and "Windows Computer"
5. Copy the 16-character password
6. Use this password (not your Gmail password)

### Troubleshooting Celery

#### "Redis connection refused"
```bash
# Make sure Redis is running (Terminal 1)
redis-server

# Check Redis status
redis-cli ping
# Should output: PONG
```

#### "No module named celery_app"
```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Then run Celery
celery -A celery_app worker --loglevel=info
```

#### Worker shows "No tasks available"
- This is normal - means it's waiting for jobs
- Check Beat terminal to see scheduled tasks
- Trigger a job manually to test

#### "Task received but not executing"
```bash
# Check if worker and beat are both running
# Worker processes tasks (Terminal 4)
# Beat schedules tasks (Terminal 5)
# Both are required
```

#### Celery logs not showing
```bash
# Increase verbosity
celery -A celery_app worker --loglevel=debug

# Or with Beat
celery -A celery_app beat --loglevel=debug
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
