from django.urls import path
from . import views

app_name = 'medical_records'

urlpatterns = [
    path('', views.medical_record_list, name='record_list'),
    path('<int:pk>/', views.medical_record_detail, name='record_detail'),
]