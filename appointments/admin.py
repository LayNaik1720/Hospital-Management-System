from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient', 'doctor', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_type', 'appointment_date', 'created_at')
    search_fields = ('appointment_id', 'patient__first_name', 'patient__last_name', 'doctor__user__first_name', 'doctor__user__last_name')
    readonly_fields = ('appointment_id', 'created_at', 'updated_at')
    date_hierarchy = 'appointment_date'