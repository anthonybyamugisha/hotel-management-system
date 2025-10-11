# Hotel Management System Setup Script

Write-Host "Hotel Management System Setup Script" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
python -m venv venv
Write-Host "Virtual environment created." -ForegroundColor Yellow

# Activate virtual environment
.\venv\Scripts\Activate.ps1
Write-Host "Virtual environment activated." -ForegroundColor Yellow

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Cyan
python manage.py migrate

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "To run the development server, execute: .\run_dev.ps1" -ForegroundColor Yellow
Write-Host "Or activate the virtual environment and run: python manage.py runserver" -ForegroundColor Yellow