from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, init_db, User, Admin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables first

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')  # Use env variable with fallback

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///parking.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    init_db()  # Creates default admin with hashed password

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        if not role:
            flash('Please select a role!', 'danger')
            return redirect(url_for('login'))
        username = request.form.get('username')
        password = request.form.get('password')

        if role == 'user':
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):  # Verify hashed password
                session['user_id'] = user.id
                flash('Login successful as User!', 'success')
                return redirect(url_for('user_dashboard'))
            else:
                flash('Invalid credentials for User!', 'danger')
        elif role == 'admin':
            admin = Admin.query.filter_by(username=username).first()
            if admin and admin.check_password(password):  # Verify hashed password
                session['admin_id'] = admin.id
                flash('Login successful as Admin!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid credentials for Admin!', 'danger')

        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    from models import City, ParkingLot
    cities = City.query.all()
    selected_city_id = None
    car_parks = []
    form_data = {}
    if request.method == 'POST':
        form_data = request.form.to_dict()
        selected_city_id = form_data.get('city')
        if selected_city_id:
            car_parks = ParkingLot.query.filter_by(city_id=selected_city_id).all()
        # If the form is fully filled (has car_park and other required fields), handle registration logic here
        if form_data.get('car_park') and form_data.get('full_name') and form_data.get('username'):
            from models import User, db
            # Check if username is unique
            if User.query.filter_by(username=form_data['username']).first():
                flash('Username already exists. Please choose another.', 'danger')
            else:
                new_user = User(
                    username=form_data['username'],
                    password=form_data['password'],
                    full_name=form_data.get('full_name'),
                    email=form_data.get('email'),
                    confirm_email=form_data.get('confirm_email'),
                    vehicle_number=form_data.get('vehicle_number'),
                    phone=form_data.get('phone'),
                    gender=form_data.get('gender'),
                    postcode=form_data.get('postcode'),
                    communication_mode=form_data.get('communication_mode'),
                    age=form_data.get('age'),
                    city_id=form_data.get('city'),
                    car_park_id=form_data.get('car_park'),
                    address=form_data.get('address', ''),
                    pin_code=form_data.get('postcode', '')
                )
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
    return render_template('register.html', cities=cities, car_parks=car_parks, selected_city_id=selected_city_id, form_data=form_data)

# User Dashboard Route
@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('index'))
    return render_template('user_dashboard.html')

# Admin Dashboard Route (Placeholder)
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

# --- User Dashboard Actions ---
@app.route('/release_spot', methods=['GET', 'POST'])
def release_spot():
    if 'user_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import ReserveParkingSpot, ParkingSpot, ParkingLot, db
    user_id = session['user_id']
    # Find active booking (no leaving_timestamp)
    active_booking = ReserveParkingSpot.query.filter_by(user_id=user_id, leaving_timestamp=None).first()
    spot = None
    lot = None
    cost = None
    if active_booking:
        spot = ParkingSpot.query.get(active_booking.spot_id)
        lot = ParkingLot.query.get(spot.lot_id) if spot else None
        if not spot:
            flash('Error: Parking spot not found!', 'danger')
            return redirect(url_for('user_dashboard'))
        if request.method == 'POST':
            # Release the spot
            active_booking.leaving_timestamp = datetime.now()
            # Calculate cost (duration * price per hour)
            duration_hours = (active_booking.leaving_timestamp - active_booking.parking_timestamp).total_seconds() / 3600
            price_per_hour = lot.price if lot else 0
            active_booking.total_cost = round(duration_hours * price_per_hour, 2)
            # Mark spot as available
            spot.status = 'A'
            spot.vehicle_number = None
            db.session.commit()
            
            # Show receipt page
            receipt_data = {
                'booking_id': active_booking.id,
                'spot_id': spot.id,
                'lot_name': lot.prime_location_name if lot else 'Unknown Location',
                'vehicle_number': active_booking.user.vehicle_number or spot.vehicle_number or 'N/A',
                'start_time': active_booking.parking_timestamp,
                'end_time': active_booking.leaving_timestamp,
                'duration_hours': round(duration_hours, 2),
                'price_per_hour': price_per_hour,
                'total_cost': active_booking.total_cost
            }
            return render_template('payment_receipt.html', receipt=receipt_data)
        # For GET, show estimated cost so far
        duration_hours = (datetime.now() - active_booking.parking_timestamp).total_seconds() / 3600
        price_per_hour = lot.price if lot else 0
        cost = round(duration_hours * price_per_hour, 2)
    return render_template('release_spot.html', active_booking=active_booking, spot=spot, lot=lot, cost=cost)

