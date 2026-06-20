from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import date
from accounts.decorators import role_required
from .models import Appointment
from patients.models import Patient
from doctors.models import Doctor, Department

def public_book_appointment(request):
    if request.method == 'POST':
        try:
            # Get or create patient
            patient_name = request.POST.get('patient_name')
            patient_phone = request.POST.get('patient_phone')
            patient_email = request.POST.get('patient_email')
            department_name = request.POST.get('department')
            preferred_date = request.POST.get('preferred_date')
            preferred_time = request.POST.get('preferred_time')
            reason = request.POST.get('reason', 'General consultation')
            
            # Create patient if doesn't exist
            names = patient_name.split(' ', 1)
            first_name = names[0]
            last_name = names[1] if len(names) > 1 else ''
            
            patient, created = Patient.objects.get_or_create(
                phone=patient_phone,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': patient_email or '',
                    'date_of_birth': date(1990, 1, 1),  # Default DOB
                    'gender': 'M',
                    'address': 'To be updated',
                    'emergency_contact_name': 'To be updated',
                    'emergency_contact_phone': patient_phone,
                    'emergency_contact_relation': 'Self'
                }
            )
            
            # Get department and assign doctor
            try:
                department = Department.objects.get(name__icontains=department_name)
                doctor = department.doctors.filter(is_available=True).first()
            except:
                doctor = Doctor.objects.filter(is_available=True).first()
            
            if doctor:
                # Create appointment
                appointment = Appointment.objects.create(
                    patient=patient,
                    doctor=doctor,
                    appointment_date=preferred_date,
                    appointment_time=preferred_time,
                    reason=reason,
                    status='scheduled'
                )
                
                messages.success(request, f'Appointment booked successfully! Your appointment ID is {appointment.appointment_id}. We will contact you soon.')
            else:
                messages.error(request, 'No doctors available. Please try again later.')
                
        except Exception as e:
            messages.error(request, 'Error booking appointment. Please try again.')
    
    return redirect('home')

@login_required
@role_required(['admin', 'receptionist', 'doctor'])
def appointment_list(request):
    date_filter = request.GET.get('date', '')
    status_filter = request.GET.get('status', '')
    doctor_filter = request.GET.get('doctor', '')
    
    appointments = Appointment.objects.select_related('patient', 'doctor__user')
    
    if date_filter:
        appointments = appointments.filter(appointment_date=date_filter)
    else:
        # Default to today's appointments
        appointments = appointments.filter(appointment_date=timezone.now().date())
    
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    if doctor_filter:
        appointments = appointments.filter(doctor_id=doctor_filter)
    
    # Filter by user role
    if request.user.is_doctor:
        try:
            doctor = request.user.doctor
            appointments = appointments.filter(doctor=doctor)
        except:
            appointments = appointments.none()
    
    appointments = appointments.order_by('appointment_time')
    paginator = Paginator(appointments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    doctors = Doctor.objects.filter(is_available=True).select_related('user')
    
    context = {
        'page_obj': page_obj,
        'date_filter': date_filter,
        'status_filter': status_filter,
        'doctor_filter': doctor_filter,
        'doctors': doctors,
        'status_choices': Appointment.STATUS_CHOICES,
        'today': timezone.now().date(),
    }
    return render(request, 'appointments/appointment_list.html', context)

@login_required
@role_required(['admin', 'receptionist'])
def appointment_create(request):
    if request.method == 'POST':
        # Handle appointment creation
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason')
        
        try:
            patient = Patient.objects.get(pk=patient_id)
            doctor = Doctor.objects.get(pk=doctor_id)
            
            # Check for conflicts
            existing = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=['scheduled', 'confirmed', 'in_progress']
            ).exists()
            
            if existing:
                messages.error(request, 'This time slot is already booked.')
            else:
                appointment = Appointment.objects.create(
                    patient=patient,
                    doctor=doctor,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    reason=reason,
                    created_by=request.user
                )
                messages.success(request, f'Appointment scheduled successfully. ID: {appointment.appointment_id}')
                return redirect('appointments:appointment_list')
        except Exception as e:
            messages.error(request, f'Error creating appointment: {str(e)}')
    
    patients = Patient.objects.filter(is_active=True).order_by('first_name')
    doctors = Doctor.objects.filter(is_available=True).select_related('user')
    
    context = {
        'patients': patients,
        'doctors': doctors,
        'today': timezone.now().date(),
    }
    return render(request, 'appointments/appointment_form.html', context)

@login_required
@role_required(['admin', 'receptionist', 'doctor'])
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Check permissions
    if request.user.is_doctor:
        try:
            if appointment.doctor != request.user.doctor:
                messages.error(request, 'You can only view your own appointments.')
                return redirect('appointments:appointment_list')
        except:
            messages.error(request, 'Access denied.')
            return redirect('appointments:appointment_list')
    
    context = {
        'appointment': appointment,
    }
    return render(request, 'appointments/appointment_detail.html', context)