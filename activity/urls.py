from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('activity.views',
                       url(r'^create/$','create',name="7create_activity"),

                       url(r'^$','activities',name="7activities"),
                       
)
