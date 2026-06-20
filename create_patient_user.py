#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from patients.models import Patient

User = get_user_model()

# Create patient user
user, created = User.objects.get_or_create(
    username='patient1',
    defaults={
        'first_name': 'John',
        'last_name': 'Patient',
        'email': 'patient@email.com',
        'role': 'patient',
        'is_active_staff': True
    }
)

if created:
    user.set_password('patient123')
    user.save()
    print(f"Created patient user: {user.username}")

# Link to existing patient record
try:
    patient = Patient.objects.first()
    if patient and not patient.user:
        patient.user = user
        patient.save()
        print(f"Linked to patient: {patient.full_name}")
except:
    pass

print("Patient login created!")
print("Username: patient1")
print("Password: patient123")