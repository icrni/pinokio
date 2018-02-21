# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-21 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0014_auto_20180221_0910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pid',
            name='labels',
        ),
        migrations.AddField(
            model_name='issues',
            name='labels',
            field=models.ManyToManyField(to='roadmap.PIDLabel'),
        ),
        migrations.AddField(
            model_name='issues',
            name='project',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='PID',
        ),
    ]
