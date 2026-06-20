from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('financial-reports/', views.financial_reports, name='financial_reports'),
    path('patient-statistics/', views.patient_statistics, name='patient_statistics'),
    path('system-reports/', views.system_reports, name='system_reports'),
]