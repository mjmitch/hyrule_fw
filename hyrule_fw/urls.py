from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from hyrule_fw.players import urls as PLAYER_URLS

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include(PLAYER_URLS))
)
