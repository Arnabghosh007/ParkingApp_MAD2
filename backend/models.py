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
    """Initialize database with only admin user. No hardcoded sample data."""
    db.create_all()
    
    # Create admin user if not exists
    if not Admin.query.first():
        admin = Admin(username='admin', password='admin123', email='admin@parkingapp.com')
        db.session.add(admin)
        db.session.commit()
