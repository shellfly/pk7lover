from django.conf.urls import patterns, include, url

urlpatterns = patterns('albums.views', 
                       url(r'^create/$','create',name="7create_album"),
                       url(r'^photos/(?P<id>\d+)/setcover/$','setcover',name="7setcover"),
                       url(r'^photos/(?P<id>\d+)/$','show_photo',name='7single_photo'),
                       url(r'^photos/(?P<photo_id>\d+)/delete/$','del_photo',name='7del_photo'),
                       url(r'^(?P<album_id>\d+)/upload/$','upload',name='7upload_photo'),
                       url(r'^(?P<album_id>\d+)/delete/$','del_album',name='7del_album'),
                       url(r'^(?P<album_id>\d+)/edit/$','edit',name='7edit_photo'),
                       url(r'^(?P<album_id>\d+)/property/$','property',name='7property_photo'),
                       url(r'^(?P<album_id>\d+)/$','album',name='7single_album'),
                       url(r'^(?P<username>\w+)/$','albums',name='7albums'),                      
)
