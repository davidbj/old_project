from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^images.html$', 'caas.apps.caas.views.images'),
	url(r'^container.html$', 'caas.apps.caas.views.container'),
	url(r'^form_container.html$', 'caas.apps.caas.views.form_container'),
    url(r'^$', 'caas.apps.caas.views.images'),
)
