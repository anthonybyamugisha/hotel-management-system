# Hotel Management System

A Django web application for hotel management with reporting and analytics capabilities.

## Features
- Traditional reports (text-based)
- Graphical dashboard with interactive charts
- Real-time data visualization
- Multiple report types:
  - General hotel overview
  - Room occupancy analysis
  - Staff performance metrics
  - Revenue tracking
  - Outstanding payments
  - Top paying guests

## Deployment to Render

### Prerequisites
1. A Render account (https://render.com)
2. A MySQL database (can be provisioned on Render or use an external one)

### Steps to Deploy

1. **Fork this repository** to your GitHub account

2. **Create a new Web Service on Render**
   - Go to your Render Dashboard
   - Click "New" and select "Web Service"
   - Connect your GitHub repository
   - Set the following:
     - Name: hotel-management
     - Runtime: Python 3
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn hotel_management.wsgi:application`
     - Plan: Free (or choose a paid plan for production)

3. **Configure Environment Variables**
   Add the following environment variables in the Render dashboard:
   - `SECRET_KEY`: A random secret key for Django
   - `DEBUG`: False (for production)
   - `ALLOWED_HOSTS`: Your Render URL (e.g., hotel-management.onrender.com)
   - `DATABASE_URL`: Your MySQL database connection string

4. **Set up Database**
   Option A: Use Render's database service
   - Create a new database on Render
   - Update the DATABASE_URL environment variable with the connection string provided by Render

   Option B: Use an external MySQL database
   - Ensure your database is accessible from Render
   - Update the DATABASE_URL environment variable with your database connection string

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy your application
   - The deployment process will:
     - Install dependencies from requirements.txt
     - Run Django migrations
     - Start the Gunicorn server

### Local Development Setup

1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd hotel-management
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env` and update values as needed

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

## Project Structure
- `hotel_management/`: Main Django project settings
- `reports/`: Main application with views, templates, and SQL reports
- `static/`: CSS and JavaScript files
- `templates/`: HTML templates

## Database
The application uses MySQL. Make sure to run the SQL scripts in the `reports/sql/` directory to set up your database schema and initial data.

## Customization
- Add new reports by creating SQL files in `reports/sql/`
- Modify templates in `reports/templates/reports/`
- Update views in `reports/views.py`
- Add new styling in `static/css/styles.css`

## License
This project is licensed under the MIT License.