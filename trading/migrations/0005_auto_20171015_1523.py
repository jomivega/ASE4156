# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-15 15:23
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0004_auto_20170920_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='quantity',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0, message='Daily stock quote can not be negative')]),
        ),
    ]
