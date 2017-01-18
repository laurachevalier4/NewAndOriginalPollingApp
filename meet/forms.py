from django.contrib.auth.forms import AuthenticationForm
from django.forms.extras.widgets import SelectDateWidget
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from registration.forms import RegistrationForm

import datetime

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
