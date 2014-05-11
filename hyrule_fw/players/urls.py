from django.conf.urls import patterns, url

from views import *

urlpatterns = patterns('',
    url(r'^$', ViewPlayerList.as_view()),
    url(r'^ranks/$', ViewRankList.as_view()),
    url(r'^ranks/([\w-]+)/$', ViewRank.as_view()),
    url(r'^players/([\w-]+)/$', ViewPlayer.as_view()),
)