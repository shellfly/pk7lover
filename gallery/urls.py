from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('gallery.views',
                       url(r'^$','index'),
)