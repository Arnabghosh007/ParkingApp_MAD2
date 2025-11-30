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
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    with app.app_context():
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        users = User.query.filter(
            (User.last_visit < yesterday) | (User.last_visit == None)
        ).all()
        
        new_lots = ParkingLot.query.filter(
            ParkingLot.created_at >= yesterday
        ).all()
        
        gmail_email = os.environ.get('GMAIL_EMAIL')
        gmail_password = os.environ.get('GMAIL_PASSWORD')
        
        if not gmail_email or not gmail_password:
            return "Gmail credentials not configured"
        
        sent_count = 0
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_email, gmail_password)
            
            for user in users:
                if not user.email:
                    continue
                
                message = f"Hello {user.full_name or user.username}!\n\n"
                message += "We noticed you haven't visited our parking app recently. "
                
                if new_lots:
                    message += f"We have {len(new_lots)} new parking lots available!\n\n"
                    for lot in new_lots:
                        message += f"- {lot.prime_location_name}: Rs. {lot.price}/day\n"
                
                message += "\nBook a parking spot today at our app!"
                
                msg = MIMEMultipart()
                msg['From'] = gmail_email
                msg['To'] = user.email
                msg['Subject'] = 'Daily Parking Reminder - Book Your Spot!'
                msg.attach(MIMEText(message, 'plain'))
                
                server.send_message(msg)
                sent_count += 1
                print(f"Reminder sent to {user.email}")
            
            server.quit()
        except Exception as e:
            print(f"Error sending reminders: {str(e)}")
            return f"Error: {str(e)}"
        
        return f"Sent reminders to {sent_count} users"

@celery.task
def send_monthly_reports():
    from app import app
    from models import db, User, ReserveParkingSpot, ParkingSpot, ParkingLot
    from datetime import datetime
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from io import BytesIO
    
    with app.app_context():
        users = User.query.all()
        
        gmail_email = os.environ.get('GMAIL_EMAIL')
        gmail_password = os.environ.get('GMAIL_PASSWORD')
        
        if not gmail_email or not gmail_password:
            return "Gmail credentials not configured"
        
        sent_count = 0
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_email, gmail_password)
            
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
                total_hours = 0
                
                lot_usage = {}
                for b in bookings:
                    spot = ParkingSpot.query.get(b.spot_id)
                    if spot:
                        lot = ParkingLot.query.get(spot.lot_id)
                        if lot:
                            lot_usage[lot.prime_location_name] = lot_usage.get(lot.prime_location_name, 0) + 1
                    if b.leaving_timestamp:
                        hours = (b.leaving_timestamp - b.parking_timestamp).total_seconds() / 3600
                    else:
                        hours = (now - b.parking_timestamp).total_seconds() / 3600
                    total_hours += hours
                
                most_used_lot = max(lot_usage, key=lot_usage.get) if lot_usage else 'N/A'
                
                pdf_buffer = BytesIO()
                doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
                story = []
                styles = getSampleStyleSheet()
                
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=24,
                    textColor=colors.HexColor('#667eea'),
                    spaceAfter=10,
                    alignment=1
                )
                
                story.append(Paragraph("Monthly Parking Activity Report", title_style))
                story.append(Paragraph(now.strftime('%B %Y'), styles['Heading3']))
                story.append(Spacer(1, 0.3*inch))
                
                story.append(Paragraph(f"Dear {user.full_name or user.username},", styles['Normal']))
                story.append(Spacer(1, 0.2*inch))
                story.append(Paragraph("Here's your parking activity summary for this month:", styles['Normal']))
                story.append(Spacer(1, 0.3*inch))
                
                data = [
                    ['Metric', 'Value'],
                    ['Total Bookings', str(total_bookings)],
                    ['Total Hours Parked', f'{round(total_hours, 2)}h'],
                    ['Total Amount Spent', f'Rs. {total_spent:.2f}'],
                    ['Most Used Parking Lot', str(most_used_lot)]
                ]
                
                table = Table(data, colWidths=[3*inch, 2*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(table)
                story.append(Spacer(1, 0.3*inch))
                story.append(Paragraph("Thank you for using our Vehicle Parking App!", styles['Normal']))
                
                doc.build(story)
                pdf_buffer.seek(0)
                
                msg = MIMEMultipart()
                msg['From'] = gmail_email
                msg['To'] = user.email
                msg['Subject'] = f"Monthly Parking Report - {now.strftime('%B %Y')}"
                
                msg.attach(MIMEText(f"Hello {user.full_name or user.username},\n\nPlease find attached your monthly parking activity report.\n\nBest regards,\nParking App Team", 'plain'))
                
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(pdf_buffer.getvalue())
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', f'attachment; filename= parking_report_{now.strftime("%B_%Y")}.pdf')
                msg.attach(attachment)
                
                server.send_message(msg)
                sent_count += 1
                print(f"Monthly PDF report sent to {user.email}")
            
            server.quit()
        except Exception as e:
            print(f"Error sending reports: {str(e)}")
            return f"Error: {str(e)}"
        
        return f"Sent reports to {sent_count} users"

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
