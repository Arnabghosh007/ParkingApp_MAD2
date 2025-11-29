from celery import Celery
from celery.schedules import crontab
import os

def make_celery(app=None):
    celery = Celery(
        'parking_app',
        broker=os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
        backend=os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    )
    
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        beat_schedule={
            'daily-reminder': {
                'task': 'celery_app.send_daily_reminders',
                'schedule': crontab(hour=18, minute=0),
            },
            'monthly-report': {
                'task': 'celery_app.send_monthly_reports',
                'schedule': crontab(day_of_month=1, hour=8, minute=0),
            },
        }
    )
    
    return celery

celery = make_celery()

@celery.task
def send_daily_reminders():
    from app import app
    from models import db, User, ParkingLot, ReserveParkingSpot
    from datetime import datetime, timedelta
    import requests
    
    with app.app_context():
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        users = User.query.filter(
            (User.last_visit < yesterday) | (User.last_visit == None)
        ).all()
        
        new_lots = ParkingLot.query.filter(
            ParkingLot.created_at >= yesterday
        ).all()
        
        for user in users:
            if user.email:
                message = f"Hello {user.full_name or user.username}! "
                message += "We noticed you haven't visited our parking app recently. "
                
                if new_lots:
                    message += f"We have {len(new_lots)} new parking lots available! "
                
                message += "Book a parking spot today!"
                
                print(f"Reminder sent to {user.email}: {message}")
        
        return f"Sent reminders to {len(users)} users"

@celery.task
def send_monthly_reports():
    from app import app
    from models import db, User, ReserveParkingSpot, ParkingSpot, ParkingLot
    from datetime import datetime
    
    with app.app_context():
        users = User.query.all()
        
        for user in users:
            if not user.email:
                continue
            
            now = datetime.utcnow()
            first_of_month = datetime(now.year, now.month, 1)
            
            bookings = ReserveParkingSpot.query.filter(
                ReserveParkingSpot.user_id == user.id,
                ReserveParkingSpot.parking_timestamp >= first_of_month
            ).all()
            
            if not bookings:
                continue
            
            total_spent = sum(b.parking_cost or 0 for b in bookings)
            total_bookings = len(bookings)
            
            lot_usage = {}
            for b in bookings:
                spot = ParkingSpot.query.get(b.spot_id)
                if spot:
                    lot = ParkingLot.query.get(spot.lot_id)
                    if lot:
                        lot_usage[lot.prime_location_name] = lot_usage.get(lot.prime_location_name, 0) + 1
            
            most_used_lot = max(lot_usage, key=lot_usage.get) if lot_usage else 'N/A'
            
            report_html = f"""
            <html>
            <head><style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background: #4CAF50; color: white; padding: 20px; }}
                .content {{ padding: 20px; }}
                .stat {{ margin: 10px 0; padding: 10px; background: #f5f5f5; }}
            </style></head>
            <body>
                <div class="header">
                    <h1>Monthly Parking Report</h1>
                    <p>{now.strftime('%B %Y')}</p>
                </div>
                <div class="content">
                    <p>Hello {user.full_name or user.username},</p>
                    <p>Here's your parking activity summary for this month:</p>
                    
                    <div class="stat">
                        <strong>Total Bookings:</strong> {total_bookings}
                    </div>
                    <div class="stat">
                        <strong>Total Amount Spent:</strong> Rs. {total_spent:.2f}
                    </div>
                    <div class="stat">
                        <strong>Most Used Parking Lot:</strong> {most_used_lot}
                    </div>
                    
                    <p>Thank you for using our Vehicle Parking App!</p>
                </div>
            </body>
            </html>
            """
            
            print(f"Monthly report generated for {user.email}")
        
        return f"Generated reports for {len(users)} users"

@celery.task
def generate_csv_task(job_id):
    from app import app
    from models import db, ExportJob, ReserveParkingSpot, ParkingSpot, ParkingLot
    from datetime import datetime
    import csv
    import os
    
    with app.app_context():
        job = ExportJob.query.get(job_id)
        if not job:
            return
        
        try:
            bookings = ReserveParkingSpot.query.filter_by(user_id=job.user_id).all()
            
            os.makedirs('exports', exist_ok=True)
            filename = f'exports/parking_history_{job.user_id}_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.csv'
            
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Booking ID', 'Spot ID', 'Lot Name', 'Vehicle Number', 
                               'Parking Time', 'Leaving Time', 'Duration (Hours)', 'Cost', 'Remarks'])
                
                for b in bookings:
                    spot = ParkingSpot.query.get(b.spot_id)
                    lot = ParkingLot.query.get(spot.lot_id) if spot else None
                    
                    if b.leaving_timestamp:
                        duration = (b.leaving_timestamp - b.parking_timestamp).total_seconds() / 3600
                    else:
                        duration = (datetime.utcnow() - b.parking_timestamp).total_seconds() / 3600
                    
                    writer.writerow([
                        b.id, b.spot_id, lot.prime_location_name if lot else 'N/A',
                        b.vehicle_number, b.parking_timestamp, b.leaving_timestamp,
                        round(duration, 2), b.parking_cost, b.remarks
                    ])
            
            job.status = 'completed'
            job.file_path = filename
            job.completed_at = datetime.utcnow()
            db.session.commit()
            
            print(f"Export completed for job {job_id}")
            
        except Exception as e:
            job.status = 'failed'
            db.session.commit()
            raise e
