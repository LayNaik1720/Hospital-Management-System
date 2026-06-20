from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from accounts.decorators import role_required
from .models import Patient, PatientInsurance
from .forms import PatientForm, PatientInsuranceForm

@login_required
@role_required(['admin', 'receptionist', 'doctor', 'nurse'])
def patient_list(request):
    search_query = request.GET.get('search', '')
    patients = Patient.objects.filter(is_active=True)
    
    if search_query:
        patients = patients.filter(
            Q(patient_id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    patients = patients.order_by('-created_at')
    paginator = Paginator(patients, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_patients': Patient.objects.filter(is_active=True).count(),
    }
    return render(request, 'patients/patient_list.html', context)

@login_required
@role_required(['admin', 'receptionist'])
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.save()
            messages.success(request, f'Patient {patient.full_name} registered successfully with ID: {patient.patient_id}')
            return redirect('patients:patient_detail', pk=patient.pk)
    else:
        form = PatientForm()
    
    return render(request, 'patients/patient_form.html', {
        'form': form,
        'title': 'Register New Patient'
    })

@login_required
@role_required(['admin', 'receptionist', 'doctor', 'nurse'])
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk, is_active=True)
    recent_appointments = patient.appointments.select_related('doctor__user').order_by('-appointment_date')[:5]
    recent_records = patient.medical_records.select_related('doctor__user').order_by('-visit_date')[:5]
    insurance_policies = patient.insurance_policies.filter(coverage_end_date__gte=timezone.now().date())
    
    context = {
        'patient': patient,
        'recent_appointments': recent_appointments,
        'recent_records': recent_records,
        'insurance_policies': insurance_policies,
    }
    return render(request, 'patients/patient_detail.html', context)

@login_required
@role_required(['admin', 'receptionist'])
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk, is_active=True)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f'Patient {patient.full_name} updated successfully.')
            return redirect('patients:patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    
    return render(request, 'patients/patient_form.html', {
        'form': form,
        'patient': patient,
        'title': f'Update Patient - {patient.full_name}'
    })

@login_required
@role_required(['admin'])
def patient_deactivate(request, pk):
    patient = get_object_or_404(Patient, pk=pk, is_active=True)
    
    if request.method == 'POST':
        patient.is_active = False
        patient.save()
        messages.success(request, f'Patient {patient.full_name} has been deactivated.')
        return redirect('patients:patient_list')
    
    return render(request, 'patients/patient_confirm_deactivate.html', {'patient': patient})

@login_required
@role_required(['admin', 'receptionist'])
def add_insurance(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk, is_active=True)
    
    if request.method == 'POST':
        form = PatientInsuranceForm(request.POST)
        if form.is_valid():
            insurance = form.save(commit=False)
            insurance.patient = patient
            insurance.save()
            messages.success(request, 'Insurance policy added successfully.')
            return redirect('patients:patient_detail', pk=patient.pk)
    else:
        form = PatientInsuranceForm()
    
    return render(request, 'patients/insurance_form.html', {
        'form': form,
        'patient': patient,
        'title': f'Add Insurance for {patient.full_name}'
    })