from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('videoupload', views.videoupload, name='videoupload'),
    
    path('login', views.login_form, name='login'),
    
    path('booking', views.booking, name='booking'), 
    
    path('booked', views.booked, name='booked'), 
    
    path('logout', views.logout_view, name='logout'),
    
    path('register', views.register, name='register'),
    
    path('emailconfirmation', views.emailconfirmation, name='emailconfirmation'),
    
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    
    path('process-payment/', views.process_payment, name='process_payment'),
    
    path('payment-done/', views.payment_done, name='payment_done'),
    
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
       
]