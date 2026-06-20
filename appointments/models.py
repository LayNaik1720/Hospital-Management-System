from django.db import models
from django.contrib.auth import get_user_model
from patients.models import Patient
from doctors.models import Doctor

User = get_user_model()

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    APPOINTMENT_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow Up'),
        ('emergency', 'Emergency'),
        ('routine_checkup', 'Routine Checkup'),
    ]
    
    appointment_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default='consultation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    reason = models.TextField(help_text="Reason for appointment")
    notes = models.TextField(blank=True, help_text="Additional notes")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_appointments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
        ordering = ['appointment_date', 'appointment_time']

    def save(self, *args, **kwargs):
        if not self.appointment_id:
            import uuid
            self.appointment_id = f"APT{str(uuid.uuid4().int)[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.appointment_id} - {self.patient.full_name} with {self.doctor.full_name}"

    @property
    def can_be_cancelled(self):
        from django.utils import timezone
        appointment_datetime = timezone.datetime.combine(self.appointment_date, self.appointment_time)
        return self.status in ['scheduled', 'confirmed'] and appointment_datetime > timezone.now()