@app.route('/book_spot', methods=['GET', 'POST'])
def book_spot():
    if 'user_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import ParkingLot, ParkingSpot, City, BookingRequest, db
    import json
    from datetime import datetime
    cities = City.query.all()
    selected_city_id = request.args.get('city_id')
    if request.method == 'POST':
        city_id = request.form.get('city_id')
        lot_id = request.form.get('car_park')
        vehicle_number = request.form.get('vehicle_number')
        parking_time = request.form.get('parking_time')
        duration = request.form.get('duration')
        if not (city_id and lot_id and vehicle_number and parking_time and duration):
            flash('All fields are required.', 'danger')
            return redirect(url_for('book_spot', city_id=city_id))
        booking_time = datetime.strptime(parking_time, '%Y-%m-%dT%H:%M')
        booking = BookingRequest(
            user_id = session['user_id'],
            lot_id = lot_id,
            vehicle_number = vehicle_number,
            parking_time = booking_time,
            duration = int(duration),
            status = 'pending'
        )
        db.session.add(booking)
        db.session.commit()
        flash('Your booking request has been sent and is pending admin approval.', 'info')
        return redirect(url_for('user_dashboard'))
    if selected_city_id:
        car_parks = ParkingLot.query.filter_by(city_id=selected_city_id).all()
    else:
        car_parks = []
    all_spots = {}
    for lot in car_parks:
        spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').all()
        all_spots[lot.id] = [{'id': s.id} for s in spots]
    all_spots_json = json.dumps(all_spots)
    return render_template('book_spot.html', cities=cities, car_parks=car_parks, all_spots_json=all_spots_json, selected_city_id=selected_city_id)

@app.route('/summary')
def summary():
    if 'user_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import ReserveParkingSpot, ParkingLot, ParkingSpot, db
    user_id = session['user_id']
    
    # All bookings for this user
    bookings = ReserveParkingSpot.query.filter_by(user_id=user_id).order_by(ReserveParkingSpot.parking_timestamp.desc()).all()
    
    # Summary stats
    total_bookings = len(bookings)
    total_hours = 0
    total_spent = 0
    completed_sessions = 0
    active_sessions = 0
    lot_counts = {}
    
    for booking in bookings:
        # Get parking spot and lot info
        spot = ParkingSpot.query.get(booking.spot_id)
        lot = ParkingLot.query.get(spot.lot_id) if spot else None
        
        if booking.parking_timestamp:
            if booking.leaving_timestamp:
                # Completed session
                completed_sessions += 1
                hours = (booking.leaving_timestamp - booking.parking_timestamp).total_seconds() / 3600
                total_hours += hours
                if booking.total_cost:
                    total_spent += booking.total_cost
            else:
                # Active session - calculate hours up to now
                active_sessions += 1
                hours = (datetime.utcnow() - booking.parking_timestamp).total_seconds() / 3600
                total_hours += hours
                # Calculate estimated cost for active session
                if spot and lot:
                    total_spent += round(hours * lot.price, 2)
            
        # Count by location
        if lot:
            lot_counts[lot.prime_location_name] = lot_counts.get(lot.prime_location_name, 0) + 1
    
    # Enhanced booking data with lot information
    enhanced_bookings = []
    for booking in bookings:
        spot = ParkingSpot.query.get(booking.spot_id)
        lot = ParkingLot.query.get(spot.lot_id) if spot else None
        enhanced_bookings.append({
            'booking': booking,
            'spot': spot,
            'lot': lot
        })
    
    return render_template('summary.html', 
                         bookings=enhanced_bookings, 
                         total_bookings=total_bookings, 
                         total_hours=round(total_hours, 2), 
                         total_spent=round(total_spent, 2),
                         completed_sessions=completed_sessions,
                         active_sessions=active_sessions,
                         lot_counts=lot_counts)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import User, db
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        user.full_name = request.form.get('full_name')
        user.email = request.form.get('email')
        user.confirm_email = request.form.get('confirm_email')
        user.vehicle_number = request.form.get('vehicle_number')
        user.phone = request.form.get('phone')
        user.gender = request.form.get('gender')
        user.postcode = request.form.get('postcode')
        user.communication_mode = request.form.get('communication_mode')
        user.age = request.form.get('age')
        user.address = request.form.get('address')
        user.pin_code = request.form.get('pin_code')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', user=user)

