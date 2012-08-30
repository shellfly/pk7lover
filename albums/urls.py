from django.conf.urls import patterns, include, url

urlpatterns = patterns('albums.views', 
                       url(r'^create/$','create'),
                       url(r'^\w+/(?P<album_id>\d+)/upload/$','upload'),
                       url(r'^\w+/(?P<album_id>\d+)/edit/$','edit'),
                       url(r'^\w+/(?P<album_id>\d+)/order/$','order'),
                       url(r'^\w+/(?P<album_id>\d+)/$','album'),
                       url(r'^upload_image/$','upload_image'),
                       url(r'^\w+/$','albums'),                      
)
