# Hotel Management System Development Server Script

Write-Host "Starting Hotel Management System Development Server..." -ForegroundColor Green
Write-Host ""

# Activate virtual environment if it exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
    Write-Host "Virtual environment activated." -ForegroundColor Yellow
} else {
    Write-Host "No virtual environment found. Make sure dependencies are installed." -ForegroundColor Yellow
}

# Install requirements if not already installed
Write-Host "Checking dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt | Out-Null

# Run Django development server
Write-Host "Starting Django development server..." -ForegroundColor Green
python manage.py runserver