# --- Admin Dashboard Actions ---
@app.route('/manage_users')
def manage_users():
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    users = User.query.all()
    return render_template('manage_users.html', users=users)

@app.route('/parking_spots')
def parking_spots():
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import ParkingSpot, ParkingLot, City
    
    # Get city filter from query parameter
    selected_city_id = request.args.get('city_id')
    cities = City.query.all()
    
    if selected_city_id:
        # Filter lots by selected city
        lots_query = ParkingLot.query.filter_by(city_id=selected_city_id)
        lots = {lot.id: lot for lot in lots_query.all()}
        # Filter spots to only those in the selected city's lots
        lot_ids = list(lots.keys())
        spots = ParkingSpot.query.filter(ParkingSpot.lot_id.in_(lot_ids)).all() if lot_ids else []
    else:
        # Show all lots and spots
        lots = {lot.id: lot for lot in ParkingLot.query.all()}
        spots = ParkingSpot.query.all()
    
    return render_template('parking_spots.html', spots=spots, lots=lots, cities=cities, selected_city_id=selected_city_id)

@app.route('/system_summary')
def system_summary():
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import ReserveParkingSpot, User, ParkingSpot, ParkingLot, City
    
    now = datetime.now()
    last_24h = now - timedelta(hours=24)
    last_7d = now - timedelta(days=7)
    last_30d = now - timedelta(days=30)
    
    # Get all parking spots with their lot information
    spots_with_lots = db.session.query(ParkingSpot, ParkingLot).join(
        ParkingLot, ParkingSpot.lot_id == ParkingLot.id
    ).all()
    
    # Create a dictionary of spot_id to parking lot price
    spot_prices = {spot.id: lot.price for spot, lot in spots_with_lots}
    
    # Get currently parked cars - join with ParkingSpot and ParkingLot
    current_parked = db.session.query(
        ReserveParkingSpot,
        ParkingSpot,
        ParkingLot,
        User
    ).join(
        ParkingSpot, ReserveParkingSpot.spot_id == ParkingSpot.id
    ).join(
        ParkingLot, ParkingSpot.lot_id == ParkingLot.id
    ).join(
        User, ReserveParkingSpot.user_id == User.id
    ).filter(
        ReserveParkingSpot.leaving_timestamp.is_(None)
    ).all()
    
    # Calculate estimated revenue for currently parked cars
    estimated_current_revenue = 0
    for parking, spot, lot, user in current_parked:
        hours = (now - parking.parking_timestamp).total_seconds() / 3600
        estimated_current_revenue += hours * lot.price
        # Ensure the spot is marked as occupied
        if spot.status != 'O':
            spot.status = 'O'
            db.session.commit()
    
    # Cars that left in different time periods
    left_24h = ReserveParkingSpot.query.filter(
        ReserveParkingSpot.leaving_timestamp != None, 
        ReserveParkingSpot.leaving_timestamp >= last_24h
    ).all()
    
    left_7d = ReserveParkingSpot.query.filter(
        ReserveParkingSpot.leaving_timestamp != None, 
        ReserveParkingSpot.leaving_timestamp >= last_7d
    ).all()
    
    # Revenue calculations
    revenue_24h = sum(rps.total_cost or 0 for rps in left_24h)
    revenue_7d = sum(rps.total_cost or 0 for rps in left_7d)
    
    # Add estimated current revenue to totals
    total_revenue_24h = revenue_24h + estimated_current_revenue
    total_revenue_7d = revenue_7d + estimated_current_revenue
    
    # Total system stats
    total_users = User.query.count()
    total_spots = ParkingSpot.query.count()
    total_lots = ParkingLot.query.count()
    total_cities = City.query.count()
    available_spots = ParkingSpot.query.filter_by(status='A').count()
    occupied_spots = ParkingSpot.query.filter_by(status='O').count()
    
    # Occupancy rate
    occupancy_rate = round((occupied_spots / total_spots * 100) if total_spots > 0 else 0, 1)
    
    # Popular locations (most used parking lots)
    from sqlalchemy import func
    popular_lots = db.session.query(
        ParkingLot.prime_location_name,
        func.count(ReserveParkingSpot.id).label('booking_count')
    ).join(ParkingSpot, ParkingLot.id == ParkingSpot.lot_id)\
     .join(ReserveParkingSpot, ParkingSpot.id == ReserveParkingSpot.spot_id)\
     .group_by(ParkingLot.id)\
     .order_by(func.count(ReserveParkingSpot.id).desc())\
     .limit(5).all()
    
    return render_template('system_summary.html', 
                         current_parked=current_parked, 
                         left_24h=left_24h,
                         left_7d=left_7d,
                         revenue_24h=round(revenue_24h, 2),
                         revenue_7d=round(revenue_7d, 2),
                         estimated_current_revenue=round(estimated_current_revenue, 2),
                         total_revenue_24h=round(total_revenue_24h, 2),
                         total_revenue_7d=round(total_revenue_7d, 2),
                         spot_prices=spot_prices,
                         now=now,
                         total_users=total_users,
                         total_spots=total_spots,
                         total_lots=total_lots,
                         total_cities=total_cities,
                         available_spots=available_spots,
                         occupied_spots=occupied_spots,
                         occupancy_rate=occupancy_rate,
                         popular_lots=popular_lots)

