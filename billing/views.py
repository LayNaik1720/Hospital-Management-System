from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from accounts.decorators import role_required
from .models import Bill, Payment, BillingCategory, ServiceCharge

@login_required
@role_required(['admin', 'accountant', 'receptionist'])
def bill_list(request):
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    bills = Bill.objects.select_related('patient')
    
    if status_filter:
        bills = bills.filter(status=status_filter)
    
    if search_query:
        bills = bills.filter(
            Q(bill_number__icontains=search_query) |
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(patient__patient_id__icontains=search_query)
        )
    
    bills = bills.order_by('-bill_date')
    paginator = Paginator(bills, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': Bill.STATUS_CHOICES,
    }
    return render(request, 'billing/bill_list.html', context)

@login_required
@role_required(['admin', 'accountant', 'receptionist'])
def bill_detail(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    payments = bill.payments.order_by('-payment_date')
    
    context = {
        'bill': bill,
        'payments': payments,
    }
    return render(request, 'billing/bill_detail.html', context)

@login_required
@role_required(['admin', 'accountant'])
def payment_list(request):
    payments = Payment.objects.select_related('bill__patient').order_by('-payment_date')
    paginator = Paginator(payments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'billing/payment_list.html', context)

@login_required
@role_required(['admin', 'accountant'])
def service_charges(request):
    categories = BillingCategory.objects.filter(is_active=True).prefetch_related('services')
    
    context = {
        'categories': categories,
    }
    return render(request, 'billing/service_charges.html', context)