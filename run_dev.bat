@echo off
echo Starting Hotel Management System Development Server...
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
) else (
    echo No virtual environment found. Make sure dependencies are installed.
)

REM Install requirements if not already installed
echo Checking dependencies...
pip install -r requirements.txt >nul 2>&1

REM Run Django development server
echo Starting Django development server...
python manage.py runserver

pause