# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('placeholder', '0006_auto_20160401_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='fuel_type',
            field=models.CharField(max_length=10, choices=[('DIESEL', 'Diesel'), ('PETROL', 'Petrol'), ('ELECTRICITY', 'Electricity')], default='Petrol'),
        ),
        migrations.AlterField(
            model_name='milageinstance',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 1, 7, 43, 31, 978441, tzinfo=utc), verbose_name='Dato (yyyy-mm-dd):'),
        ),
    ]
