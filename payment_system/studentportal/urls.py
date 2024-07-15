from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('payment/', views.payment, name='student_payment'),  
    path('queries/', views.queries, name='student_queries'),  
    path('settings/', views.acc_settings, name='student_settings'),  

]
