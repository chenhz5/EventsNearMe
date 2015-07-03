from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
from djangoRestAPI import views



urlpatterns = patterns('',    
    url(r'^showEvents/', include('polls.urls', namespace="polls")),
    url(r'^event/(?P<inputParams>.*)$', views.getEvents, name = 'getEvents')
)
