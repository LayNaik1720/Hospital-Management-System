from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from accounts.decorators import role_required
from .models import LabTest, LabTestRequest, LabTestResult

@login_required
@role_required(['admin', 'lab_technician', 'doctor'])
def test_request_list(request):
    status_filter = request.GET.get('status', '')
    requests = LabTestRequest.objects.select_related('patient', 'doctor__user')
    
    if status_filter:
        requests = requests.filter(status=status_filter)
    
    # Filter by user role
    if request.user.is_doctor:
        try:
            doctor = request.user.doctor
            requests = requests.filter(doctor=doctor)
        except:
            requests = requests.none()
    
    requests = requests.order_by('-requested_at')
    paginator = Paginator(requests, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'status_choices': LabTestRequest.STATUS_CHOICES,
    }
    return render(request, 'laboratory/test_request_list.html', context)

@login_required
@role_required(['admin', 'lab_technician', 'doctor'])
def test_request_detail(request, pk):
    test_request = get_object_or_404(LabTestRequest, pk=pk)
    
    # Check permissions
    if request.user.is_doctor:
        try:
            if test_request.doctor != request.user.doctor:
                messages.error(request, 'You can only view your own test requests.')
                return redirect('laboratory:test_request_list')
        except:
            messages.error(request, 'Access denied.')
            return redirect('laboratory:test_request_list')
    
    results = test_request.results.select_related('test').order_by('test__name')
    
    context = {
        'test_request': test_request,
        'results': results,
    }
    return render(request, 'laboratory/test_request_detail.html', context)

@login_required
@role_required(['admin', 'lab_technician'])
def test_list(request):
    tests = LabTest.objects.filter(is_active=True).order_by('category', 'name')
    
    context = {
        'tests': tests,
    }
    return render(request, 'laboratory/test_list.html', context)