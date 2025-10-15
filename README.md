# Hotel Management System

A comprehensive Django-based hotel management system with reporting, analytics dashboard, and real-time room management capabilities.

## Features

- **Real-time Room Management**: Track and update room statuses (Available, Occupied, Booked, Maintenance) with interactive controls
- **Interactive Analytics Dashboard**: Visualize key metrics with Chart.js including revenue trends, occupancy rates, room distribution, and staff performance
- **Comprehensive Reporting**: Detailed reports on hotel operations, revenue, occupancy, and staff performance
- **Filterable Data Views**: Easily filter information by hotel, room type, or status
- **Responsive Web Interface**: Modern UI that works on desktop and mobile devices
- **Database Integration**: MySQL backend with comprehensive hotel management schema
- **Dynamic Data Visualization**: Interactive charts and graphs for data-driven decision making

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
   - Create a MySQL database named `hotelmanagementsystemdb`
   - Update credentials in `hotel_management/settings.py` if needed (default user: root, password: Groupm@2025)
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Populate the database with sample data (optional but recommended):
   ```bash
   python manage.py shell < reports/sql/populating_tables.sql
   ```
7. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure
```
hotel_management/
├── hotel_management/          # Main Django project
│   ├── settings.py           # Configuration
│   ├── urls.py              # Main URL routing
│   ├── views.py             # Main project views
│   └── wsgi.py              # WSGI entry point
├── reports/                  # Reports app
│   ├── sql/                 # SQL query files for reports
│   │   └── README.md        # SQL files documentation
│   ├── templates/           # HTML templates
│   ├── views.py             # View functions
│   └── urls.py              # App URL routing
├── static/                   # Static files
│   ├── css/
│   └── js/
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
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

# Populate database with sample data (optional)
python manage.py shell < reports/sql/populating_tables.sql

# Run development server
python manage.py runserver

# Access the application at http://127.0.0.1:8000/
```

### Linux/Mac
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Populate database with sample data (optional)
python manage.py shell < reports/sql/populating_tables.sql

# Run development server
python manage.py runserver

# Access the application at http://127.0.0.1:8000/
```

## Application Modules

### 1. Room Management System
- Real-time room status tracking and updates
- Filter rooms by hotel, type, or status
- Interactive room status management (Available, Occupied, Booked, Maintenance)
- Room availability reports
- Room utilization analytics
- Dynamic room status updates with confirmation prompts

### 2. Traditional Reports
- General Report - Overview of hotels, staff, and guests
- Room Occupancy Report - Room status and occupancy information
- Staff Performance Report - Employee performance metrics
- Monthly Revenue Collection - Revenue tracking
- Outstanding Payments - Guest payment status
- Top Paying Guests - High-value customers
- Hotels and Staff - Detailed hotel and staff information

### 3. Analytics Dashboard
Interactive visualizations using Chart.js:
- Monthly Revenue Trend (line chart)
- Hotel Occupancy Rates (bar chart)
- Room Type Distribution (pie chart)
- Staff Performance (horizontal bar chart)

### 4. Navigation
- Home page with quick access to all modules
- Reports index with direct links to all reports
- Room management interface with tabbed views
- Analytics dashboard with interactive charts

## Database Schema

The system uses a MySQL database with the following tables:
- **hotel** - Hotel information (ID, name, location, contact)
- **staff** - Staff information (ID, hotel ID, name, contact, role)
- **guest** - Guest information (ID, name, contact, gender)
- **room** - Room information (ID, hotel ID, type, status)
- **booking** - Booking information (ID, guest ID, room ID, dates, status)
- **payment** - Payment information (ID, booking ID, date, amount)
- **invoice** - Invoice information (ID, booking ID, guest ID, amount, status)
- **services** - Service information (ID, name, price, booking ID)

## SQL Files Documentation

Each SQL file in the `reports/sql/` directory serves a specific purpose in the application. For detailed information about what each SQL file implements, see [reports/sql/README.md](reports/sql/README.md).

## Accessing the Application

After starting the development server, access the application at:
- **Home Page**: http://127.0.0.1:8000/
- **Reports**: http://127.0.0.1:8000/reports/
- **Room Management**: http://127.0.0.1:8000/reports/room-management/
- **Analytics Dashboard**: http://127.0.0.1:8000/reports/dashboard/

## Recent Updates

### Codebase Improvements
- Optimized SQL queries for better performance
- Removed unused test and debug files to reduce clutter
- Improved error handling in report generation
- Enhanced data visualization in dashboard charts
- Streamlined template structure for consistent styling

### Report Enhancements
- Fixed data fetching issues in multiple reports
- Improved table layouts with horizontal scrolling for wide data sets
- Updated column naming consistency across reports
- Enhanced visual styling to match modern UI standards
- Added responsive design for better mobile experience

### Database Optimization
- Cleaned up unused SQL files while preserving essential schema and data population scripts
- Verified all report queries are functioning correctly
- Improved query efficiency for dashboard data generation

## Troubleshooting

- Ensure MySQL is running and accessible
- Verify database credentials in `hotel_management/settings.py`
- Check that all dependencies are installed (`pip install -r requirements.txt`)
- For database connection issues, try recreating the database and running migrations
- If charts are not displaying data, check the browser console for JavaScript errors
- For report data issues, verify the database has been populated with sample data