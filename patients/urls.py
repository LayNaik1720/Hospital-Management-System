from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('register/', views.patient_create, name='patient_create'),
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
    path('<int:pk>/update/', views.patient_update, name='patient_update'),
    path('<int:pk>/deactivate/', views.patient_deactivate, name='patient_deactivate'),
    path('<int:patient_pk>/add-insurance/', views.add_insurance, name='add_insurance'),
]