from django.urls import path
from .views import ServiceListView, ServiceDetailView


urlpatterns = [
    path('', ServiceListView.as_view(), name='service_list'),
    path('<str:name>/', ServiceDetailView.as_view(), name='service-detail'),
]
