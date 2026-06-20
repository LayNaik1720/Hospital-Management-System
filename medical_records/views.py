from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from accounts.decorators import role_required
from .models import MedicalRecord, VitalSigns

@login_required
@role_required(['admin', 'doctor', 'nurse'])
def medical_record_list(request):
    search_query = request.GET.get('search', '')
    records = MedicalRecord.objects.select_related('patient', 'doctor__user')
    
    if search_query:
        records = records.filter(
            Q(record_id__icontains=search_query) |
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(patient__patient_id__icontains=search_query)
        )
    
    # Filter by user role
    if request.user.is_doctor:
        try:
            doctor = request.user.doctor
            records = records.filter(doctor=doctor)
        except:
            records = records.none()
    
    records = records.order_by('-visit_date')
    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'medical_records/record_list.html', context)

@login_required
@role_required(['admin', 'doctor', 'nurse'])
def medical_record_detail(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    
    # Check permissions
    if request.user.is_doctor:
        try:
            if record.doctor != request.user.doctor:
                messages.error(request, 'You can only view your own medical records.')
                return redirect('medical_records:record_list')
        except:
            messages.error(request, 'Access denied.')
            return redirect('medical_records:record_list')
    
    files = record.files.order_by('-uploaded_at')
    
    context = {
        'record': record,
        'files': files,
    }
    return render(request, 'medical_records/record_detail.html', context)