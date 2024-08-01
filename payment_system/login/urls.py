from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('validation/', views.login_validation, name='login_validation'),
    path('do_logout/', views.do_logout, name='do_logout')
]
