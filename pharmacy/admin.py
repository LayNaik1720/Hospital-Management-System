from django.contrib import admin
from .models import Medicine, MedicineBatch, Prescription, PrescriptionItem, PharmacySale

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'generic_name', 'manufacturer', 'medicine_type', 'unit_price', 'is_active')
    list_filter = ('medicine_type', 'manufacturer', 'is_active', 'is_prescription_required')
    search_fields = ('name', 'generic_name', 'manufacturer')

@admin.register(MedicineBatch)
class MedicineBatchAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'batch_number', 'expiry_date', 'remaining_quantity', 'selling_price')
    list_filter = ('expiry_date', 'created_at')
    search_fields = ('medicine__name', 'batch_number', 'supplier')

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_id', 'patient', 'doctor', 'prescription_date', 'is_dispensed')
    list_filter = ('is_dispensed', 'prescription_date')
    search_fields = ('prescription_id', 'patient__first_name', 'patient__last_name')
    readonly_fields = ('prescription_id', 'prescription_date')

@admin.register(PharmacySale)
class PharmacySaleAdmin(admin.ModelAdmin):
    list_display = ('sale_id', 'patient', 'final_amount', 'payment_method', 'sale_date')
    list_filter = ('payment_method', 'sale_date')
    search_fields = ('sale_id', 'patient__first_name', 'patient__last_name')
    readonly_fields = ('sale_id', 'sale_date')