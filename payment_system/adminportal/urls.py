from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.adm_dashboard, name='adm_dashboard'),
    path('upload/', views.addStudent, name='addStudent'),
    path('getCourse/', views.course, name='course'),
    path('studentData/', views.studentDetails, name='studentDetails'),
    
    path('studentlist/', views.student_list, name='student_list'),
    path('paymentsetup/', views.payment_setup, name='payment_setup'),
    path('paymenthistory/', views.payment_history, name='payment_history'),
]
