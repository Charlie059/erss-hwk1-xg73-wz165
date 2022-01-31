from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from users.models import Users


class Ride(models.Model):
    OPEN = "OPEN"
    STATUS_CHOICES = (
        ("OPEN", "OPEN"),
        ("CONFIRMED", "CONFIRMED"),
        ("COMPLETE", "COMPLETE"),
    )
    X = 'X'
    XL = 'XL'
    CAR_CHOICES = [
        (X, 'X(3 passengers)'),
        (XL, 'XL(5 passengers)'),
    ]
    # Ride().owner = ?
    # Users().related_name = ride
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="rider_owner")
    driver = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="rider_driver", null=True)
    starting_location = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    share = models.BooleanField(default=False)
    arrive_date = models.DateTimeField(help_text='Format: 2022-01-01 12:00')
    special_request = models.CharField(max_length=200)
    vehicle_type = models.CharField(max_length=20, choices = CAR_CHOICES, default = X)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=OPEN)
    who_on_car = models.ManyToManyField(Users)
    passenger_number = models.IntegerField(default = 1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    seat_available = models.IntegerField(default = -1)
    # def __str__(self):
    #     return self.owner

    def get_absolute_url(self):
        return reverse('ride:ride-detail', kwargs={'pk': self.pk})
