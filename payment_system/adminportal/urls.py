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
    path('profilesettings/', views.adm_profile, name='adm_profile'),
     path('editpaymentsetup/<int:id>/', views.payment_edit, name='payment_edit'),
    path('paymentdetails/<int:payment_id>/', views.payment_details, name='paymentdetails'),

    # API to get the fees deatils assigned by the student.
    path('getfeesassigned/', views.get_Fees_details, name='get_Fees_details'),

    # URL to create a table to store the fees details of a respective class
    # use CSE01 for computer science and engineering and ISE02 for information science and engineering
    path('paiddetails/', views.Paid_details, name='Paid_details')
]
