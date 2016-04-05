# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('placeholder', '0009_auto_20160402_2349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='milageinstance',
            name='date',
            field=models.DateTimeField(verbose_name='Date (yyyy-mm-dd):', default=datetime.datetime(2016, 4, 4, 7, 26, 19, 214963, tzinfo=utc)),
        ),
    ]
