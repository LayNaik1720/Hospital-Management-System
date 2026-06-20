from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from accounts.decorators import role_required

# Import models with error handling
try:
    from patients.models import Patient
except ImportError:
    Patient = None

try:
    from appointments.models import Appointment
except ImportError:
    Appointment = None

try:
    from billing.models import Bill, Payment
except ImportError:
    Bill = None
    Payment = None

try:
    from pharmacy.models import PharmacySale, Medicine
except ImportError:
    PharmacySale = None
    Medicine = None

try:
    from laboratory.models import LabTestRequest
except ImportError:
    LabTestRequest = None

try:
    from doctors.models import Doctor, Department
except ImportError:
    Doctor = None
    Department = None

@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()
    
    # Common statistics
    context = {
        'user': user,
        'today': today,
    }
    
    if user.is_admin or user.is_receptionist:
        # Admin/Receptionist Dashboard
        dashboard_data = {}
        
        if Patient:
            dashboard_data['total_patients'] = Patient.objects.filter(is_active=True).count()
            dashboard_data['recent_patients'] = Patient.objects.filter(is_active=True).order_by('-created_at')[:5]
        
        if Doctor:
            dashboard_data['total_doctors'] = Doctor.objects.filter(is_available=True).count()
        
        if Appointment:
            dashboard_data['todays_appointments'] = Appointment.objects.filter(
                appointment_date=today,
                status__in=['scheduled', 'confirmed', 'in_progress']
            ).count()
            dashboard_data['recent_appointments'] = Appointment.objects.filter(
                appointment_date=today
            ).select_related('patient', 'doctor__user').order_by('appointment_time')[:10]
        
        if Bill:
            dashboard_data['pending_bills'] = Bill.objects.filter(status='pending').count()
        
        context.update(dashboard_data)
    
    elif user.is_doctor:
        # Doctor Dashboard
        try:
            doctor = user.doctor
            dashboard_data = {}
            
            if Appointment:
                dashboard_data['todays_appointments'] = Appointment.objects.filter(
                    doctor=doctor,
                    appointment_date=today,
                    status__in=['scheduled', 'confirmed', 'in_progress']
                ).select_related('patient').order_by('appointment_time')
                
                dashboard_data['total_patients_treated'] = Appointment.objects.filter(
                    doctor=doctor,
                    status='completed'
                ).values('patient').distinct().count()
            
            if LabTestRequest:
                dashboard_data['pending_lab_requests'] = LabTestRequest.objects.filter(
                    doctor=doctor,
                    status__in=['pending', 'sample_collected']
                ).count()
            
            context.update(dashboard_data)
        except:
            pass
    
    elif user.is_pharmacist:
        # Pharmacist Dashboard
        dashboard_data = {}
        
        if PharmacySale:
            dashboard_data['todays_sales'] = PharmacySale.objects.filter(
                sale_date__date=today
            ).aggregate(total=Sum('final_amount'))['total'] or 0
            
            dashboard_data['recent_sales'] = PharmacySale.objects.filter(
                sale_date__date=today
            ).select_related('patient').order_by('-sale_date')[:5]
        
        if Medicine:
            dashboard_data['low_stock_medicines'] = Medicine.objects.filter(
                is_active=True
            ).annotate(
                current_stock=Sum('batches__remaining_quantity')
            ).filter(
                current_stock__lte=F('minimum_stock_level')
            ).count()
        
        context.update(dashboard_data)
    
    elif user.is_lab_technician:
        # Lab Technician Dashboard
        dashboard_data = {}
        
        if LabTestRequest:
            dashboard_data['pending_tests'] = LabTestRequest.objects.filter(
                status__in=['pending', 'sample_collected']
            ).count()
            
            dashboard_data['todays_requests'] = LabTestRequest.objects.filter(
                requested_at__date=today
            ).select_related('patient', 'doctor__user').order_by('-requested_at')[:10]
        
        context.update(dashboard_data)
    
    elif user.is_accountant:
        # Accountant Dashboard
        dashboard_data = {}
        
        if Payment:
            dashboard_data['todays_revenue'] = Payment.objects.filter(
                payment_date__date=today
            ).aggregate(total=Sum('amount'))['total'] or 0
        
        if Bill:
            dashboard_data['pending_bills'] = Bill.objects.filter(
                status__in=['pending', 'partially_paid']
            ).count()
            
            dashboard_data['overdue_bills'] = Bill.objects.filter(
                due_date__lt=today,
                status__in=['pending', 'partially_paid']
            ).count()
        
        context.update(dashboard_data)
    
    return render(request, 'analytics/dashboard.html', context)

