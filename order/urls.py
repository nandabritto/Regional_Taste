from django.contrib import admin
from django.urls import path
from . import views
from .views import CheckoutView

urlpatterns = [
    path('', views.order, name='order'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    
]
