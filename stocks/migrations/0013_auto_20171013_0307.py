# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-13 03:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0012_auto_20171013_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmentstockconfiguration',
            name='quantity',
            field=models.FloatField(),
        ),
    ]
