from django.db import models
from django.contrib.auth import get_user_model
from patients.models import Patient
from doctors.models import Doctor

User = get_user_model()

class LabTest(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=100)
    normal_range = models.CharField(max_length=200, blank=True, help_text="Normal reference range")
    unit = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sample_type = models.CharField(max_length=50, help_text="Blood, Urine, Stool, etc.")
    preparation_instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class LabTestRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sample_collected', 'Sample Collected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    request_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_requests')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='lab_requests')
    tests = models.ManyToManyField(LabTest, related_name='requests')
    requested_at = models.DateTimeField(auto_now_add=True)
    sample_collected_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=[
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('stat', 'STAT')
    ], default='routine')
    clinical_notes = models.TextField(blank=True)
    sample_collected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='collected_samples')

    def save(self, *args, **kwargs):
        if not self.request_id:
            import uuid
            self.request_id = f"LAB{str(uuid.uuid4().int)[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.request_id} - {self.patient.full_name}"

    @property
    def total_cost(self):
        return sum(test.price for test in self.tests.all())

class LabTestResult(models.Model):
    request = models.ForeignKey(LabTestRequest, on_delete=models.CASCADE, related_name='results')
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    result_value = models.CharField(max_length=500)
    reference_range = models.CharField(max_length=200, blank=True)
    is_abnormal = models.BooleanField(default=False)
    comments = models.TextField(blank=True)
    tested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='performed_tests')
    tested_at = models.DateTimeField(auto_now_add=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_tests')
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['request', 'test']

    def __str__(self):
        return f"{self.test.name}: {self.result_value}"