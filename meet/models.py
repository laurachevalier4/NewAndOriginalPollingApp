# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from multiselectfield import MultiSelectField

"""
TODO:
- Add friends -- private vs. public surveys and the ability to see how your friends answered
- Add ability to postpone the survey being added to the archives
"""

class Survey(models.Model):
    CATEGORY_CHOICES=(
    ('Entmt', 'Entertainment'),
    ('Food', 'Food'),
    ('Nat', 'Nature'),
    ('Poli', 'Politics'),
    ('PandS', 'Products and Services'),
    ('Reltn', 'Relationships'),
    ('Sci', 'Science'),
    ('Tech', 'Tech'),
    ('Trav', 'Travel'),
    ('O', 'Other')
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE) # many different surveys can be linked to the same owner
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended') # survey should disappear after the end date passes
    category = MultiSelectField(max_length=25,choices=CATEGORY_CHOICES, blank=False)
    tags = models.CharField(max_length=80)
    reward_value = models.IntegerField(default=1) # base it on number of questions and add more if companies pay more
    allow_comments = models.BooleanField(default=False)

    def num_questions(self):
        # count number of questions whose survey id's are the same; if the number is 1, it will count as a single question
        # Question.objects.filter(survey__id=self.id).count()
        return self.question_set.count()

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE) # many different questions can be linked to the same survey
    question_text = models.CharField(max_length=200)
    # add field to categorize questions into surveys (or single-question surveys)

    def num_votes(self):
        return self.vote_set.count()

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # if the question is deleted, the choice will be deleted
    choice_text = models.CharField(max_length=150)
    num_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Comment(models.Model):
    pub_date = models.DateTimeField('date commented')
    marked_inappropriate = models.BooleanField(default=False) # give admins ability to mark comments appropriate
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    text = models.CharField(max_length=200)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Profile(models.Model):
    """
    profile info and activity
    access values in templates in views with user.profile.thing
    Generally speaking, you will never have to call the Profile's save method; everything is done through the User model (https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone)
    """
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('O', 'Other'))
    SOCIAL_MEDIA_CHOICES = (
    ('FB', 'Facebook'),
    ('TW', 'Twitter'),
    ('IN', 'Instagram'),
    ('LI', 'LinkedIn'),
    ('SN', 'Snapchat'),
    ('TU', 'Tumblr'),
    ('PI', 'Pinterest'),
    ('GO', 'Google+'),
    ('YO', 'Youtube'),
    ('RE', 'Reddit'),
    ('ME', 'Meetup'))
    MARITAL_STATUS_CHOICES = (
    ('S', 'Single'),
    ('M', 'Married'),
    ('D', 'Dating'),
    ('C', "It's complicated"))
    EDUCATION_LEVEL_CHOICES = (
    (1, 'Less than high school'),
    (2, 'High school diploma or equivalent'),
    (3, 'Some college, no degree'),
    (4, "Associate's degree"),
    (5, "Bachelor's degree"),
    (6, "Master's degree"),
    (7, "Doctoral or professional degree")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200, blank=True)
    city = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True) #can only choose 1
    company = models.CharField(max_length=50, blank=True, null=True)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    education_level = models.IntegerField(choices=EDUCATION_LEVEL_CHOICES, null=True, blank=True)
    industry = models.CharField(max_length=30, blank=True) # make student an option
    # potentially sensitive info is optional
    income = models.CharField(max_length=40, blank=True, null=True)
    social_media_sites = MultiSelectField(choices=SOCIAL_MEDIA_CHOICES, max_length=22, blank=True) # can choose any number of choices

    # keep track of user activity for rewards
    points = models.IntegerField(default=0)
    num_questions_answered = models.IntegerField(default=0)
    num_questions_asked = models.IntegerField(default=0)
    # votes = models.ManyToManyField(Vote, related_name="votes") # many different users can answer the same question... but also a user can answer many different questions (*SHOULD PROBS BE MANY TO MANY)
    # questions_asked = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True, related_name="questions_asked")

"""
The next two functions are linked to the User model whenever a save event occurs (post_save)
"""
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True) # many different votes linked to the same choice
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    voter = models.ForeignKey(Profile, on_delete=models.CASCADE) # many different votes linked to the same voter
