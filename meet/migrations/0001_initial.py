# -*- coding: utf-8 -*-
# Generated by Django 1.11.dev20170103185511 on 2017-01-09 01:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=150)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(verbose_name='date commented')),
                ('marked_inappropriate', models.BooleanField(default=False)),
                ('upvotes', models.IntegerField(default=0)),
                ('downvotes', models.IntegerField(default=0)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=200)),
                ('city', models.CharField(blank=True, max_length=30)),
                ('country', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('company', models.CharField(blank=True, max_length=50, null=True)),
                ('marital_status', models.CharField(blank=True, choices=[('S', 'Single'), ('M', 'Married'), ('D', 'Dating'), ('C', "It's complicated")], max_length=1, null=True)),
                ('education_level', models.IntegerField(blank=True, choices=[(1, 'Less than high school'), (2, 'High school diploma or equivalent'), (3, 'Some college, no degree'), (4, "Associate's degree"), (5, "Bachelor's degree"), (6, "Master's degree"), (7, 'Doctoral or professional degree')], null=True)),
                ('industry', models.CharField(blank=True, max_length=30)),
                ('income', models.CharField(blank=True, max_length=40, null=True)),
                ('social_media_sites', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('FB', 'Facebook'), ('TW', 'Twitter'), ('IN', 'Instagram'), ('LI', 'LinkedIn'), ('SN', 'Snapchat'), ('TU', 'Tumblr'), ('PI', 'Pinterest'), ('GO', 'Google+'), ('YO', 'Youtube'), ('RE', 'Reddit'), ('ME', 'Meetup')], max_length=22)),
                ('points', models.IntegerField(default=0)),
                ('num_questions_answered', models.IntegerField(default=0)),
                ('num_questions_asked', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('end_date', models.DateTimeField(verbose_name='date ended')),
                ('category', multiselectfield.db.fields.MultiSelectField(choices=[('Entmt', 'Entertainment'), ('Food', 'Food'), ('Nat', 'Nature'), ('Poli', 'Politics'), ('PandS', 'Products and Services'), ('Reltn', 'Relationships'), ('Sci', 'Science'), ('Tech', 'Tech'), ('Trav', 'Travel'), ('O', 'Other')], max_length=25)),
                ('tags', models.CharField(max_length=80)),
                ('reward_value', models.IntegerField(default=1)),
                ('allow_comments', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meet.Question')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meet.Survey'),
        ),
        migrations.AddField(
            model_name='profile',
            name='questions_answered',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='meet.Question'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meet.Survey'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meet.Question'),
        ),
    ]
