from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password, email=None):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': 'admin'
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    vehicle_number = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    pin_code = db.Column(db.String(10), nullable=True)
    last_visit = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    reservations = db.relationship('ReserveParkingSpot', backref='user', lazy=True)

    def __init__(self, username, password, full_name=None, email=None, vehicle_number=None, 
                 phone=None, address=None, pin_code=None):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.full_name = full_name
        self.email = email
        self.vehicle_number = vehicle_number
        self.phone = phone
        self.address = address
        self.pin_code = pin_code

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'vehicle_number': self.vehicle_number,
            'phone': self.phone,
            'address': self.address,
            'pin_code': self.pin_code,
            'last_visit': self.last_visit.isoformat() if self.last_visit else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'role': 'user'
        }

class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    parking_spots = db.relationship('ParkingSpot', backref='parking_lot', lazy=True, cascade='all, delete-orphan')

    def __init__(self, prime_location_name, price, address, pin_code, number_of_spots):
        self.prime_location_name = prime_location_name
        self.price = price
        self.address = address
        self.pin_code = pin_code
        self.number_of_spots = number_of_spots

    def to_dict(self):
        available_count = ParkingSpot.query.filter_by(lot_id=self.id, status='A').count()
        occupied_count = ParkingSpot.query.filter_by(lot_id=self.id, status='O').count()
        return {
            'id': self.id,
            'prime_location_name': self.prime_location_name,
            'price': self.price,
            'address': self.address,
            'pin_code': self.pin_code,
            'number_of_spots': self.number_of_spots,
            'available_spots': available_count,
            'occupied_spots': occupied_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')
    vehicle_number = db.Column(db.String(20), nullable=True)
    
    reservations = db.relationship('ReserveParkingSpot', backref='spot', lazy=True)

    def __init__(self, lot_id, status='A', vehicle_number=None):
        self.lot_id = lot_id
        self.status = status
        self.vehicle_number = vehicle_number

    def to_dict(self):
        return {
            'id': self.id,
            'lot_id': self.lot_id,
            'status': self.status,
            'status_label': 'Occupied' if self.status == 'O' else 'Available',
            'vehicle_number': self.vehicle_number
        }

class ReserveParkingSpot(db.Model):
    __tablename__ = 'reserve_parking_spots'
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_number = db.Column(db.String(50), nullable=True)
    parking_timestamp = db.Column(db.DateTime, nullable=False)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=True)
    remarks = db.Column(db.String(200), nullable=True)

    def __init__(self, spot_id, user_id, parking_timestamp, vehicle_number=None):
        self.spot_id = spot_id
        self.user_id = user_id
        self.parking_timestamp = parking_timestamp
        self.vehicle_number = vehicle_number

    def to_dict(self):
        spot = ParkingSpot.query.get(self.spot_id)
        lot = ParkingLot.query.get(spot.lot_id) if spot else None
        return {
            'id': self.id,
            'spot_id': self.spot_id,
            'lot_id': spot.lot_id if spot else None,
            'lot_name': lot.prime_location_name if lot else None,
            'lot_address': lot.address if lot else None,
            'user_id': self.user_id,
            'vehicle_number': self.vehicle_number,
            'parking_timestamp': self.parking_timestamp.isoformat() if self.parking_timestamp else None,
            'leaving_timestamp': self.leaving_timestamp.isoformat() if self.leaving_timestamp else None,
            'parking_cost': self.parking_cost,
            'remarks': self.remarks,
            'is_active': self.leaving_timestamp is None
        }

class ExportJob(db.Model):
    __tablename__ = 'export_jobs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    file_path = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'file_path': self.file_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('reserve_parking_spots.id'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    card_number = db.Column(db.String(20), nullable=False)
    expiry = db.Column(db.String(10), nullable=False)
    cvv = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='completed')
    transaction_id = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='payments')
    booking = db.relationship('ReserveParkingSpot', backref='payment')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'booking_id': self.booking_id,
            'amount': self.amount,
            'card_number': f"****{self.card_number[-4:]}",
            'status': self.status,
            'transaction_id': self.transaction_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

