# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('placeholder', '0003_auto_20160331_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milageinstance',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 1, 6, 24, 25, 851861, tzinfo=utc), verbose_name='Dato (yyyy-mm-dd):'),
        ),
    ]
