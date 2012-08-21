from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login,logout
from django.template.context import RequestContext

urlpatterns = patterns('accounts.views', 
                       url(r'^profile/$','profile'),
                       url(r'^login/$','login'),
                       url(r'^logout/$','logout'),
                       url(r'^signup/$','signup'),
)
