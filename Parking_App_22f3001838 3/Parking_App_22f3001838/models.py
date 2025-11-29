from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Store hashed password

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)  # Hash the password

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# User Model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Store hashed password
    full_name = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    confirm_email = db.Column(db.String(120), nullable=True)
    vehicle_number = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    postcode = db.Column(db.String(20), nullable=True)
    communication_mode = db.Column(db.String(20), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=True)
    car_park_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    pin_code = db.Column(db.String(10), nullable=True)
    reservations = db.relationship('ReserveParkingSpot', backref='user', lazy=True)

    def __init__(self, username, password, full_name=None, email=None, confirm_email=None, vehicle_number=None, phone=None, gender=None, postcode=None, communication_mode=None, age=None, city_id=None, car_park_id=None, address=None, pin_code=None):
        self.username = username
        self.password_hash = generate_password_hash(password)  # Hash the password
        self.full_name = full_name
        self.email = email
        self.confirm_email = confirm_email
        self.vehicle_number = vehicle_number
        self.phone = phone
        self.gender = gender
        self.postcode = postcode
        self.communication_mode = communication_mode
        self.age = age
        self.city_id = city_id
        self.car_park_id = car_park_id
        self.address = address
        self.pin_code = pin_code

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# City Model
class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    parking_lots = db.relationship('ParkingLot', backref='city', lazy=True)

    def __init__(self, name):
        self.name = name

# ParkingLot, ParkingSpot, and ReserveParkingSpot models remain unchanged
class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    prime_location_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    maximum_number_of_spots = db.Column(db.Integer, nullable=False)
    parking_spots = db.relationship('ParkingSpot', backref='parking_lot', lazy=True)

    def __init__(self, city_id, prime_location_name, price, address, pin_code, maximum_number_of_spots):
        self.city_id = city_id
        self.prime_location_name = prime_location_name
        self.price = price
        self.address = address
        self.pin_code = pin_code
        self.maximum_number_of_spots = maximum_number_of_spots

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')  # O-occupied, A-available
    vehicle_number = db.Column(db.String(20), nullable=True)

    def __init__(self, lot_id, status='A', vehicle_number=None):
        self.lot_id = lot_id
        self.status = status
        self.vehicle_number = vehicle_number

class ReserveParkingSpot(db.Model):
    __tablename__ = 'reserve_parking_spots'
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost_per_unit = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=True)

    def __init__(self, spot_id, user_id, parking_timestamp, parking_cost_per_unit):
        self.spot_id = spot_id
        self.user_id = user_id
        self.parking_timestamp = parking_timestamp
        self.parking_cost_per_unit = parking_cost_per_unit

class BookingRequest(db.Model):
    __tablename__ = 'booking_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    vehicle_number = db.Column(db.String(50), nullable=False)
    parking_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in hours
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, approved, rejected
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', backref='booking_requests')
    lot = db.relationship('ParkingLot', backref='booking_requests')
    spot = db.relationship('ParkingSpot', backref='booking_requests')

# Function to create the database and add a default admin
def init_db():
    db.create_all()
    
    # Add default admin
    if not Admin.query.first():
        admin = Admin(username='admin', password='admin123')
        db.session.add(admin)
        db.session.commit()
    
    # Add sample cities if none exist
    if not City.query.first():
        cities = [
            City('Mumbai'),
            City('Delhi'),
            City('Bangalore'),
            City('Chennai'),
            City('Kolkata'),
            City('Hyderabad'),
            City('Pune'),
            City('Ahmedabad')
        ]
        for city in cities:
            db.session.add(city)
        db.session.commit()
    
    # Add sample parking lots if none exist
    if not ParkingLot.query.first():
        # Get city IDs
        mumbai = City.query.filter_by(name='Mumbai').first()
        delhi = City.query.filter_by(name='Delhi').first()
        bangalore = City.query.filter_by(name='Bangalore').first()
        
        parking_lots = [
            # Mumbai parking lots
            ParkingLot(mumbai.id, 'Bandra West Mall', 50.0, 'Linking Road, Bandra West', '400050', 100),
            ParkingLot(mumbai.id, 'Andheri Station', 30.0, 'Andheri East, Near Station', '400069', 150),
            ParkingLot(mumbai.id, 'Powai Business Hub', 40.0, 'Hiranandani, Powai', '400076', 80),
            
            # Delhi parking lots
            ParkingLot(delhi.id, 'Connaught Place', 45.0, 'CP, Central Delhi', '110001', 120),
            ParkingLot(delhi.id, 'Gurgaon Cyber City', 35.0, 'DLF Phase 2, Gurgaon', '122002', 200),
            ParkingLot(delhi.id, 'Karol Bagh Market', 25.0, 'Karol Bagh, Central Delhi', '110005', 90),
            
            # Bangalore parking lots
            ParkingLot(bangalore.id, 'MG Road Metro', 40.0, 'MG Road, Brigade Road', '560001', 110),
            ParkingLot(bangalore.id, 'Electronic City', 30.0, 'Electronic City Phase 1', '560100', 180),
            ParkingLot(bangalore.id, 'Koramangala', 35.0, '5th Block, Koramangala', '560095', 75)
        ]
        
        for lot in parking_lots:
            db.session.add(lot)
        db.session.commit()
        
        # Add parking spots for each lot
        for lot in ParkingLot.query.all():
            for i in range(lot.maximum_number_of_spots):
                spot = ParkingSpot(lot.id, 'A')  # 'A' = Available
                db.session.add(spot)
        db.session.commit()