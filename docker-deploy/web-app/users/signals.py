from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from ride.models import Ride
from users.models import Users


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        User.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Ride)
def create_ride(sender, instance, **kwargs):
    post_save.disconnect(create_ride, sender=sender)
    carType = instance.vehicle_type
    if carType == 'X':
        canCarry = 3
    else:
        canCarry = 5
    instance.seat_available = canCarry - instance.passenger_number
    instance.save()
    post_save.connect(create_ride, sender=sender)


@receiver(post_save, sender=Users)
def syn_vehicle_capacity(sender, instance, **kwargs):
    post_save.disconnect(syn_vehicle_capacity, sender=sender)
    carType = instance.vehicle_type
    if carType == 'X':
        canCarry = 3
    else:
        canCarry = 5
    instance.vehicle_capacity = canCarry
    instance.save()
    post_save.connect(syn_vehicle_capacity, sender=sender)
