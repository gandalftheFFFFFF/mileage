# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MilageInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime(2016, 3, 21, 15, 56, 57, 507837), verbose_name='Dato (yyyy-mm-dd):')),
                ('km_stand', models.DecimalField(max_digits=18, decimal_places=2)),
                ('amount', models.DecimalField(max_digits=18, decimal_places=2)),
                ('liter', models.DecimalField(max_digits=18, decimal_places=2)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
