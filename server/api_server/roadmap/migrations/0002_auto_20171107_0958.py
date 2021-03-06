# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-07 09:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issues',
            name='assignee',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='issues',
            name='end_date',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='issues',
            name='epic_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='issues',
            name='issue_type',
            field=models.CharField(default='bug', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='issues',
            name='start_date',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='issues',
            name='status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
