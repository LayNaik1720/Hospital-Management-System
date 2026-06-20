@echo off
echo ========================================
echo Hospital Management System Setup
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate

echo Step 3: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo Step 4: Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Please edit .env file with your database credentials
    echo Press any key after updating .env file...
    pause
)

echo Step 5: Creating database migrations...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo Error: Failed to create migrations
    pause
    exit /b 1
)

echo Step 6: Applying migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo Error: Failed to apply migrations
    pause
    exit /b 1
)

echo Step 7: Setting up initial hospital data...
python manage.py setup_hospital_data

echo Step 8: Creating superuser...
echo Please create an admin user:
python manage.py createsuperuser

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To start the development server, run:
echo python manage.py runserver
echo.
echo Then visit: http://127.0.0.1:8000
echo Admin panel: http://127.0.0.1:8000/admin
echo.
pause