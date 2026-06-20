from django.db import models
from django.contrib.auth import get_user_model
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment

User = get_user_model()

class MedicalRecord(models.Model):
    record_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medical_records')
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    visit_date = models.DateTimeField(auto_now_add=True)
    chief_complaint = models.TextField(help_text="Patient's main concern")
    history_of_present_illness = models.TextField(blank=True)
    physical_examination = models.TextField(blank=True)
    vital_signs = models.JSONField(default=dict, blank=True, help_text="Blood pressure, temperature, etc.")
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    follow_up_instructions = models.TextField(blank=True)
    next_visit_date = models.DateField(null=True, blank=True)
    is_confidential = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.record_id:
            import uuid
            self.record_id = f"MR{str(uuid.uuid4().int)[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.record_id} - {self.patient.full_name} ({self.visit_date.date()})"

class MedicalRecordFile(models.Model):
    FILE_TYPE_CHOICES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('report', 'Report'),
        ('xray', 'X-Ray'),
        ('scan', 'Scan'),
    ]
    
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='medical_records/%Y/%m/')
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES)
    description = models.CharField(max_length=200, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medical_record.record_id} - {self.description or self.file.name}"

class VitalSigns(models.Model):
    medical_record = models.OneToOneField(MedicalRecord, on_delete=models.CASCADE, related_name='vital_signs_detail')
    blood_pressure_systolic = models.PositiveIntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.PositiveIntegerField(null=True, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True, help_text="beats per minute")
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="in Fahrenheit")
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True, help_text="breaths per minute")
    oxygen_saturation = models.PositiveIntegerField(null=True, blank=True, help_text="percentage")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="in kg")
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="in cm")
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vitals for {self.medical_record.record_id}"

    @property
    def bmi(self):
        if self.weight and self.height:
            height_m = float(self.height) / 100  # Convert cm to meters
            return round(float(self.weight) / (height_m ** 2), 2)
        return None