from django.conf.urls import patterns, include, url

urlpatterns = patterns('albums.views', 
                       url(r'^create/$','create'),
                       url(r'^(?P<username>\w+)/(?P<album_id>\d+)/$','album'),
                       url(r'^(?P<username>\w+)/$','albums'),                      
)
