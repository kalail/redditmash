from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rankings/$', 'redditmash.views.rankings'),
    url(r'^$', 'redditmash.views.index'),
)
