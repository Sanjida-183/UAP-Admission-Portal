# urls.py - FINAL VERSION
from django.urls import path
from . import views

app_name = 'admission'# admission/urls.py - Make sure these lines exist
from django.urls import path
from . import views

app_name = 'admission'

urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.admission_info, name='admission_info'),
    path('apply/', views.admission_online, name='admission_online'),
    path('apply/submit/', views.application_create, name='application_create'),
    path('application/<uuid:pk>/', views.application_detail, name='application_detail'),
    
    # Student URLs - Add these
    path('student/register/', views.student_register, name='student_register'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    
    # staff actions
    path('application/<uuid:pk>/accept/', views.accept_applicant, name='accept_applicant'),
    path('application/<uuid:pk>/reject/', views.reject_applicant, name='reject_applicant'),
    
    # auth
    path('staff/login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.admission_info, name='admission_info'),
    path('apply/', views.admission_online, name='admission_online'),
    path('apply/submit/', views.application_create, name='application_create'),
    path('application/<uuid:pk>/', views.application_detail, name='application_detail'),
    
    # Student authentication URLs - ADD THESE
    path('student/register/', views.student_register, name='student_register'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    
    # staff actions
    path('application/<uuid:pk>/accept/', views.accept_applicant, name='accept_applicant'),
    path('application/<uuid:pk>/reject/', views.reject_applicant, name='reject_applicant'),
    
    # auth
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]