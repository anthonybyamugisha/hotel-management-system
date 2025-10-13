# Hotel Management System

A Django-based hotel management system with reporting and dashboard capabilities.

## Local Development Setup

1. Install Python 3.8+
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the database (MySQL):
   - Create a MySQL database named `hotelmanagementdb`
   - Update credentials in `hotel_management/settings.py` if needed
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure
```
hotel_management/
├── hotel_management/          # Main Django project
│   ├── settings.py           # Configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI entry point
├── reports/                  # Reports app
│   ├── sql/                 # SQL query files
│   ├── templates/           # HTML templates
│   ├── views.py             # View functions
│   └── urls.py              # App URL routing
├── static/                   # Static files
│   ├── css/
│   ├── js/
│   └── images/
└── manage.py                # Django management script
```

## Development Commands

### Windows
```bash
# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Run development server
python manage.py runserver
```

### Linux/Mac
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Run development server
python manage.py runserver
```

## Reports Available

1. General Report - Overview of hotels, staff, and guests
2. Room Occupancy Report - Room status and occupancy information
3. Staff Performance Report - Employee performance metrics
4. Monthly Revenue Collection - Revenue tracking
5. Outstanding Payments - Guest payment status
6. Top Paying Guests - High-value customers

## Dashboard Charts

1. Monthly Revenue Trend
2. Hotel Occupancy Rates
3. Room Type Distribution
4. Staff Performance