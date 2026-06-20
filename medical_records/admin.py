from django.contrib import admin
from .models import MedicalRecord, MedicalRecordFile, VitalSigns

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'patient', 'doctor', 'visit_date', 'is_confidential')
    list_filter = ('is_confidential', 'visit_date', 'created_at')
    search_fields = ('record_id', 'patient__first_name', 'patient__last_name', 'diagnosis')
    readonly_fields = ('record_id', 'created_at', 'updated_at')

@admin.register(VitalSigns)
class VitalSignsAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate', 'temperature', 'recorded_at')
    list_filter = ('recorded_at',)
    search_fields = ('medical_record__record_id', 'medical_record__patient__first_name')