#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from doctors.models import Department, Doctor

User = get_user_model()

def create_pediatrics_doctor():
    print("Creating Pediatrics doctor...")
    
    # Get Pediatrics department
    pediatrics = Department.objects.get(name='Pediatrics')
    
    # Create doctor user
    user, created = User.objects.get_or_create(
        username='dr_pediatrics',
        defaults={
            'first_name': 'Emily',
            'last_name': 'Davis',
            'email': 'dr.davis@hospital.com',
            'role': 'doctor',
            'is_active_staff': True
        }
    )
    
    if created:
        user.set_password('doctor123')
        user.save()
        print(f"Created doctor user: {user.username}")
    
    # Create doctor profile
    doctor, created = Doctor.objects.get_or_create(
        user=user,
        defaults={
            'employee_id': 'DOC003',
            'department': pediatrics,
            'specialization': 'Pediatric Medicine',
            'qualification': 'MD, FAAP',
            'experience_years': 8,
            'consultation_fee': 180.00
        }
    )
    
    if created:
        print(f"Created doctor profile: {doctor}")
    
    print("Pediatrics doctor created successfully!")
    print(f"Username: dr_pediatrics")
    print(f"Password: doctor123")

if __name__ == '__main__':
    create_pediatrics_doctor()