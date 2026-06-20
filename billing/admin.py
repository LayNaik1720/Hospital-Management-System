from django.contrib import admin
from .models import BillingCategory, ServiceCharge, Bill, BillItem, Payment

@admin.register(BillingCategory)
class BillingCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(ServiceCharge)
class ServiceChargeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'amount', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'code')

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_number', 'patient', 'total_amount', 'paid_amount', 'status', 'bill_date')
    list_filter = ('status', 'bill_date')
    search_fields = ('bill_number', 'patient__first_name', 'patient__last_name')
    readonly_fields = ('bill_number', 'bill_date')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'bill', 'amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('payment_id', 'bill__bill_number')
    readonly_fields = ('payment_id', 'payment_date')