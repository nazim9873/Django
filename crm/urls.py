from django.contrib import admin
from django.urls import path
from crm import views

app_name="crm"
urlpatterns = [
    path('', views.index, name='crm'),
    path('services/', views.services, name='services'),
    path('enquiry/', views.enquiry, name='enquiry'),
    path('enquiry_followup/<str:pk>/', views.enquiry_followup, name='enquiry_followup'),
    path('payment/<str:pk>/', views.payment, name='payment'),
    path('enquiry_search/', views.enquiry_search, name='enquiry_search'),
    path('details/', views.details, name='details'),
    path('payment_search/', views.payment_search, name='payment_search'),
    path('registration/', views.registration, name='registration'),

]
