from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.core.urlresolvers import reverse_lazy

app_name='meet' # so as to not confuse urls across different apps
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^login/$', auth_views.login, {'template_name': 'meet/login.html', 'authentication_form': LoginForm}, name="login"),
    url(r'^logout/$', auth_views.logout, {'next_page': reverse_lazy('meet:login')}),
]
