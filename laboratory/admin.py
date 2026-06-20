from django.contrib import admin
from .models import LabTest, LabTestRequest, LabTestResult

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'price', 'sample_type', 'is_active')
    list_filter = ('category', 'sample_type', 'is_active')
    search_fields = ('name', 'code', 'category')

@admin.register(LabTestRequest)
class LabTestRequestAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'patient', 'doctor', 'status', 'priority', 'requested_at')
    list_filter = ('status', 'priority', 'requested_at')
    search_fields = ('request_id', 'patient__first_name', 'patient__last_name')
    readonly_fields = ('request_id', 'requested_at')

@admin.register(LabTestResult)
class LabTestResultAdmin(admin.ModelAdmin):
    list_display = ('request', 'test', 'result_value', 'is_abnormal', 'tested_at')
    list_filter = ('is_abnormal', 'tested_at')
    search_fields = ('request__request_id', 'test__name')