@app.route('/manage_locations', methods=['GET', 'POST'])
def manage_locations():
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import City, ParkingLot, ParkingSpot, db
    message = None
    # Handle add city
    if request.method == 'POST' and 'add_city' in request.form:
        city_name = request.form['city_name']
        new_city = City(name=city_name)
        db.session.add(new_city)
        db.session.commit()
        message = f"Added city: {city_name}"
    # Handle add car park
    if request.method == 'POST' and 'add_parking' in request.form:
        city_id = request.form['city_id']
        parking_name = request.form['parking_name']
        price = request.form.get('price', 0)
        address = request.form.get('address', '')
        pin_code = request.form.get('pin_code', '')
        max_spots = int(request.form.get('max_spots', 10))
        new_lot = ParkingLot(city_id=city_id, prime_location_name=parking_name, price=price, address=address, pin_code=pin_code, maximum_number_of_spots=max_spots)
        db.session.add(new_lot)
        db.session.commit()
        for _ in range(max_spots):
            spot = ParkingSpot(lot_id=new_lot.id, status='A')
            db.session.add(spot)
        db.session.commit()
        message = f"Added car park: {parking_name} with {max_spots} spots"
    cities = City.query.all()
    car_parks = ParkingLot.query.all()
    return render_template('manage_locations.html', car_parks=car_parks, cities=cities, message=message)

@app.route('/delete_parking_lot/<int:lot_id>', methods=['POST'])
def delete_parking_lot(lot_id):
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import ParkingLot, ParkingSpot, db
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    if any(spot.status != 'A' for spot in spots):
        flash('Cannot delete parking lot: Not all spots are empty!', 'danger')
        return redirect(url_for('manage_locations'))
    # Delete all spots first (if using ON DELETE CASCADE, this is not needed)
    for spot in spots:
        db.session.delete(spot)
    db.session.delete(lot)
    db.session.commit()
    flash('Parking lot deleted successfully.', 'success')
    return redirect(url_for('manage_locations'))

@app.route('/update_parking_spot/<int:spot_id>', methods=['POST'])
def update_parking_spot(spot_id):
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import ParkingSpot, db
    spot = ParkingSpot.query.get_or_404(spot_id)
    new_status = request.form.get('status')
    new_vehicle = request.form.get('vehicle_number')
    spot.status = new_status
    spot.vehicle_number = new_vehicle if new_status == 'O' else None
    db.session.commit()
    flash(f'Spot {spot.id} updated successfully.', 'success')
    return redirect(url_for('parking_spots'))

# --- City Delete ---
@app.route('/delete_city/<int:city_id>', methods=['POST'])
def delete_city(city_id):
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import City, ParkingLot, db
    city = City.query.get_or_404(city_id)
    if city.parking_lots:
        flash('Cannot delete city: Remove all car parks first.', 'danger')
        return redirect(url_for('manage_locations'))
    db.session.delete(city)
    db.session.commit()
    flash('City deleted successfully.', 'success')
    return redirect(url_for('manage_locations'))

