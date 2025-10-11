@echo off
echo Hotel Management System Setup Script
echo ===================================
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
echo Virtual environment created.

REM Activate virtual environment
call venv\Scripts\activate.bat
echo Virtual environment activated.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo Running database migrations...
python manage.py migrate

echo.
echo Setup complete!
echo To run the development server, execute: run_dev.bat
echo Or activate the virtual environment and run: python manage.py runserver
pause