from django.db import models
from openpyxl import load_workbook
import os
from Mechanic_website import settings
import datetime
import pytz


class Schedule(models.Model):
    timestamp = models.DateTimeField()
    available = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)


class Booking(models.Model):
    time = models.DateTimeField(blank=False) #this needs to disappear as soon as i fix the datetime picker
    make = models.CharField(max_length=100, blank=False)
    model = models.CharField(max_length=100, blank=False)
    year = models.CharField(max_length=4, blank=False)
    fuel = models.CharField(max_length=20, blank=False)
    transmission = models.CharField(max_length=20, blank=False)
    category = models.CharField(max_length=40, blank=True, null=True)
    description = models.CharField(max_length=250, blank=False)
    name = models.CharField(max_length=20, blank=False)
    surname = models.CharField(max_length=20, blank=False)
    phone = models.CharField(max_length=20, blank=False)
    email = models.EmailField(max_length=254, blank=False, null=True)
    slot = models.ForeignKey(Schedule, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



def time_intervals():
    tz = pytz.timezone('Europe/Sofia')
    start = tz.localize(datetime.datetime(year=2021, month=1, day=1, hour=9, minute=0)) # new attempt to make it save proper time
    end = tz.localize(datetime.datetime(year=2031, month=1, day=31, hour=18, minute=0))
    delta = datetime.timedelta(minutes=60)

    while start <= end:
        yield start
        start += delta


# dts = [dt for dt in time_intervals() if 9 <= dt.hour <= 18]
#return start.strftime('%d-%m-%Y %H:%M'), end.strftime('%d-%m-%Y %H:%M')




def service_list():
    wb = load_workbook(os.path.join(settings.BASE_DIR, 'services_list.xlsx'))
    wb = wb.active
    services = {
        row[0].value: row[1].value
        for row in wb.rows
    }

    return services

# def populate_services():
#     services = service_list()
#     for service, description in services:
#         Service.objects.create(name=service, description=description)


