# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('placeholder', '0002_auto_20160322_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milageinstance',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 31, 11, 10, 12, 260847), verbose_name=b'Dato (yyyy-mm-dd):'),
        ),
    ]
