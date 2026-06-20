#!/usr/bin/env python
import os
import sys
import django
from datetime import date, datetime, timedelta
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from doctors.models import Department, Doctor
from patients.models import Patient
from billing.models import BillingCategory, ServiceCharge

User = get_user_model()

def create_sample_data():
    print("Creating sample data...")
    
    # Create departments
    departments_data = [
        {'name': 'Cardiology', 'description': 'Heart and cardiovascular system'},
        {'name': 'Neurology', 'description': 'Brain and nervous system'},
        {'name': 'Orthopedics', 'description': 'Bones, joints, and muscles'},
        {'name': 'Pediatrics', 'description': 'Children healthcare'},
        {'name': 'Emergency', 'description': 'Emergency medical care'},
        {'name': 'General Medicine', 'description': 'General medical care'},
    ]
    
    for dept_data in departments_data:
        dept, created = Department.objects.get_or_create(
            name=dept_data['name'],
            defaults={'description': dept_data['description']}
        )
        if created:
            print(f"Created department: {dept.name}")
    
    # Create sample doctors
    cardiology = Department.objects.get(name='Cardiology')
    neurology = Department.objects.get(name='Neurology')
    
    doctors_data = [
        {
            'username': 'dr_smith',
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'dr.smith@hospital.com',
            'department': cardiology,
            'specialization': 'Interventional Cardiology',
            'qualification': 'MD, FACC',
            'experience_years': 15,
            'consultation_fee': 200.00,
            'employee_id': 'DOC001'
        },
        {
            'username': 'dr_johnson',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'email': 'dr.johnson@hospital.com',
            'department': neurology,
            'specialization': 'Neurological Surgery',
            'qualification': 'MD, PhD',
            'experience_years': 12,
            'consultation_fee': 250.00,
            'employee_id': 'DOC002'
        }
    ]
    
    for doc_data in doctors_data:
        user, created = User.objects.get_or_create(
            username=doc_data['username'],
            defaults={
                'first_name': doc_data['first_name'],
                'last_name': doc_data['last_name'],
                'email': doc_data['email'],
                'role': 'doctor',
                'is_active_staff': True
            }
        )
        if created:
            user.set_password('doctor123')
            user.save()
            print(f"Created doctor user: {user.username}")
        
        doctor, created = Doctor.objects.get_or_create(
            user=user,
            defaults={
                'employee_id': doc_data['employee_id'],
                'department': doc_data['department'],
                'specialization': doc_data['specialization'],
                'qualification': doc_data['qualification'],
                'experience_years': doc_data['experience_years'],
                'consultation_fee': doc_data['consultation_fee']
            }
        )
        if created:
            print(f"Created doctor profile: {doctor}")
    
    # Create sample patients
    patients_data = [
        {
            'first_name': 'Alice',
            'last_name': 'Williams',
            'date_of_birth': date(1985, 3, 15),
            'gender': 'F',
            'blood_group': 'A+',
            'phone': '(555) 123-4567',
            'email': 'alice.williams@email.com',
            'address': '123 Main St, City, State 12345',
            'emergency_contact_name': 'Bob Williams',
            'emergency_contact_phone': '(555) 987-6543',
            'emergency_contact_relation': 'Husband'
        },
        {
            'first_name': 'Michael',
            'last_name': 'Brown',
            'date_of_birth': date(1978, 7, 22),
            'gender': 'M',
            'blood_group': 'O-',
            'phone': '(555) 234-5678',
            'email': 'michael.brown@email.com',
            'address': '456 Oak Ave, City, State 12345',
            'emergency_contact_name': 'Lisa Brown',
            'emergency_contact_phone': '(555) 876-5432',
            'emergency_contact_relation': 'Wife'
        }
    ]
    
    admin_user = User.objects.get(username='admin')
    
    for patient_data in patients_data:
        patient, created = Patient.objects.get_or_create(
            first_name=patient_data['first_name'],
            last_name=patient_data['last_name'],
            defaults={**patient_data, 'created_by': admin_user}
        )
        if created:
            print(f"Created patient: {patient}")
    
    # Create billing categories and services
    categories_data = [
        {'name': 'Consultation', 'description': 'Doctor consultation fees'},
        {'name': 'Procedures', 'description': 'Medical procedures'},
        {'name': 'Laboratory', 'description': 'Lab tests and diagnostics'},
        {'name': 'Pharmacy', 'description': 'Medicine and drugs'},
        {'name': 'Room Charges', 'description': 'Hospital room charges'}
    ]
    
    for cat_data in categories_data:
        category, created = BillingCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"Created billing category: {category.name}")
    
    # Create sample service charges
    consultation_cat = BillingCategory.objects.get(name='Consultation')
    lab_cat = BillingCategory.objects.get(name='Laboratory')
    
    services_data = [
        {'category': consultation_cat, 'name': 'General Consultation', 'code': 'CONS001', 'amount': 150.00},
        {'category': consultation_cat, 'name': 'Specialist Consultation', 'code': 'CONS002', 'amount': 200.00},
        {'category': lab_cat, 'name': 'Complete Blood Count', 'code': 'LAB001', 'amount': 50.00},
        {'category': lab_cat, 'name': 'X-Ray Chest', 'code': 'LAB002', 'amount': 75.00},
    ]
    
    for service_data in services_data:
        service, created = ServiceCharge.objects.get_or_create(
            code=service_data['code'],
            defaults=service_data
        )
        if created:
            print(f"Created service: {service.name}")
    
    print("Sample data creation completed!")

if __name__ == '__main__':
    create_sample_data()