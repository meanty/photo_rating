# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
# from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    url(r'create/$', views.CreateFormView.as_view(), name='create_form'),
    url(r'new_user/$', views.user_create, name='user_create'),
    url(r'vote/$', views.VotePage.as_view(), name='vote_page'),
    url(r'(?P<pk>\d+)/$', views.UserCard.as_view(), name='user-card'),
]

# router = DefaultRouter()
# router.register(r'vote', views.VoteSet)
# #router.register(r'vote/up', views.up_rating)
# urlpatterns += router.urls