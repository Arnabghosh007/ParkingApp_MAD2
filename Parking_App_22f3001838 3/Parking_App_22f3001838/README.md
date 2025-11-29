# Vehicle Parking System

A comprehensive web-based parking management system built with Flask.

## Features

- **User Registration & Login**: Secure user authentication with password hashing
- **Admin Dashboard**: Administrative controls for managing users, parking lots, and system overview
- **Parking Spot Management**: Book and release parking spots in real-time
- **Multi-City Support**: Support for multiple cities and parking locations
- **Cost Calculation**: Automatic calculation of parking fees based on duration
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://127.0.0.1:5000`

## Default Admin Credentials

- **Username**: admin
- **Password**: admin123

## Sample Cities & Parking Lots

The system comes pre-loaded with sample data for major Indian cities:
- Mumbai (3 parking lots)
- Delhi (3 parking lots) 
- Bangalore (3 parking lots)
- Chennai, Kolkata, Hyderabad, Pune, Ahmedabad

## Usage

### For Users:
1. Register with your details and select your preferred city and parking lot
2. Login to access your dashboard
3. Book available parking spots
4. Release spots when leaving
5. View your parking history and costs

### For Admins:
1. Login with admin credentials
2. Manage users and parking locations
3. View system-wide statistics
4. Add/remove parking lots and spots

## Project Structure

```
Vehicle Parking System/
├── app.py              # Main Flask application
├── models.py           # Database models
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
├── static/            # CSS and static files
└── instance/          # Database files
```

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Database**: SQLite
- **Security**: Werkzeug password hashing
- **Architecture**: Pure server-side rendering with form-based interactions
