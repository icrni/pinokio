# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-21 18:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadmap', '0016_issues_linked_issues'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='cost',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
