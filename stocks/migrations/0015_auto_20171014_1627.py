# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-14 16:27
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0014_auto_20171014_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmentbucketdescription',
            name='text',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(3, message='The description should at least be 3 characters long.')]),
        ),
    ]
