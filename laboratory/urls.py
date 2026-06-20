from django.urls import path
from . import views

app_name = 'laboratory'

urlpatterns = [
    path('requests/', views.test_request_list, name='test_request_list'),
    path('requests/<int:pk>/', views.test_request_detail, name='test_request_detail'),
    path('tests/', views.test_list, name='test_list'),
]