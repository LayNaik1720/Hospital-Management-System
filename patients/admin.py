from django.contrib import admin
from .models import Patient, PatientInsurance

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'first_name', 'last_name', 'phone', 'gender', 'is_active', 'created_at')
    list_filter = ('gender', 'blood_group', 'is_active', 'created_at')
    search_fields = ('patient_id', 'first_name', 'last_name', 'phone', 'email')
    readonly_fields = ('patient_id', 'created_at', 'updated_at')

@admin.register(PatientInsurance)
class PatientInsuranceAdmin(admin.ModelAdmin):
    list_display = ('patient', 'provider_name', 'policy_number', 'is_primary', 'coverage_start_date', 'coverage_end_date')
    list_filter = ('is_primary', 'provider_name', 'coverage_start_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'policy_number', 'provider_name')