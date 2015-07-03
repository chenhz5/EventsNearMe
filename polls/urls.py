from django.conf.urls import patterns, url
from polls import views

urlpatterns = patterns('',
        # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
)