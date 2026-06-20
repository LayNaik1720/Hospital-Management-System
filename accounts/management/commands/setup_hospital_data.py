from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from doctors.models import Department
from billing.models import BillingCategory, ServiceCharge
from laboratory.models import LabTestCategory, LabTest
from pharmacy.models import Medicine

User = get_user_model()

class Command(BaseCommand):
    help = 'Setup initial hospital data'

    def handle(self, *args, **options):
        self.stdout.write('Setting up initial hospital data...')
        
        # Create departments
        departments = [
            'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics',
            'Emergency', 'General Medicine', 'Surgery', 'Radiology',
            'Dermatology', 'Psychiatry', 'Oncology', 'Gynecology'
        ]
        
        for dept_name in departments:
            dept, created = Department.objects.get_or_create(
                name=dept_name,
                defaults={'description': f'{dept_name} Department'}
            )
            if created:
                self.stdout.write(f'Created department: {dept_name}')
        
        # Create billing categories
        billing_categories = [
            ('Consultation', 'Doctor consultation fees'),
            ('Procedures', 'Medical procedures and treatments'),
            ('Laboratory', 'Laboratory tests and diagnostics'),
            ('Pharmacy', 'Medicine and pharmaceutical items'),
            ('Room Charges', 'Hospital room and accommodation'),
            ('Emergency', 'Emergency services'),
            ('Surgery', 'Surgical procedures'),
            ('Imaging', 'X-ray, CT, MRI, Ultrasound')
        ]
        
        for cat_name, description in billing_categories:
            cat, created = BillingCategory.objects.get_or_create(
                name=cat_name,
                defaults={'description': description}
            )
            if created:
                self.stdout.write(f'Created billing category: {cat_name}')
        
        # Create sample service charges
        consultation_cat = BillingCategory.objects.get(name='Consultation')
        lab_cat = BillingCategory.objects.get(name='Laboratory')
        
        services = [
            ('General Consultation', 'consultation', consultation_cat, 50.00),
            ('Specialist Consultation', 'consultation', consultation_cat, 100.00),
            ('Emergency Consultation', 'consultation', consultation_cat, 150.00),
            ('Blood Test - CBC', 'lab_test', lab_cat, 25.00),
            ('Urine Analysis', 'lab_test', lab_cat, 20.00),
            ('X-Ray Chest', 'imaging', lab_cat, 75.00),
        ]
        
        for name, service_type, category, price in services:
            service, created = ServiceCharge.objects.get_or_create(
                name=name,
                defaults={
                    'service_type': service_type,
                    'category': category,
                    'base_price': price
                }
            )
            if created:
                self.stdout.write(f'Created service: {name}')
        
        # Create lab test categories
        lab_categories = [
            ('Hematology', 'Blood related tests'),
            ('Biochemistry', 'Chemical analysis tests'),
            ('Microbiology', 'Infection and culture tests'),
            ('Pathology', 'Tissue and cell analysis'),
            ('Radiology', 'Imaging tests'),
            ('Cardiology', 'Heart related tests')
        ]
        
        for cat_name, description in lab_categories:
            cat, created = LabTestCategory.objects.get_or_create(
                name=cat_name,
                defaults={'description': description}
            )
            if created:
                self.stdout.write(f'Created lab category: {cat_name}')
        
        # Create sample lab tests
        hematology_cat = LabTestCategory.objects.get(name='Hematology')
        biochemistry_cat = LabTestCategory.objects.get(name='Biochemistry')
        
        lab_tests = [
            ('Complete Blood Count (CBC)', hematology_cat, 'Blood', '4.5-11.0 x10³/μL', 'cells/μL', 25.00),
            ('Hemoglobin', hematology_cat, 'Blood', '12-16 g/dL', 'g/dL', 15.00),
            ('Blood Glucose', biochemistry_cat, 'Blood', '70-100 mg/dL', 'mg/dL', 20.00),
            ('Cholesterol Total', biochemistry_cat, 'Blood', '<200 mg/dL', 'mg/dL', 30.00),
            ('Urine Analysis', biochemistry_cat, 'Urine', 'Normal', '', 20.00),
        ]
        
        for name, category, sample_type, normal_range, unit, price in lab_tests:
            test, created = LabTest.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'sample_type': sample_type,
                    'normal_range': normal_range,
                    'unit': unit,
                    'price': price,
                    'turnaround_time_hours': 24
                }
            )
            if created:
                self.stdout.write(f'Created lab test: {name}')
        
        # Create sample medicines
        medicines = [
            ('Paracetamol', 'Acetaminophen', 'Generic Pharma', 'tablet', '500mg', 0.50),
            ('Amoxicillin', 'Amoxicillin', 'Generic Pharma', 'capsule', '250mg', 1.20),
            ('Ibuprofen', 'Ibuprofen', 'Generic Pharma', 'tablet', '400mg', 0.75),
            ('Cough Syrup', 'Dextromethorphan', 'Generic Pharma', 'syrup', '100ml', 5.00),
            ('Insulin', 'Human Insulin', 'Diabetes Care', 'injection', '100IU/ml', 25.00),
        ]
        
        for name, generic_name, manufacturer, med_type, strength, price in medicines:
            medicine, created = Medicine.objects.get_or_create(
                name=name,
                defaults={
                    'generic_name': generic_name,
                    'manufacturer': manufacturer,
                    'medicine_type': med_type,
                    'strength': strength,
                    'unit_price': price,
                    'minimum_stock_level': 50
                }
            )
            if created:
                self.stdout.write(f'Created medicine: {name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully set up initial hospital data!')
        )