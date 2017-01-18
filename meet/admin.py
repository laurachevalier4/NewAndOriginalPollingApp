# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from .models import Question, Profile, Choice, Survey, Vote, User

class ChoiceInline(NestedStackedInline):
    model = Choice
    extra = 3

class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    inlines = [ChoiceInline]

class SurveyAdmin(NestedModelAdmin):
    class Media:
        css = {
            "all": ("admin/style.css",)
        }

    fieldsets = [
        ('Date information', {'fields': ('pub_date', 'end_date', 'owner')}),
    ]
    inlines = [QuestionInline]
    # Choice objects are edited on the Question admin page. Provide enough fields for 3 choices.

    list_display = ('owner', 'pub_date', 'end_date', 'was_published_recently')
    list_filter = ['pub_date', 'owner']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'question':
            kwargs["queryset"] = Question.objects.filter(survey_id=request.id)
        return super(SurveyAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class VoteInline(admin.TabularInline):
    model = Vote
    extra = 3

class ProfileAdmin(admin.ModelAdmin):
    model = Profile

    inlines = [VoteInline]

    fieldsets = [
        ('User', {'fields': ['user']}),
        ('Basic Info', {'fields': ('city', 'country', 'birth_date', 'gender', 'marital_status')}),
        ('Career Info', {'fields': ('education_level', 'industry', 'income')}),
        ('Extra', {'fields': ['social_media_sites']}),
        ('Activity', {'fields': ['points']})
    ]

    list_display = ('user', 'points')

# class UserAdmin(NestedModelAdmin):
#     inlines = [ProfileInline]

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Profile, ProfileAdmin)
