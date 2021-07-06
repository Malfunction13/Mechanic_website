from django.contrib import messages
from django.core import mail
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import BookingForm, UpdateForm, SearchBookingForm
from .models import Booking, Schedule
import pytz
import datetime
from Mechanic_website.settings import TIME_ZONE, DEFAULT_FROM_EMAIL


def booking(request):
    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            ts = form.cleaned_data['timestamp']  # a date object
            hour = form.cleaned_data['hour']  # a string
            ts_booking = local_datetime(ts, hour, TIME_ZONE)
            ts_slot = utc_datetime(ts_booking)

            # this will be difficult to break by user input because the hours cannot be manually inserted, only picked
            slot = Schedule.objects.get(timestamp=ts_slot)  # Schedule object for requested slot
            if slot.available:

                slot.available = False  # change the field's value to False
                slot.save()
                new_booking = Booking(time=ts_booking,
                                      make=form.cleaned_data['make'],
                                      model=form.cleaned_data['model'],
                                      year=form.cleaned_data['year'],
                                      fuel=form.cleaned_data['fuel'],
                                      transmission=form.cleaned_data['transmission'],
                                      category=form.cleaned_data['category'],
                                      description=form.cleaned_data['description'],
                                      name=form.cleaned_data['name'],
                                      surname=form.cleaned_data['surname'],
                                      phone=form.cleaned_data['phone'],
                                      email=form.cleaned_data['email'],
                                      slot=slot)

                new_booking.save()
                booking_created_email(new_booking)  # sends email confirmation
            else:

                print("HANDLE SLOT TAKEN ERROR")  # THE USER SHOULD GET A NOTIFICATION "THIS SLOT IS TAKEN"

        return redirect('booking-complete')

    else:

        form = BookingForm()

        if request.is_ajax():
            hours = get_hours(request, BookingForm)

            return JsonResponse({'hours': hours}, status=200)

        return render(request, 'booking/booking.html', {'my_form': form})


def booking_complete(request):
    return render(request, 'booking/booking_confirm.html')


def search(request):
    form = SearchBookingForm(request.GET)  # needs to be loaded with request.GET info to validate submission

    if form.is_valid():

        try:
            booking = Booking.objects.get(id=form.cleaned_data['booking_id'])
            request.session['booking_id'] = booking.id  # avoiding overhead on object serialization & just pass ID

            return redirect('booking-update')

        except ObjectDoesNotExist:
            messages.error(request, message="The booking was not found!")
    else:
        form = SearchBookingForm()
    return render(request, 'booking/booking_search.html', {'form': form})


def update(request):
    booking = Booking.objects.get(id=request.session['booking_id'])  # make use of the ID passed in session by search()
    update_form = UpdateForm()
    if request.method == "POST":

        update_form = UpdateForm(request.POST)  # load with req dictionary containing the submitted data

        if update_form.is_valid():
            slot = Schedule.objects.get(id=booking.slot.id)
            slot.available = True  # first free up current slot
            slot.save()
            ts = update_form.cleaned_data['timestamp']
            hour = update_form.cleaned_data['hour']

            ts_booking = local_datetime(ts, hour, TIME_ZONE)  # construct a localized datetime obj from date and hour
            ts_slot = utc_datetime(ts_booking)

            new_slot = Schedule.objects.get(timestamp=ts_slot)
            new_slot.available = False  # occupy new slot
            new_slot.save()

            booking.time = ts_booking
            booking.slot = new_slot

            for field in update_form.cleaned_data:

                if field not in ['timestamp', 'hour']:
                    setattr(booking, field, update_form.cleaned_data[field])

            booking.save()
            booking_updated_email(booking)  # sends email confirmation

            return redirect('home')

    else:
        update_form = BookingForm(initial={
            "timestamp": booking.time,
            "hour": "",
            "make": booking.make,
            "model": booking.model,
            "year": booking.year,
            "fuel": booking.fuel,
            "transmission": booking.transmission,
            "description": booking.description,
            "name": booking.name,
            "surname": booking.surname,
            "phone": booking.phone,
            "email": booking.email,
        })

        update_form.fields['hour'].choices = ((i, i) for i in update_form.available_hours())

        if request.is_ajax():
            hours = get_hours(request, UpdateForm)

            return JsonResponse({'hours': hours}, status=200)

    return render(request, 'booking/booking_update.html', {'my_form': update_form})


def delete_confirm(request):
    return render(request, 'booking/delete_confirm.html', )


def delete_complete(request):
    booking = Booking.objects.get(id=request.session['booking_id'])
    slot = Schedule.objects.get(id=booking.slot.id)
    slot.available = True
    slot.save()
    booking.delete()

    booking_deleted_email(booking)

    return render(request, 'booking/delete_complete.html', )


"""Email helpers"""


def booking_created_email(booking):
    subject = "Booking confirmation"
    message = render_to_string('booking/email/booking_created.html', {'booking': booking})
    to = booking.email
    mail.send_mail(subject, message=message, html_message=message, from_email=DEFAULT_FROM_EMAIL, recipient_list=[to],
                   fail_silently=False)


def booking_updated_email(booking):
    subject = "Booking update confirmation"
    message = render_to_string('booking/email/booking_updated.html', {'booking': booking})
    to = booking.email
    mail.send_mail(subject, message=message, html_message=message, from_email=DEFAULT_FROM_EMAIL, recipient_list=[to],
                   fail_silently=False)


def booking_deleted_email(booking):
    subject = "Booking cancellation confirmation"
    message = render_to_string('booking/email/booking_deleted.html')
    to = booking.email
    mail.send_mail(subject, message=message, html_message=message, from_email=DEFAULT_FROM_EMAIL, recipient_list=[to],
                   fail_silently=False)


""" Helper functions"""


def local_datetime(date_object, hour, timezone):
    """ Takes a date object from the form, an hour str eg '09:00' and a pytz timezone class string.
        Returns a datetime object with tzinfo=instance of a pytz object.
        The date/hour remain unchanged, only a proper timezone is added.
        Absolutely necessary for proper DST info."""

    ts = datetime.date.strftime(date_object, '%d-%m-%Y')
    local_tz = pytz.timezone(timezone)  # a pytz object
    ts = f"{ts} {hour}"  # datetime string in proper format to create a datetime object
    ts_localized = local_tz.localize(datetime.datetime.strptime(ts, "%d-%m-%Y %H:%M"))  # in local tz

    return ts_localized


def utc_datetime(ts_localized):
    """ Takes a localized datetime object and returns a datetime converted to UTC.
        The new object has changed time and new tzinfo.
        Absolutely necessary for proper DST info."""

    ts_utc = ts_localized.astimezone(pytz.timezone('UTC'))  # localize in UTC to match the slots in DB(always in UTC)

    return ts_utc


def get_hours(request, form):  # form is a class that will be instantiated
    date = request.GET.get('date')

    new_form = form(data={"timestamp": date})
    hours = new_form.available_hours()  # the Form class itself has a method to fetch the available hours for the day

    return hours
