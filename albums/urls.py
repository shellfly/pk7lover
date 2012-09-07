from django.conf.urls import patterns, include, url

urlpatterns = patterns('albums.views', 
                       url(r'^create/$','create'),
                       url(r'^setcover/(?P<id>\d+)','setcover'),
                       url(r'^photos/(?P<id>\d+)/$','show_photo'),
                       url(r'^photos/(?P<id>\d+)/delete/$','del_photo',name='7del_photo'),
                       url(r'^(?P<username>\w+)/(?P<album_id>\d+)/upload/$','upload',name='7upload_photo'),
                       url(r'^(?P<username>\w+)/(?P<album_id>\d+)/delete/$','del_album',name='7del_album'),
                       url(r'^\w+/(?P<album_id>\d+)/edit/$','edit'),
                       url(r'^\w+/(?P<album_id>\d+)/order/$','order'),
                       url(r'^(?P<username>\w+)/(?P<album_id>\d+)/$','album',name='single_album'),
                       url(r'^(?P<username>\w+)/$','albums',name='7albums'),                      
)
