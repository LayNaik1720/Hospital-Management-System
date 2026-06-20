from django.contrib import admin
from .models import Department, Doctor, DoctorSchedule

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_of_department', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'specialization', 'department', 'consultation_fee', 'is_available')
    list_filter = ('department', 'specialization', 'is_available', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'employee_id', 'specialization')

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day_of_week', 'start_time', 'end_time', 'is_active')
    list_filter = ('day_of_week', 'is_active')
    search_fields = ('doctor__user__first_name', 'doctor__user__last_name')