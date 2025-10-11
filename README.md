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

## Deployment to Render

### Automatic Deployment
Render will automatically:
1. Install dependencies from `requirements.txt`
2. Run the build command: `./setup.sh`
3. Start the application with: `gunicorn hotel_management.wsgi:application`

### Manual Deployment Steps
1. Push your code to GitHub
2. Connect your repository to Render
3. Configure the service using `render.yaml`
4. Set environment variables in Render dashboard:
   - `SECRET_KEY` (auto-generated)
   - `DEBUG=False`
   - `ALLOWED_HOSTS` (comma-separated list including your Render domain)

### Troubleshooting Deployment Issues

If your application isn't working after deployment, check:

1. **Render Logs**: Check the build and runtime logs for error messages
2. **Environment Variables**: Ensure all required variables are set
3. **Database Connection**: Verify the database is properly linked
4. **Static Files**: Make sure `collectstatic` runs during build

### Diagnostic URLs
- Test deployment: `/reports/test/`
- Main dashboard: `/reports/dashboard/`
- Reports index: `/reports/reports/`

### Common Issues and Solutions

#### Database Connection Errors
- Ensure your database service is running
- Check that `DATABASE_URL` is correctly set
- Verify database credentials and permissions

#### Static Files Not Loading
- Confirm `collectstatic` runs during build
- Check `STATIC_ROOT` and `STATIC_URL` settings
- Verify WhiteNoise is properly configured

#### Application Not Starting
- Check the start command: `gunicorn hotel_management.wsgi:application`
- Ensure all dependencies are in `requirements.txt`
- Verify the WSGI application path is correct

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
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── Procfile                 # Render start command
├── render.yaml              # Render service configuration
└── setup.sh                 # Build script
```

## Development Commands

### Windows
```bash
# Setup (first time)
setup.bat

# Run development server
run_dev.bat
```

### Linux/Mac
```bash
# Setup (first time)
make setup

# Run development server
make run
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

## Support

For deployment issues, check:
1. Render logs for specific error messages
2. [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for detailed troubleshooting steps
3. Render documentation: https://render.com/docs