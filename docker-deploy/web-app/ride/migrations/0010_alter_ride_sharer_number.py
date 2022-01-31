# Generated by Django 4.0.1 on 2022-01-29 22:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0009_ride_sharer_number_alter_ride_vehicle_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='sharer_number',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)]),
        ),
    ]
