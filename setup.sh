#!/bin/bash

echo "========================================"
echo "Hospital Management System Setup"
echo "========================================"
echo

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo "Step 3: Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "Step 4: Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Please edit .env file with your database credentials"
    echo "Press Enter after updating .env file..."
    read
fi

echo "Step 5: Creating database migrations..."
python manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "Error: Failed to create migrations"
    exit 1
fi

echo "Step 6: Applying migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Error: Failed to apply migrations"
    exit 1
fi

echo "Step 7: Setting up initial hospital data..."
python manage.py setup_hospital_data

echo "Step 8: Creating superuser..."
echo "Please create an admin user:"
python manage.py createsuperuser

echo
echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo
echo "To start the development server, run:"
echo "python manage.py runserver"
echo
echo "Then visit: http://127.0.0.1:8000"
echo "Admin panel: http://127.0.0.1:8000/admin"
echo