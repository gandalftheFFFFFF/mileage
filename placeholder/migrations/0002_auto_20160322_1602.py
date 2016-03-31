# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('placeholder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milageinstance',
            name='date',
            field=models.DateTimeField(verbose_name='Dato (yyyy-mm-dd):', default=datetime.datetime(2016, 3, 22, 16, 2, 30, 233792)),
        ),
    ]
