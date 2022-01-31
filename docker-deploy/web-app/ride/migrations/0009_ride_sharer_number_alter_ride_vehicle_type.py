# Generated by Django 4.0.1 on 2022-01-29 22:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0008_ride_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='sharer_number',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)]),
        ),
        migrations.AlterField(
            model_name='ride',
            name='vehicle_type',
            field=models.CharField(choices=[('X', 'X(3 passengers)'), ('XL', 'XL(5 passengers)')], default='X', max_length=20),
        ),
    ]
