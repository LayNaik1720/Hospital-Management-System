from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register-staff/', views.register_staff, name='register_staff'),
    path('profile/', views.profile_view, name='profile'),
]