@login_required
@role_required(['admin', 'accountant'])
def financial_reports(request):
    # Date range filter
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    if request.GET.get('start_date'):
        start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d').date()
    if request.GET.get('end_date'):
        end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d').date()
    
    # Revenue statistics
    total_revenue = 0
    bills_by_status = []
    daily_revenue = []
    
    if Payment:
        total_revenue = Payment.objects.filter(
            payment_date__date__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        daily_revenue = Payment.objects.filter(
            payment_date__date__range=[start_date, end_date]
        ).extra(
            select={'day': 'date(payment_date)'}
        ).values('day').annotate(total=Sum('amount')).order_by('day')
    
    if Bill:
        bills_by_status = Bill.objects.filter(
            bill_date__date__range=[start_date, end_date]
        ).values('status').annotate(count=Count('id'), total=Sum('total_amount'))
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'total_revenue': total_revenue,
        'bills_by_status': bills_by_status,
        'daily_revenue': daily_revenue,
    }
    
    return render(request, 'analytics/financial_reports.html', context)

@login_required
@role_required(['admin', 'doctor'])
def patient_statistics(request):
    # Patient demographics
    patients_by_gender = []
    patients_by_age = {}
    recent_registrations = []
    total_patients = 0
    
    if Patient:
        from django.db.models import Case, When, IntegerField
        
        patients_by_gender = Patient.objects.filter(is_active=True).values('gender').annotate(count=Count('id'))
        
        patients_by_age = Patient.objects.filter(is_active=True).aggregate(
            under_18=Count(Case(When(date_of_birth__year__gt=timezone.now().year-18, then=1))),
            age_18_30=Count(Case(When(
                date_of_birth__year__lte=timezone.now().year-18,
                date_of_birth__year__gt=timezone.now().year-30,
                then=1
            ))),
            age_31_50=Count(Case(When(
                date_of_birth__year__lte=timezone.now().year-30,
                date_of_birth__year__gt=timezone.now().year-50,
                then=1
            ))),
            over_50=Count(Case(When(date_of_birth__year__lte=timezone.now().year-50, then=1)))
        )
        
        recent_registrations = Patient.objects.filter(
            is_active=True,
            created_at__gte=timezone.now() - timedelta(days=30)
        ).extra(
            select={'day': 'date(created_at)'}
        ).values('day').annotate(count=Count('id')).order_by('day')
        
        total_patients = Patient.objects.filter(is_active=True).count()
    
    context = {
        'patients_by_gender': patients_by_gender,
        'patients_by_age': patients_by_age,
        'recent_registrations': recent_registrations,
        'total_patients': total_patients,
    }
    
    return render(request, 'analytics/patient_statistics.html', context)

@login_required
@role_required(['admin'])
def system_reports(request):
    # User activity - simplified for now
    recent_activities = []
    departments_stats = []
    
    if Department:
        departments_stats = Department.objects.filter(is_active=True).annotate(
            doctor_count=Count('doctors', filter=Q(doctors__is_available=True))
        )
    
    context = {
        # 'recent_activities': recent_activities,  # Commented out until SystemLog model is created
        'departments_stats': departments_stats,
    }
    
    return render(request, 'analytics/system_reports.html', context)