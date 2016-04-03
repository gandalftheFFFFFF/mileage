# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('placeholder', '0008_auto_20160402_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='milageinstance',
            name='car',
            field=models.ForeignKey(default=1, to='placeholder.Car'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='milageinstance',
            name='date',
            field=models.DateTimeField(verbose_name='Date (yyyy-mm-dd):', default=datetime.datetime(2016, 4, 2, 21, 49, 28, 289653, tzinfo=utc)),
        ),
    ]