# --- Parking Spot Delete ---
@app.route('/delete_parking_spot/<int:spot_id>', methods=['POST'])
def delete_parking_spot(spot_id):
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import ParkingSpot, db
    spot = ParkingSpot.query.get_or_404(spot_id)
    if spot.status != 'A':
        flash('Cannot delete spot: It is not available.', 'danger')
        return redirect(url_for('parking_spots'))
    db.session.delete(spot)
    db.session.commit()
    flash('Parking spot deleted successfully.', 'success')
    return redirect(url_for('parking_spots'))

# --- City Edit ---
@app.route('/edit_city/<int:city_id>', methods=['GET', 'POST'])
def edit_city(city_id):
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import City, db
    city = City.query.get_or_404(city_id)
    if request.method == 'POST':
        new_name = request.form.get('name')
        if new_name:
            city.name = new_name
            db.session.commit()
            flash('City updated successfully.', 'success')
            return redirect(url_for('manage_locations'))
        else:
            flash('City name cannot be empty.', 'danger')
    return render_template('edit_city.html', city=city)

# --- Parking Lot Edit ---
@app.route('/edit_parking_lot/<int:lot_id>', methods=['GET', 'POST'])
def edit_parking_lot(lot_id):
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import ParkingLot, db
    lot = ParkingLot.query.get_or_404(lot_id)
    if request.method == 'POST':
        lot.prime_location_name = request.form.get('prime_location_name')
        lot.price = request.form.get('price')
        lot.address = request.form.get('address')
        lot.pin_code = request.form.get('pin_code')
        db.session.commit()
        flash('Parking lot updated successfully.', 'success')
        return redirect(url_for('manage_locations'))
    return render_template('edit_parking_lot.html', lot=lot)

