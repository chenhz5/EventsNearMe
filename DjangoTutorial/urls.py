from django.conf.urls import patterns, include, url
from EventAggregator import views



urlpatterns = patterns('',    
    url(r'^showEvents/', include('polls.urls', namespace="polls")),
    url(r'^event/(?P<inputParams>.*)$', views.getEvents, name = 'getEvents')
)