def init_db():
    db.create_all()
    
    if not Admin.query.first():
        admin = Admin(username='admin', password='admin123', email='admin@parkingapp.com')
        db.session.add(admin)
        db.session.commit()
    
    # Add sample parking lots (hardcoded) - ensure all 15 are created
    if ParkingLot.query.count() < 15:
        lots_data = [
            {'name': 'Central Plaza Parking', 'price': 50, 'address': '123 Central Ave, Downtown', 'pin': '110001', 'spots': 50},
            {'name': 'Airport Terminal Lot', 'price': 100, 'address': 'Airport Road, Terminal-2', 'pin': '110037', 'spots': 100},
            {'name': 'Mall Garage Downtown', 'price': 30, 'address': '456 Shopping St, Mall Area', 'pin': '110002', 'spots': 75},
            {'name': 'IT Park Tech Hub', 'price': 75, 'address': '789 Tech Park, Sector-32', 'pin': '110032', 'spots': 60},
            {'name': 'Metro Station Plaza', 'price': 40, 'address': '321 Metro Rd, Near Station', 'pin': '110003', 'spots': 80},
            {'name': 'Hospital Complex Parking', 'price': 60, 'address': '654 Medical Lane, Hospital', 'pin': '110004', 'spots': 40},
            {'name': 'Business District Tower', 'price': 85, 'address': '987 Business Ave, Tower-A', 'pin': '110005', 'spots': 120},
            {'name': 'University Campus Lot', 'price': 20, 'address': '111 Campus Rd, University', 'pin': '110006', 'spots': 150},
            {'name': 'Convention Center', 'price': 90, 'address': '222 Convention Way, Hall-1', 'pin': '110007', 'spots': 200},
            {'name': 'Sports Complex', 'price': 45, 'address': '333 Sports Ave, Stadium', 'pin': '110008', 'spots': 100},
            {'name': 'Shopping Mall Extension', 'price': 35, 'address': '444 Mall Road, Extension', 'pin': '110009', 'spots': 90},
            {'name': 'Tech Park Tower-2', 'price': 80, 'address': '555 Tech Tower, Sector-30', 'pin': '110010', 'spots': 70},
            {'name': 'Railway Station', 'price': 25, 'address': '666 Railway Rd, Main Station', 'pin': '110011', 'spots': 130},
            {'name': 'Commercial Plaza', 'price': 65, 'address': '777 Commerce St, Plaza-B', 'pin': '110012', 'spots': 60},
            {'name': 'Beach Resort Parking', 'price': 70, 'address': '888 Beach Rd, Resort Area', 'pin': '110013', 'spots': 110},
        ]
        
        for lot in lots_data:
            parking_lot = ParkingLot(
                prime_location_name=lot['name'],
                price=lot['price'],
                address=lot['address'],
                pin_code=lot['pin'],
                number_of_spots=lot['spots']
            )
            db.session.add(parking_lot)
        db.session.commit()
        
        # Create parking spots for each lot
        for lot in ParkingLot.query.all():
            for i in range(lot.number_of_spots):
                spot = ParkingSpot(lot_id=lot.id, status='A')
                db.session.add(spot)
        db.session.commit()
    
    # Add sample users (hardcoded) - ensure all 18 are created
    if User.query.count() < 18:
        users_data = [
            {'username': 'demo', 'password': 'demo123', 'name': 'Demo User', 'email': 'demo@test.com', 'vehicle': 'DL-01-AB-1234', 'phone': '9876543210'},
            {'username': 'john_doe', 'password': 'john123', 'name': 'John Doe', 'email': 'john@test.com', 'vehicle': 'DL-01-AB-5678', 'phone': '9876543211'},
            {'username': 'jane_smith', 'password': 'jane123', 'name': 'Jane Smith', 'email': 'jane@test.com', 'vehicle': 'MH-02-CD-9876', 'phone': '9876543212'},
            {'username': 'alex_kumar', 'password': 'alex123', 'name': 'Alex Kumar', 'email': 'alex@test.com', 'vehicle': 'KA-03-EF-5432', 'phone': '9876543213'},
            {'username': 'priya_sharma', 'password': 'priya123', 'name': 'Priya Sharma', 'email': 'priya@test.com', 'vehicle': 'TN-04-GH-1098', 'phone': '9876543214'},
            {'username': 'rahul_patel', 'password': 'rahul123', 'name': 'Rahul Patel', 'email': 'rahul@test.com', 'vehicle': 'GJ-05-IJ-7654', 'phone': '9876543215'},
            {'username': 'arun_singh', 'password': 'arun123', 'name': 'Arun Singh', 'email': 'arun@test.com', 'vehicle': 'UP-06-KL-3210', 'phone': '9876543216'},
            {'username': 'neha_gupta', 'password': 'neha123', 'name': 'Neha Gupta', 'email': 'neha@test.com', 'vehicle': 'HR-07-MN-9876', 'phone': '9876543217'},
            {'username': 'vikram_khan', 'password': 'vikram123', 'name': 'Vikram Khan', 'email': 'vikram@test.com', 'vehicle': 'WB-08-OP-5432', 'phone': '9876543218'},
            {'username': 'divya_verma', 'password': 'divya123', 'name': 'Divya Verma', 'email': 'divya@test.com', 'vehicle': 'RJ-09-QR-1234', 'phone': '9876543219'},
            {'username': 'arjun_nair', 'password': 'arjun123', 'name': 'Arjun Nair', 'email': 'arjun@test.com', 'vehicle': 'KL-10-ST-5678', 'phone': '9876543220'},
            {'username': 'ishita_roy', 'password': 'ishita123', 'name': 'Ishita Roy', 'email': 'ishita@test.com', 'vehicle': 'AS-11-UV-9876', 'phone': '9876543221'},
            {'username': 'rohit_mehra', 'password': 'rohit123', 'name': 'Rohit Mehra', 'email': 'rohit@test.com', 'vehicle': 'DL-12-WX-3210', 'phone': '9876543222'},
            {'username': 'sneha_desai', 'password': 'sneha123', 'name': 'Sneha Desai', 'email': 'sneha@test.com', 'vehicle': 'MH-13-YZ-7654', 'phone': '9876543223'},
            {'username': 'manish_choudhury', 'password': 'manish123', 'name': 'Manish Choudhury', 'email': 'manish@test.com', 'vehicle': 'OR-14-AB-1098', 'phone': '9876543224'},
            {'username': 'anjali_iyer', 'password': 'anjali123', 'name': 'Anjali Iyer', 'email': 'anjali@test.com', 'vehicle': 'TG-15-CD-5432', 'phone': '9876543225'},
            {'username': 'karthik_reddy', 'password': 'karthik123', 'name': 'Karthik Reddy', 'email': 'karthik@test.com', 'vehicle': 'AP-16-EF-9876', 'phone': '9876543226'},
            {'username': 'pooja_malhotra', 'password': 'pooja123', 'name': 'Pooja Malhotra', 'email': 'pooja@test.com', 'vehicle': 'PB-17-GH-3210', 'phone': '9876543227'},
        ]
        
        for user in users_data:
            new_user = User(
                username=user['username'],
                password=user['password'],
                full_name=user['name'],
                email=user['email'],
                vehicle_number=user['vehicle'],
                phone=user['phone']
            )
            db.session.add(new_user)
        db.session.commit()
    
    # Add sample bookings (hardcoded)
    if not ReserveParkingSpot.query.first():
        now = datetime.utcnow()
        demo_user = User.query.filter_by(username='demo').first()
        lots = ParkingLot.query.all()
        
        if demo_user and lots:
            # Create 15 realistic bookings with various statuses
            booking_data = [
                # Active bookings (no leaving_timestamp)
                {'user': demo_user, 'lot_idx': 0, 'vehicle': 'DL-01-AB-1234', 'hours_ago': 2, 'complete': False},
                {'user': User.query.filter_by(username='john_doe').first(), 'lot_idx': 1, 'vehicle': 'DL-01-AB-5678', 'hours_ago': 1, 'complete': False},
                {'user': User.query.filter_by(username='jane_smith').first(), 'lot_idx': 2, 'vehicle': 'MH-02-CD-9876', 'hours_ago': 0.5, 'complete': False},
                
                # Completed bookings (with leaving_timestamp and cost)
                {'user': User.query.filter_by(username='alex_kumar').first(), 'lot_idx': 3, 'vehicle': 'KA-03-EF-5432', 'hours_ago': 5, 'complete': True, 'duration': 3},
                {'user': User.query.filter_by(username='priya_sharma').first(), 'lot_idx': 4, 'vehicle': 'TN-04-GH-1098', 'hours_ago': 24, 'complete': True, 'duration': 2},
                {'user': User.query.filter_by(username='rahul_patel').first(), 'lot_idx': 0, 'vehicle': 'GJ-05-IJ-7654', 'hours_ago': 48, 'complete': True, 'duration': 4},
                {'user': User.query.filter_by(username='arun_singh').first(), 'lot_idx': 1, 'vehicle': 'UP-06-KL-3210', 'hours_ago': 72, 'complete': True, 'duration': 1.5},
                {'user': User.query.filter_by(username='neha_gupta').first(), 'lot_idx': 2, 'vehicle': 'HR-07-MN-9876', 'hours_ago': 96, 'complete': True, 'duration': 2.5},
                {'user': User.query.filter_by(username='vikram_khan').first(), 'lot_idx': 3, 'vehicle': 'WB-08-OP-5432', 'hours_ago': 120, 'complete': True, 'duration': 3},
                {'user': demo_user, 'lot_idx': 4, 'vehicle': 'DL-01-AB-1234', 'hours_ago': 144, 'complete': True, 'duration': 5},
            ]
            
            for booking in booking_data:
                if booking['user']:
                    lot = lots[booking['lot_idx']]
                    parking_spot = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').first()
                    
                    if parking_spot:
                        start_time = now - timedelta(hours=booking['hours_ago'])
                        
                        reservation = ReserveParkingSpot(
                            spot_id=parking_spot.id,
                            user_id=booking['user'].id,
                            parking_timestamp=start_time,
                            vehicle_number=booking['vehicle']
                        )
                        
                        if booking['complete']:
                            duration = booking.get('duration', 1)
                            reservation.leaving_timestamp = start_time + timedelta(hours=duration)
                            reservation.parking_cost = round(lot.price * duration, 2)
                            parking_spot.status = 'A'
                        else:
                            parking_spot.status = 'O'
                            parking_spot.vehicle_number = booking['vehicle']
                        
                        db.session.add(reservation)
                        db.session.add(parking_spot)
            
            db.session.commit()
