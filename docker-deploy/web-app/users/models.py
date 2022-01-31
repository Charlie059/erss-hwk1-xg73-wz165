from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image

class Users(AbstractUser):
    X = 'X'
    XL = 'XL'
    CAR_CHOICES = [
        (X, 'X(3 passengers)'),
        (XL, 'XL(5 passengers)'),
    ]

    vehicle_type = models.CharField(max_length=20, blank=True, default="",  choices = CAR_CHOICES)
    vehicle_number = models.CharField(max_length=20, blank=True, default="")
    vehicle_capacity = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(3), MaxValueValidator(5)])
    special_info = models.TextField(default="", blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

