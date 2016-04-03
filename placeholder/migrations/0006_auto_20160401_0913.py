# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('placeholder', '0005_auto_20160401_0907'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Expenses',
            new_name='Expense',
        ),
        migrations.AddField(
            model_name='car',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 4, 1, 7, 13, 54, 813376, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='milageinstance',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 1, 7, 13, 31, 395479, tzinfo=utc), verbose_name='Dato (yyyy-mm-dd):'),
        ),
    ]
