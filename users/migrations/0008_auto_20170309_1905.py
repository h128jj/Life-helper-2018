# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 19:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20170303_0430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractive',
            name='expire_date',
            field=models.DateTimeField(auto_created=datetime.datetime(2017, 3, 10, 19, 5, 10, 502331), verbose_name='Expire date'),
        ),
    ]