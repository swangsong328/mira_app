@echo off
echo ============================================
echo Beauty Salon Booking System - Setup Script
echo ============================================
echo.

echo [1/6] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/6] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/6] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file from .env.example
) else (
    echo .env file already exists, skipping...
)

echo [5/6] Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)

echo [6/6] Seeding demo data...
python manage.py seed_demo
if errorlevel 1 (
    echo ERROR: Failed to seed demo data
    pause
    exit /b 1
)

echo.
echo ============================================
echo Setup completed successfully!
echo ============================================
echo.
echo Admin credentials:
echo   Email: admin@beautysalon.com
echo   Password: admin123
echo.
echo Customer credentials:
echo   Email: customer@example.com
echo   Password: password123
echo.
echo To start the development server, run:
echo   python manage.py runserver
echo.
echo Then visit: http://localhost:8000
echo.
pause

