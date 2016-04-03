# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('placeholder', '0004_auto_20160401_0624'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('registration_no', models.CharField(max_length=10)),
                ('price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('text', models.TextField(null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('amount', models.DecimalField(max_digits=9, decimal_places=2)),
                ('text', models.CharField(max_length=300)),
                ('comment', models.TextField(null=True, blank=True)),
                ('car', models.ForeignKey(to='placeholder.Car')),
            ],
        ),
        migrations.AlterField(
            model_name='milageinstance',
            name='date',
            field=models.DateTimeField(verbose_name='Dato (yyyy-mm-dd):', default=datetime.datetime(2016, 4, 1, 7, 7, 1, 745170, tzinfo=utc)),
        ),
    ]
