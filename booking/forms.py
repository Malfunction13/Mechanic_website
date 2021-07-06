from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from .models import Schedule
import datetime
import pytz


class BookingForm(forms.Form):
    timestamp = forms.DateField(initial=datetime.date.today,
                                widget=DatePickerInput(
                                format='%d-%m-%Y',
                                options={
                                        "showClose": True,
                                        "showTodayButton": True,
                                        'locale': 'bg'}
                                    )
                                )
    hour = forms.ChoiceField(choices=[(1, 1)])
    make = forms.CharField(max_length=100)
    model = forms.CharField(max_length=100)
    year = forms.CharField(max_length=4)
    fuel = forms.CharField(max_length=20)
    transmission = forms.CharField(max_length=20)
    category = forms.CharField(max_length=40, required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 13.1em;'}), max_length=250)
    name = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=254)

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['hour'] = forms.ChoiceField(choices=[(i, i) for i in self.available_hours()])

    def available_hours(self):  # a datetime object
        if type(self['timestamp'].value()) != str:  # initially the data is date object
            day = Schedule.objects.filter(timestamp__date=self["timestamp"].value(),
                                          available=True)

        else:  # however when the view instantiates the form with request.POST info it turns into a str
            # so string parsing is required
            converted_date = datetime.datetime.strptime(self["timestamp"].value(), "%d-%m-%Y")
            day = Schedule.objects.filter(timestamp__date=converted_date, available=True)

        slots_utc = [slot.timestamp for slot in day]
        slots_local = [slot.astimezone(pytz.timezone("Europe/Sofia")) for slot in slots_utc]  # localize to Sofia time
        hours = [f"{slot.hour}:00" if slot.hour > 9 else f"0{slot.hour}:00" for slot in slots_local]  # str options

        return hours


class UpdateForm(BookingForm):
    # contains same fields as the BookingForm and initial data is loaded by the view that calls UpdateForm

    pass


class SearchBookingForm(forms.Form):
    booking_id = forms.IntegerField(label="Your booking ID")
