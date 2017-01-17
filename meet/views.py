# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from django.db.models import F, Count

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import Choice, Question, Survey, Vote, Profile

"""
ListView displays a list of objects
DetailView displays a detail page for a particular type of object
The model attribute tells the generic view what model it will be acting upon
DetailView expects the primary key value captured by the url to be called pk, so this is what we use in urls.py
"""
def latest_survey_list():
    current_surveys = Survey.objects.filter(pub_date__lte=timezone.now())
    to_delete = []
    for survey in current_surveys:
        # filter out questions with no answers
        for question in survey.question_set.all():
            if not len(question.choice_set.all()) > 1:
                to_delete.append(question.id)
                break

    Question.objects.filter(id__in=to_delete).delete()

    return Survey.objects.annotate(count=Count('question')).filter(pub_date__lte=timezone.now(), count__gt=0).order_by('-pub_date')[:10] # make sure surveys have > 0 questions

class IndexView(generic.ListView):
    template_name = 'meet/index.html'
    context_object_name = 'latest_survey_list'

    def get_queryset(self):
        """
        Return the last ten published questions, not including those set to be published in the future.
        """
        self.question_id= self.kwargs.get('question_id') # gives the id of the question we're returning from
        return latest_survey_list()

class DetailView(generic.DetailView):
    model = Survey
    template_name = 'meet/detail.html'
    # default template name would be meet/survey_detail.html

    def get_queryset(self):
        """
        Excludes any future questions
        """
        return Question.objects.filter(survey__pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'meet/results.html'


def vote(request, question_id):
    print("voting!")
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.

        return render(request, 'meet/index.html', {
            'latest_survey_list': latest_survey_list(),
            'question_id': int(question_id), # must convert to int to correctly display error message
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.num_votes = F('num_votes') + 1
        vote = Vote(choice=selected_choice, question=question, voter=request.user.profile)
        vote.save()
        profile = request.user.profile
        profile.vote_set.add(vote)
        profile.save()
        selected_choice.save()
        return HttpResponseRedirect(reverse('meet:index', kwargs={'question_id': question_id,}))

"""
==========================================================
GROUPS AND PERMISSIONS
==========================================================
"""
# supers = Group(name="Supers")
# Supers have ability to eliminate comments or questions that are inappropriate

# content_type = ContentType.objects.get_for_model(Survey)
# can_delete = Permission.objects.create(
#     codename='can_delete',
#     name='Can Delete Surveys',
#     content_type=content_type,
# )

# supers.permissions.add(can_delete)
# when a user has a certain amount of activity or upvotes on their comments, add them to this Group
# e.g. in a view: user = request.user ... user.groups.add(supers)
