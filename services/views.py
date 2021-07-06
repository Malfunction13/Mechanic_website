from django.views.generic import ListView, DetailView
from .models import Service


class ServiceListView(ListView):
    model = Service


class ServiceDetailView(DetailView):
    model = Service
    slug_field = 'name'  # the name of the field we will look up in the model
    slug_url_kwarg = 'name'  # the keyword we will look to replace in the url
