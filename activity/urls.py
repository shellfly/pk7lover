from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('activity.views',
                       url(r'^create/$','create',name="7create_activity"),
                       url(r'^(?P<activity_id>\d+)/$','activity',name='7activity'),
                       url(r'^(?P<activity_id>\d+)/delete/$','delete',name='7delete_activity'),
                       url(r'^(?P<activity_id>\d+)/anticipate/$','anticipate',name='7anticipate'),
                       url(r'^photos/(?P<id>\d+)/vote$','vote',name='7vote'),
                       url(r'^photos/(?P<id>\d+)/$','show',name='7show'),
                       url(r'^$','activities',name="7activities"),
                       
)
