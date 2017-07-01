# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.conf import settings
from django.conf.urls import include, url, static
from django.contrib import admin
from . import views
import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.init, name='clients_list'),
    url(r'^search/', views.search),
    url(r'^users/', include('app_userlist.urls')),
    url(r'^xlsx/$', views.xlsx),
    url(r'vote/(?P<pk>\d+)/$', views.vote),
] 
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()