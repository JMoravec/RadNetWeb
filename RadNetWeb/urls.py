from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'RadNet.views.home', name='home'),
                       url(r'^Data/', include('RadNet.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^accounts/', include('allauth.urls')),
                       )
