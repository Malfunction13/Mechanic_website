from django.contrib import admin
from .models import Booking, Schedule
from django import forms

admin.site.register(Booking)
admin.site.register(Schedule)
#
# class BookingAdminForm(forms.ModelForm):
#     fields = "__all__"
#
#     def set_slot(self):
#         pass
#
#
# @admin.site.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     form = BookingAdminForm
