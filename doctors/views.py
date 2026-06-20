from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from accounts.decorators import role_required
from .models import Doctor, Department, DoctorSchedule

@login_required
@role_required(['admin', 'receptionist', 'doctor', 'nurse'])
def doctor_list(request):
    search_query = request.GET.get('search', '')
    department_filter = request.GET.get('department', '')
    
    doctors = Doctor.objects.filter(is_available=True).select_related('user', 'department')
    
    if search_query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(employee_id__icontains=search_query) |
            Q(specialization__icontains=search_query)
        )
    
    if department_filter:
        doctors = doctors.filter(department_id=department_filter)
    
    doctors = doctors.order_by('user__first_name')
    paginator = Paginator(doctors, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    departments = Department.objects.filter(is_active=True).order_by('name')
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'department_filter': department_filter,
        'departments': departments,
        'total_doctors': Doctor.objects.filter(is_available=True).count(),
    }
    return render(request, 'doctors/doctor_list.html', context)

@login_required
@role_required(['admin', 'receptionist', 'doctor', 'nurse'])
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk, is_available=True)
    schedules = doctor.schedules.filter(is_active=True).order_by('day_of_week', 'start_time')
    recent_appointments = doctor.appointments.select_related('patient').order_by('-appointment_date')[:10]
    
    context = {
        'doctor': doctor,
        'schedules': schedules,
        'recent_appointments': recent_appointments,
    }
    return render(request, 'doctors/doctor_detail.html', context)

@login_required
@role_required(['admin'])
def department_list(request):
    departments = Department.objects.filter(is_active=True).order_by('name')
    
    context = {
        'departments': departments,
    }
    return render(request, 'doctors/department_list.html', context)