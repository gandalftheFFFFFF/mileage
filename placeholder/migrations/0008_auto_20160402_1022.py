# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('placeholder', '0007_auto_20160401_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='date',
            field=models.DateField(verbose_name='Date (yyyy-mm-dd):'),
        ),
        migrations.AlterField(
            model_name='car',
            name='fuel_type',
            field=models.CharField(max_length=10, default='PETROL', choices=[('DIESEL', 'Diesel'), ('PETROL', 'Petrol'), ('ELECTRICITY', 'Electricity')]),
        ),
        migrations.AlterField(
            model_name='milageinstance',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=18, verbose_name='Fuel cost'),
        ),
        migrations.AlterField(
            model_name='milageinstance',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 2, 8, 22, 0, 447191, tzinfo=utc), verbose_name='Date (yyyy-mm-dd):'),
        ),
        migrations.AlterField(
            model_name='milageinstance',
            name='km_stand',
            field=models.DecimalField(decimal_places=2, max_digits=18, verbose_name='Km driven'),
        ),
        migrations.AlterField(
            model_name='milageinstance',
            name='liter',
            field=models.DecimalField(decimal_places=2, max_digits=18, verbose_name='Fuel volume'),
        ),
        migrations.AlterUniqueTogether(
            name='car',
            unique_together=set([('registration_no', 'user')]),
        ),
    ]
