# -*- coding: utf-8 -*-
# Generated by Django 1.11.dev20170103185511 on 2017-01-17 14:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meet', '0006_remove_choice_votes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='votes',
        ),
        migrations.AlterField(
            model_name='vote',
            name='voter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meet.Profile'),
        ),
    ]