#!/bin/bash

echo "============================================"
echo "Beauty Salon Booking System - Setup Script"
echo "============================================"
echo ""

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "[1/6] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/6] Activating virtual environment..."
source venv/bin/activate

echo "[3/6] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[4/6] Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from .env.example"
else
    echo ".env file already exists, skipping..."
fi

echo "[5/6] Running database migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to run migrations"
    exit 1
fi

echo "[6/6] Seeding demo data..."
python manage.py seed_demo
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to seed demo data"
    exit 1
fi

echo ""
echo "============================================"
echo "Setup completed successfully!"
echo "============================================"
echo ""
echo "Admin credentials:"
echo "  Email: admin@beautysalon.com"
echo "  Password: admin123"
echo ""
echo "Customer credentials:"
echo "  Email: customer@example.com"
echo "  Password: password123"
echo ""
echo "To start the development server, run:"
echo "  python manage.py runserver"
echo ""
echo "Then visit: http://localhost:8000"
echo ""

