__author__ = 'Joshua Moravec'
from django.conf.urls import patterns, include, url
from django.contrib import admin
from RadNet import views

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^AddData/$', views.add_data, name='addData'),
                       url(r'^AddFilter/$', views.add_filter, name='addFilter'),
                       url(r'^AddCoefficients/$', views.add_coefficients, name='addCoeff'),
                       url(r'^AddCoefficients/(?P<type_id>\d+)/$', views.add_coefficients),
                       )
