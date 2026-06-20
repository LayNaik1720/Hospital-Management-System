from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('bills/', views.bill_list, name='bill_list'),
    path('bills/<int:pk>/', views.bill_detail, name='bill_detail'),
    path('payments/', views.payment_list, name='payment_list'),
    path('services/', views.service_charges, name='service_charges'),
]