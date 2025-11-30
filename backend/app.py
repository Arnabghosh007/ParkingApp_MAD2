from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_caching import Cache
from datetime import datetime, timedelta
from functools import wraps
import os

from config import Config
from models import db, init_db, Admin, User, ParkingLot, ParkingSpot, ReserveParkingSpot, ExportJob

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
app.config.from_object(Config)

CORS(app, resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager(app)
cache = Cache(app)
db.init_app(app)

import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    try:
        return redis_client.exists(f"blocklist:{jti}") > 0
    except:
        return False

def add_token_to_blocklist(jti, expires_in=86400):
    try:
        redis_client.setex(f"blocklist:{jti}", expires_in, "revoked")
    except:
        pass

with app.app_context():
    init_db()

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

def user_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') != 'user':
            return jsonify({'error': 'User access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    if role == 'admin':
        admin = Admin.query.filter_by(username=username).first()
        if not admin:
            return jsonify({'error': f'Admin username "{username}" not found'}), 401
        if not admin.check_password(password):
            return jsonify({'error': 'Incorrect password for this admin account'}), 401
        
        access_token = create_access_token(
            identity=str(admin.id),
            additional_claims={'role': 'admin', 'username': admin.username}
        )
        refresh_token = create_refresh_token(
            identity=str(admin.id),
            additional_claims={'role': 'admin'}
        )
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': admin.to_dict()
        })
    else:
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': f'User "{username}" not found. Please register first'}), 401
        if not user.check_password(password):
            return jsonify({'error': 'Incorrect password. Please try again'}), 401
        
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': 'user', 'username': user.username}
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),
            additional_claims={'role': 'user'}
        )
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        })

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    full_name = data.get('full_name')
    vehicle_number = data.get('vehicle_number')
    phone = data.get('phone')
    address = data.get('address')
    pin_code = data.get('pin_code')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if email and User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    user = User(
        username=username,
        password=password,
        email=email,
        full_name=full_name,
        vehicle_number=vehicle_number,
        phone=phone,
        address=address,
        pin_code=pin_code
    )
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={'role': 'user', 'username': user.username}
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        additional_claims={'role': 'user'}
    )
    
    return jsonify({
        'message': 'Registration successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 201

@app.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    add_token_to_blocklist(jti)
    return jsonify({'message': 'Successfully logged out'})

@app.route('/api/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    claims = get_jwt()
    access_token = create_access_token(
        identity=identity,
        additional_claims={'role': claims.get('role'), 'username': claims.get('username')}
    )
    return jsonify({'access_token': access_token})

@app.route('/api/admin/dashboard')
@admin_required
def admin_dashboard():
    total_lots = ParkingLot.query.count()
    total_spots = ParkingSpot.query.count()
    available_spots = ParkingSpot.query.filter_by(status='A').count()
    occupied_spots = ParkingSpot.query.filter_by(status='O').count()
    total_users = User.query.count()
    
    today = datetime.utcnow().date()
    today_bookings = ReserveParkingSpot.query.filter(
        db.func.date(ReserveParkingSpot.parking_timestamp) == today
    ).count()
    
    total_revenue = db.session.query(db.func.sum(ReserveParkingSpot.parking_cost)).scalar() or 0
    
    return jsonify({
        'total_lots': total_lots,
        'total_spots': total_spots,
        'available_spots': available_spots,
        'occupied_spots': occupied_spots,
        'total_users': total_users,
        'today_bookings': today_bookings,
        'total_revenue': round(total_revenue, 2),
        'occupancy_rate': round((occupied_spots / total_spots * 100) if total_spots > 0 else 0, 1)
    })

@app.route('/api/admin/users')
@admin_required
def get_all_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@app.route('/api/admin/parking-lots', methods=['GET'])
@admin_required
def get_parking_lots_admin():
    lots = ParkingLot.query.all()
    return jsonify([lot.to_dict() for lot in lots])

@app.route('/api/admin/parking-lots', methods=['POST'])
@admin_required
def create_parking_lot():
    data = request.get_json()
    
    required = ['prime_location_name', 'price', 'number_of_spots']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields: prime_location_name, price, number_of_spots'}), 400
    
    lot = ParkingLot(
        prime_location_name=data['prime_location_name'],
        price=float(data['price']),
        address=data.get('address', 'TBD'),
        pin_code=data.get('pin_code', 'TBD'),
        number_of_spots=int(data['number_of_spots'])
    )
    db.session.add(lot)
    db.session.flush()
    
    for i in range(int(data['number_of_spots'])):
        spot = ParkingSpot(lot_id=lot.id, status='A')
        db.session.add(spot)
    
    db.session.commit()
    cache.delete_memoized(get_parking_lots_cached)
    
    return jsonify(lot.to_dict()), 201

@app.route('/api/admin/parking-lots/<int:lot_id>', methods=['PUT'])
@admin_required
def update_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.get_json()
    
    if 'prime_location_name' in data:
        lot.prime_location_name = data['prime_location_name']
    if 'price' in data:
        lot.price = float(data['price'])
    if 'address' in data:
        lot.address = data['address']
    if 'pin_code' in data:
        lot.pin_code = data['pin_code']
    if 'number_of_spots' in data:
        new_count = int(data['number_of_spots'])
        current_count = len(lot.parking_spots)
        
        if new_count > current_count:
            for i in range(new_count - current_count):
                spot = ParkingSpot(lot_id=lot.id, status='A')
                db.session.add(spot)
        elif new_count < current_count:
            available_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').limit(current_count - new_count).all()
            if len(available_spots) < current_count - new_count:
                return jsonify({'error': 'Cannot reduce spots: some are occupied'}), 400
            for spot in available_spots:
                db.session.delete(spot)
        
        lot.number_of_spots = new_count
    
    db.session.commit()
    cache.delete_memoized(get_parking_lots_cached)
    
    return jsonify(lot.to_dict())

@app.route('/api/admin/parking-lots/<int:lot_id>', methods=['DELETE'])
@admin_required
def delete_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    
    occupied = ParkingSpot.query.filter_by(lot_id=lot_id, status='O').count()
    if occupied > 0:
        return jsonify({'error': 'Cannot delete lot: some spots are occupied'}), 400
    
    db.session.delete(lot)
    db.session.commit()
    cache.delete_memoized(get_parking_lots_cached)
    
    return jsonify({'message': 'Parking lot deleted successfully'})

@app.route('/api/admin/parking-lots/<int:lot_id>/spots')
@admin_required
def get_lot_spots_admin(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    
    result = []
    for spot in spots:
        spot_data = spot.to_dict()
        if spot.status == 'O':
            active_reservation = ReserveParkingSpot.query.filter_by(
                spot_id=spot.id, leaving_timestamp=None
            ).first()
            if active_reservation:
                user = User.query.get(active_reservation.user_id)
                spot_data['reservation'] = {
                    'user': user.full_name or user.username,
                    'vehicle_number': active_reservation.vehicle_number,
                    'parking_since': active_reservation.parking_timestamp.isoformat()
                }
        result.append(spot_data)
    
    return jsonify({
        'lot': lot.to_dict(),
        'spots': result
    })

@app.route('/api/admin/stats/summary')
@admin_required
def admin_stats_summary():
    from sqlalchemy import func
    
    lots = ParkingLot.query.all()
    lot_stats = []
    for lot in lots:
        bookings = db.session.query(func.count(ReserveParkingSpot.id)).join(
            ParkingSpot, ReserveParkingSpot.spot_id == ParkingSpot.id
        ).filter(ParkingSpot.lot_id == lot.id).scalar()
        
        revenue = db.session.query(func.sum(ReserveParkingSpot.parking_cost)).join(
            ParkingSpot, ReserveParkingSpot.spot_id == ParkingSpot.id
        ).filter(ParkingSpot.lot_id == lot.id).scalar() or 0
        
        lot_stats.append({
            'name': lot.prime_location_name,
            'total_bookings': bookings,
            'revenue': round(revenue, 2),
            'available': ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count(),
            'occupied': ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
        })
    
    return jsonify({'lot_stats': lot_stats})

@cache.memoize(timeout=60)
def get_parking_lots_cached():
    lots = ParkingLot.query.all()
    return [lot.to_dict() for lot in lots]

@app.route('/api/parking-lots')
@jwt_required()
def get_parking_lots():
    return jsonify(get_parking_lots_cached())

@app.route('/api/parking-lots/<int:lot_id>')
@jwt_required()
def get_parking_lot_detail(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    return jsonify(lot.to_dict())

@app.route('/api/user/profile')
@user_required
def get_user_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(int(user_id))
    return jsonify(user.to_dict())

@app.route('/api/user/profile', methods=['PUT'])
@user_required
def update_user_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(int(user_id))
    data = request.get_json()
    
    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'email' in data:
        user.email = data['email']
    if 'vehicle_number' in data:
        user.vehicle_number = data['vehicle_number']
    if 'phone' in data:
        user.phone = data['phone']
    if 'address' in data:
        user.address = data['address']
    if 'pin_code' in data:
        user.pin_code = data['pin_code']
    
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/api/user/bookings', methods=['GET'])
@user_required
def get_user_bookings():
    user_id = get_jwt_identity()
    active = ReserveParkingSpot.query.filter_by(
        user_id=int(user_id), leaving_timestamp=None
    ).all()
    return jsonify([b.to_dict() for b in active])

@app.route('/api/user/bookings', methods=['POST'])
@user_required
def book_spot():
    user_id = get_jwt_identity()
    data = request.get_json()
    lot_id = data.get('lot_id')
    vehicle_number = data.get('vehicle_number')
    
    if not lot_id:
        return jsonify({'error': 'Parking lot ID required'}), 400
    
    active = ReserveParkingSpot.query.filter_by(
        user_id=int(user_id), leaving_timestamp=None
    ).first()
    if active:
        return jsonify({'error': 'You already have an active booking'}), 400
    
    lot = ParkingLot.query.get_or_404(lot_id)
    available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    
    if not available_spot:
        return jsonify({'error': 'No available spots in this parking lot'}), 400
    
    user = User.query.get(int(user_id))
    if not vehicle_number:
        vehicle_number = user.vehicle_number
    
    available_spot.status = 'O'
    available_spot.vehicle_number = vehicle_number
    
    reservation = ReserveParkingSpot(
        spot_id=available_spot.id,
        user_id=int(user_id),
        parking_timestamp=datetime.utcnow(),
        vehicle_number=vehicle_number
    )
    db.session.add(reservation)
    db.session.commit()
    
    cache.delete_memoized(get_parking_lots_cached)
    
    return jsonify({
        'message': 'Spot booked successfully',
        'booking': reservation.to_dict(),
        'spot': available_spot.to_dict()
    }), 201

@app.route('/api/user/bookings/<int:booking_id>/release', methods=['POST'])
@user_required
def release_spot(booking_id):
    user_id = get_jwt_identity()
    reservation = ReserveParkingSpot.query.filter_by(
        id=booking_id, user_id=int(user_id), leaving_timestamp=None
    ).first_or_404()
    
    spot = ParkingSpot.query.get(reservation.spot_id)
    lot = ParkingLot.query.get(spot.lot_id)
    
    reservation.leaving_timestamp = datetime.utcnow()
    duration_hours = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds() / 3600
    reservation.parking_cost = round(duration_hours * lot.price, 2)
    
    spot.status = 'A'
    spot.vehicle_number = None
    
    db.session.commit()
    cache.delete_memoized(get_parking_lots_cached)
    
    return jsonify({
        'message': 'Spot released successfully',
        'booking': reservation.to_dict(),
        'duration_hours': round(duration_hours, 2),
        'cost': reservation.parking_cost
    })

@app.route('/api/user/bookings/history')
@user_required
def get_booking_history():
    user_id = get_jwt_identity()
    bookings = ReserveParkingSpot.query.filter_by(user_id=int(user_id)).order_by(
        ReserveParkingSpot.parking_timestamp.desc()
    ).all()
    return jsonify([b.to_dict() for b in bookings])

@app.route('/api/user/stats/summary')
@user_required
def user_stats_summary():
    user_id = get_jwt_identity()
    from sqlalchemy import func
    
    bookings = ReserveParkingSpot.query.filter_by(user_id=int(user_id)).all()
    
    total_bookings = len(bookings)
    total_spent = sum(b.parking_cost or 0 for b in bookings)
    total_hours = 0
    lot_usage = {}
    
    for b in bookings:
        if b.leaving_timestamp:
            hours = (b.leaving_timestamp - b.parking_timestamp).total_seconds() / 3600
        else:
            hours = (datetime.utcnow() - b.parking_timestamp).total_seconds() / 3600
        total_hours += hours
        
        spot = ParkingSpot.query.get(b.spot_id)
        if spot:
            lot = ParkingLot.query.get(spot.lot_id)
            if lot:
                lot_usage[lot.prime_location_name] = lot_usage.get(lot.prime_location_name, 0) + 1
    
    active_bookings = len([b for b in bookings if not b.leaving_timestamp])
    
    return jsonify({
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'completed_bookings': total_bookings - active_bookings,
        'total_spent': round(total_spent, 2),
        'total_hours': round(total_hours, 2),
        'lot_usage': lot_usage
    })

@app.route('/api/user/export', methods=['POST'])
@user_required
def trigger_export():
    user_id = get_jwt_identity()
    
    pending = ExportJob.query.filter_by(user_id=int(user_id), status='pending').first()
    if pending:
        return jsonify({'message': 'Export already in progress', 'job': pending.to_dict()})
    
    job = ExportJob(user_id=int(user_id), status='pending')
    db.session.add(job)
    db.session.commit()
    
    try:
        from celery_app import generate_csv_task
        generate_csv_task.delay(job.id)
    except Exception as e:
        import csv
        import io
        
        bookings = ReserveParkingSpot.query.filter_by(user_id=int(user_id)).all()
        
        os.makedirs('exports', exist_ok=True)
        filename = f'exports/parking_history_{user_id}_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.csv'
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Booking ID', 'Spot ID', 'Lot Name', 'Vehicle Number', 
                           'Parking Time', 'Leaving Time', 'Cost', 'Remarks'])
            
            for b in bookings:
                spot = ParkingSpot.query.get(b.spot_id)
                lot = ParkingLot.query.get(spot.lot_id) if spot else None
                writer.writerow([
                    b.id, b.spot_id, lot.prime_location_name if lot else 'N/A',
                    b.vehicle_number, b.parking_timestamp, b.leaving_timestamp,
                    b.parking_cost, b.remarks
                ])
        
        job.status = 'completed'
        job.file_path = filename
        job.completed_at = datetime.utcnow()
        db.session.commit()
    
    return jsonify({'message': 'Export started', 'job': job.to_dict()})

@app.route('/api/user/export/<int:job_id>')
@user_required
def get_export_status(job_id):
    user_id = get_jwt_identity()
    job = ExportJob.query.filter_by(id=job_id, user_id=int(user_id)).first_or_404()
    return jsonify(job.to_dict())

@app.route('/api/user/export/<int:job_id>/download')
@user_required
def download_export(job_id):
    user_id = get_jwt_identity()
    job = ExportJob.query.filter_by(id=job_id, user_id=int(user_id), status='completed').first_or_404()
    
    if not job.file_path or not os.path.exists(job.file_path):
        return jsonify({'error': 'Export file not found'}), 404
    
    return send_file(job.file_path, as_attachment=True, download_name=f'parking_history.csv')

@app.route('/<path:path>')
def serve_spa(path):
    """Catch-all route to serve the Vue SPA for all non-API routes"""
    if path.startswith('api/'):
        return jsonify({'error': 'Not Found'}), 404
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
