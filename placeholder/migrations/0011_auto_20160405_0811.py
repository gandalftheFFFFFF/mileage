# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('placeholder', '0010_auto_20160404_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='fuel_type',
            field=models.CharField(default='PETROL', max_length=20, choices=[('DIESEL', 'Diesel'), ('ELECTRICITY', 'Electricity'), ('PETROL', 'Petrol')]),
        ),
        migrations.AlterField(
            model_name='milageinstance',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 5, 6, 11, 36, 2636, tzinfo=utc), verbose_name='Date (yyyy-mm-dd):'),
        ),
    ]
