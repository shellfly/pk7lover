from django.conf.urls import patterns, include, url

urlpatterns = patterns('albums.views', 
                       url(r'^create/$','create',name="7create_album"),
                       url(r'^setcover/(?P<id>\d+)','setcover',name="7setcover"),
                       url(r'^photos/(?P<id>\d+)/$','show_photo',name='7single_photo'),
                       url(r'^photos/(?P<photo_id>\d+)/delete/$','del_photo',name='7del_photo'),
                       url(r'^(?P<username>\w+)/(?P<album_id>\d+)/upload/$','upload',name='7upload_photo'),
                       url(r'^(?P<username>\w+)/(?P<album_id>\d+)/delete/$','del_album',name='7del_album'),
                       url(r'^(?P<username>\w+)/(?P<album_id>\d+)/edit/$','edit',name='7edit_photo'),
                       url(r'^\w+/(?P<album_id>\d+)/property/$','property',name='7property_photo'),
                       url(r'^(?P<username>\w+)/(?P<album_id>\d+)/$','album',name='7single_album'),
                       url(r'^(?P<username>\w+)/albums$','albums',name='7albums'),                      
)
