# -*- coding: utf-8 -*-
# Generated by Django 1.11.dev20170103185511 on 2017-01-17 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meet', '0002_auto_20170116_2326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='questions_answered',
        ),
        migrations.AddField(
            model_name='profile',
            name='questions_answered',
            field=models.ManyToManyField(related_name='questions_answered', to='meet.Question'),
        ),
    ]
