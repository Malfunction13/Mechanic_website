from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking, name='booking'),
    path('success/', views.booking_complete, name='booking-complete'),
    path('search/', views.search, name='booking-search'),
    path('update/', views.update, name='booking-update'),
    path('delete/', views.delete_confirm, name='booking-delete-confirm'),
    path('delete/complete', views.delete_complete, name='booking-delete-complete'),
]