# --- Parking Spot Edit ---
@app.route('/edit_parking_spot/<int:spot_id>', methods=['GET', 'POST'])
def edit_parking_spot(spot_id):
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import ParkingSpot, db
    spot = ParkingSpot.query.get_or_404(spot_id)
    if request.method == 'POST':
        spot.status = request.form.get('status')
        spot.vehicle_number = request.form.get('vehicle_number')
        db.session.commit()
        flash('Parking spot updated successfully.', 'success')
        return redirect(url_for('parking_spots'))
    return render_template('edit_parking_spot.html', spot=spot)

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('admin_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

# --- Additional Pages ---
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in to view your profile.', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('profile.html', user=user)

# --- Booking and Parking Lot Routes ---
@app.route('/booking_confirmation/<int:booking_id>')
def booking_confirmation(booking_id):
    if 'user_id' not in session:
        flash('Please log in to view booking confirmation.', 'warning')
        return redirect(url_for('login'))
    
    # Get booking details (you'll need to implement Booking model)
    # For now, using placeholder data
    booking_data = {
        'id': booking_id,
        'spot_number': 'A-15',
        'parking_lot': 'Central Mall Parking',
        'start_time': datetime.now(),
        'duration': '2 hours',
        'cost': 50.0
    }
    
    return render_template('booking_confirmation.html', booking=booking_data)

@app.route('/parking_lot_details/<int:lot_id>')
def parking_lot_details(lot_id):
    from models import ParkingLot, ParkingSpot
    
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(parking_lot_id=lot_id).all()
    
    # Calculate availability statistics
    total_spots = len(spots)
    available_spots = len([spot for spot in spots if spot.is_available])
    occupied_spots = total_spots - available_spots
    
    stats = {
        'total': total_spots,
        'available': available_spots,
        'occupied': occupied_spots,
        'occupancy_rate': round((occupied_spots / total_spots * 100) if total_spots > 0 else 0, 1)
    }
    
    return render_template('parking_lot_details.html', lot=lot, spots=spots, stats=stats)

# --- Additional Utility Routes ---
@app.route('/search_parking')
def search_parking():
    from models import City, ParkingLot
    
    cities = City.query.all()
    lots = ParkingLot.query.all()
    
    # Filter by city if provided
    city_id = request.args.get('city_id')
    if city_id:
        lots = ParkingLot.query.filter_by(city_id=city_id).all()
    
    return render_template('search_parking.html', cities=cities, lots=lots)

@app.route('/api/parking_availability/<int:lot_id>')
def parking_availability_api(lot_id):
    from models import ParkingSpot
    from flask import jsonify
    
    spots = ParkingSpot.query.filter_by(parking_lot_id=lot_id).all()
    available_count = len([spot for spot in spots if spot.is_available])
    total_count = len(spots)
    
    return jsonify({
        'lot_id': lot_id,
        'available': available_count,
        'total': total_count,
        'occupancy_rate': round(((total_count - available_count) / total_count * 100) if total_count > 0 else 0, 1)
    })

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/pricing')
def pricing():
    # Sample pricing data
    pricing_data = {
        'hourly_rates': {
            'standard': 25,
            'premium': 40,
            'vip': 60
        },
        'daily_rates': {
            'standard': 200,
            'premium': 300,
            'vip': 450
        }
    }
    return render_template('pricing.html', pricing=pricing_data)

@app.route('/manage_bookings', methods=['GET', 'POST'])
def manage_bookings():
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import BookingRequest, ParkingLot, ParkingSpot, User, db
    if request.method == 'POST':
        booking_id = request.form.get('booking_id')
        action = request.form.get('action')
        booking = BookingRequest.query.get_or_404(booking_id)
        if action == 'approve':
            spot_id = request.form.get('spot_id')
            spot = ParkingSpot.query.get_or_404(spot_id)
            if spot.status != 'A':
                flash('Selected spot is not available.', 'danger')
            else:
                from models import ReserveParkingSpot
                from datetime import datetime
                
                # Create reservation record
                reservation = ReserveParkingSpot(
                    spot_id=spot.id,
                    user_id=booking.user_id,
                    parking_timestamp=datetime.now(),
                    parking_cost_per_unit=spot.parking_lot.price
                )
                
                # Update spot status
                spot.status = 'O'
                spot.vehicle_number = booking.vehicle_number
                
                # Update booking status
                booking.status = 'approved'
                booking.spot_id = spot.id
                
                # Add and commit changes
                db.session.add(reservation)
                db.session.commit()
                
                flash(f'Booking approved and spot {spot.id} assigned. Reservation created.', 'success')
        elif action == 'reject':
            booking.status = 'rejected'
            db.session.commit()
            flash('Booking request rejected.', 'info')
        return redirect(url_for('manage_bookings'))
    # GET: show all pending requests
    pending_bookings = BookingRequest.query.filter_by(status='pending').order_by(BookingRequest.created_at.asc()).all()
    lots = {lot.id: lot for lot in ParkingLot.query.all()}
    users = {user.id: user for user in User.query.all()}
    spots_by_lot = {}
    for lot in lots.values():
        spots_by_lot[lot.id] = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').all()
    return render_template('manage_bookings.html', bookings=pending_bookings, lots=lots, users=users, spots_by_lot=spots_by_lot)

@app.route('/my_bookings')
def my_bookings():
    if 'user_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import BookingRequest, ParkingLot, ParkingSpot
    bookings = BookingRequest.query.filter_by(user_id=session['user_id']).order_by(BookingRequest.created_at.desc()).all()
    lots = {lot.id: lot for lot in ParkingLot.query.all()}
    spots = {spot.id: spot for spot in ParkingSpot.query.all()}
    return render_template('my_bookings.html', bookings=bookings, lots=lots, spots=spots)

@app.route('/occupy_spot/<int:booking_id>', methods=['GET', 'POST'])
def occupy_spot(booking_id):
    if 'user_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    from models import BookingRequest, ParkingSpot, ReserveParkingSpot, db
    from datetime import datetime
    booking = BookingRequest.query.get_or_404(booking_id)
    if booking.user_id != session['user_id']:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('my_bookings'))
    if booking.status != 'approved' or not booking.spot_id:
        flash('Booking is not approved or spot not assigned.', 'danger')
        return redirect(url_for('my_bookings'))
    spot = ParkingSpot.query.get(booking.spot_id)
    already_occupied = ReserveParkingSpot.query.filter_by(user_id=booking.user_id, spot_id=spot.id, leaving_timestamp=None).first()
    if request.method == 'POST' and not already_occupied:
        reserve = ReserveParkingSpot(
            spot_id=spot.id,
            user_id=booking.user_id,
            parking_timestamp=datetime.now(),
            parking_cost_per_unit=spot.parking_lot.price
        )
        spot.status = 'O'
        spot.vehicle_number = booking.vehicle_number
        db.session.add(reserve)
        db.session.commit()
        flash('Spot marked as occupied. Enjoy your parking!', 'success')
        return redirect(url_for('my_bookings'))
    return render_template('occupy_spot.html', booking=booking, spot=spot, already_occupied=already_occupied)


if __name__ == '__main__':
    app.run(debug=True)