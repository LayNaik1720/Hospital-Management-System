# Hospital Management System (HMS)

A comprehensive, secure, and scalable Hospital Management System built with Django and SQL Server.

## 🏥 Features

### 🔐 Role-Based Access Control
- **Admin**: Full system access, user management, reports
- **Doctor**: Patient records, appointments, prescriptions, lab requests
- **Nurse**: Patient care, vital signs, medical records
- **Receptionist**: Patient registration, appointment scheduling
- **Pharmacist**: Medicine inventory, sales, prescription dispensing
- **Lab Technician**: Test requests, result entry, report generation
- **Accountant**: Billing, payments, financial reports
- **Patient**: Optional portal access

### 👤 Patient Management
- Unique Patient ID generation
- Comprehensive patient profiles
- Medical history and allergies tracking
- Insurance policy management
- Search and filter capabilities

### 👨‍⚕️ Doctor & Staff Management
- Doctor profiles with specializations
- Department management
- Duty schedules and availability
- Staff credentials and role mapping

### 📅 Appointment Scheduling
- Doctor-wise time slot booking
- Conflict prevention system
- Appointment status tracking
- Rescheduling capabilities

### 📋 Electronic Medical Records (EMR)
- Secure patient visit records
- Diagnosis and treatment plans
- File upload for reports/images
- Role-based access control
- Prescription management

### 💊 Pharmacy Management
- Medicine inventory with batch tracking
- Expiry date monitoring
- Auto stock alerts
- Prescription-based dispensing
- Sales reporting

### 🧾 Billing & Insurance
- OPD/IPD billing system
- Automatic bill generation
- Insurance claim processing
- Multiple payment methods
- Invoice generation (PDF)

### 🧪 Laboratory Management
- Test catalog management
- Doctor test requests
- Result entry by technicians
- Report generation and access

### 📊 Analytics & Reports
- Role-based dashboards
- Financial reports
- Patient statistics
- System usage analytics
- Export capabilities (Excel/PDF)

## 🛠️ Technical Stack

- **Backend**: Python 3.8+, Django 4.2
- **Database**: SQL Server
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Django Auth with custom user model
- **Security**: CSRF protection, SQL injection prevention, secure file uploads

## 📋 Prerequisites

1. Python 3.8 or higher
2. SQL Server (Express/Standard/Enterprise)
3. ODBC Driver 17 for SQL Server

## 🚀 Installation & Setup

### 1. Clone and Setup Environment

```bash
# Navigate to project directory
cd "Hospital Management System"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration

1. Install SQL Server and create a database named `hospital_management`
2. Copy `.env.example` to `.env` and update database credentials:

```env
DB_NAME=hospital_management
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=1433
```

### 3. Database Migration

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Load Initial Data (Optional)

```bash
# Create sample departments
python manage.py shell
```

```python
from doctors.models import Department
from billing.models import BillingCategory, ServiceCharge

# Create departments
departments = [
    'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 
    'Emergency', 'General Medicine', 'Surgery', 'Radiology'
]

for dept_name in departments:
    Department.objects.get_or_create(name=dept_name)

# Create billing categories
categories = ['Consultation', 'Procedures', 'Laboratory', 'Pharmacy', 'Room Charges']
for cat_name in categories:
    BillingCategory.objects.get_or_create(name=cat_name)
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the system.

## 👥 Default User Roles

After creating a superuser, you can:

1. Access admin panel at `/admin/`
2. Create staff users with different roles
3. Assign appropriate permissions

## 🔒 Security Features

- **Authentication**: Secure login/logout with session management
- **Authorization**: Role-based access control (RBAC)
- **Data Protection**: Input validation and SQL injection prevention
- **File Security**: Secure file uploads with type validation
- **Audit Trail**: System activity logging
- **Password Security**: Django's built-in password hashing

## 📱 API Endpoints

The system includes REST API endpoints for:
- Patient management
- Appointment scheduling
- Medical records
- Pharmacy operations
- Laboratory tests

## 🔧 Configuration

### Production Settings

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Configure proper `ALLOWED_HOSTS`
3. Use strong `SECRET_KEY`
4. Enable HTTPS settings
5. Configure proper database backup

### File Upload Settings

- Maximum file size: 5MB
- Allowed formats: PDF, JPG, JPEG, PNG, DOC, DOCX
- Secure file storage with UUID naming

## 📊 Reporting Features

- **Financial Reports**: Revenue, billing, payment tracking
- **Patient Analytics**: Demographics, visit patterns
- **Operational Reports**: Appointment statistics, staff performance
- **Export Options**: PDF, Excel formats

## 🔍 Search & Filter

- Advanced patient search
- Appointment filtering by date/status/doctor
- Medicine inventory search
- Bill and payment tracking

## 🚨 Alerts & Notifications

- Low stock medicine alerts
- Appointment reminders
- Overdue bill notifications
- System activity alerts

## 🛡️ Data Privacy & Compliance

- HIPAA-style data privacy principles
- Secure data handling
- Access logging and audit trails
- Role-based data access

## 📞 Support & Maintenance

### Regular Maintenance Tasks

1. Database backup and optimization
2. Log file management
3. Security updates
4. Performance monitoring

### Troubleshooting

Common issues and solutions:

1. **Database Connection**: Check SQL Server service and credentials
2. **Migration Errors**: Ensure proper database permissions
3. **File Upload Issues**: Check media directory permissions
4. **Performance**: Monitor database queries and optimize as needed

## 🔄 Future Enhancements

- Mobile application integration
- Telemedicine features
- Advanced reporting dashboard
- Integration with medical devices
- Multi-language support

## 📄 License

This project is developed for educational and healthcare management purposes.

## 🤝 Contributing

1. Follow Django best practices
2. Maintain security standards
3. Document new features
4. Test thoroughly before deployment

---

**Note**: This system handles sensitive medical data. Ensure proper security measures, regular backups, and compliance with healthcare regulations in your jurisdiction.