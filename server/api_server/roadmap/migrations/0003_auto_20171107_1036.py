# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-07 10:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0002_auto_20171107_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='issues',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
