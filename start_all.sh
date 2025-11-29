#!/bin/bash

# Start Redis
redis-server --daemonize yes 2>/dev/null
sleep 1

# Start Flask backend
cd /home/runner/workspace
python backend/app.py > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend started (PID: $BACKEND_PID)"
sleep 3

# Start Celery Worker
cd /home/runner/workspace/backend
celery -A celery_app worker --loglevel=info > /tmp/celery_worker.log 2>&1 &
WORKER_PID=$!
echo "Celery Worker started (PID: $WORKER_PID)"
sleep 2

# Start Celery Beat (scheduler)
celery -A celery_app beat --loglevel=info > /tmp/celery_beat.log 2>&1 &
BEAT_PID=$!
echo "Celery Beat started (PID: $BEAT_PID)"
sleep 2

# Start Frontend
cd /home/runner/workspace/frontend
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend started (PID: $FRONTEND_PID)"
sleep 5

echo "✅ All services started!"
echo "Backend: PID $BACKEND_PID"
echo "Celery Worker: PID $WORKER_PID"
echo "Celery Beat: PID $BEAT_PID"
echo "Frontend: PID $FRONTEND_PID"
