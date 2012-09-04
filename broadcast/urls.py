from django.conf.urls import patterns, include, url


urlpatterns = patterns('broadcast.views',
                       url(r'^say/$','say',name='7broadcast_say'),
)
