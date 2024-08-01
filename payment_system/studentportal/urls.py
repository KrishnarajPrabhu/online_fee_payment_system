from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='student_dashboard'),
    path('payment/', views.payment, name='student_payment'),
    path('queries/', views.queries, name='student_queries'),
    path('settings/', views.acc_settings, name='student_settings'),

    # To handel pending fees of a student
    path('pending-fees/', views.pending_fees, name='pending-fees'),
    path('get-payment-data/', views.razorpay_invoke_data,
         name='razorpay_invoke_data'),  # To return payment details
    # To handel post request sent by razerpay.
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),

    # To return student transaction to the frontend.
    path('student-transaction-detail/',
         views.student_transaction, name='student-transaction-detail'),

    path('demo/', views.demo, name='demo'),
]
