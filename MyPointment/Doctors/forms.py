from django import forms
from booking.models import Appointment

class ExampleForm(forms.Form):
    time_taken = forms.CharField(max_length=10)
    
    