from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import DateTimeField, DateTimeInput

User = get_user_model()
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class Become2DriverForm(forms.ModelForm):
    CAR_CHOICES = (
        ('X', 'X(3 passengers)'),
        ('XL', 'XL(5 passengers)'),
    )

    vehicle_type = forms.ChoiceField(widget=forms.Select, choices=CAR_CHOICES)
    vehicle_number = forms.CharField()
    vehicle_capacity = forms.IntegerField()
    special_info = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['vehicle_type', 'vehicle_number', 'vehicle_capacity', 'special_info']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'image']


class SearchShareRideFrom(forms.Form):
    destination = forms.CharField(max_length=100)
    earliest_arrive_time = DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
    )
    latest_arrive_time = DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
    )
    num_Of_Passenger = forms.IntegerField()


# TODO ShareUpdateRideFrom
class ShareUpdateRideFrom(forms.Form):
    num_Of_Passenger = forms.IntegerField(help_text="Update number of passages group included yourself")

