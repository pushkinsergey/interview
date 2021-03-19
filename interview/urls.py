"""interview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
from rest_framework.authtoken.views import ObtainAuthToken
#from django.contrib import admin
from interviewapi import views
from interviewapi.serializers import UserSerializer
#from django.conf.urls import include

urlpatterns = [
    url(r'^api/list/$', views.PollList.as_view()),
    url(r'^api/poll/(?P<pk>[0-9]+)/$', views.PollEdit.as_view()),
    url(r'^api/poll/(?P<pk>[0-9]+)/question/$', views.QuestionList.as_view()),    
    url(r'^api/question/(?P<pk>[0-9]+)/$', views.QuestionEdit.as_view()),    
    url(r'^api/interview/$', views.Interviews.as_view()), 
    url(r'^api/interview/(?P<pk>[0-9]+)/$', views.Interviewing.as_view()),    
    url(r'^api-token-auth/', views.CustomAuthToken.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)


