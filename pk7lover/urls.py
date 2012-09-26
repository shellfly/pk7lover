from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login,logout
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^administrato/', include(admin.site.urls)),
                       url(r'^accounts/',include('accounts.urls')),
                       url(r'^albums/',include('albums.urls')),
                       url(r'^broadcast/',include('broadcast.urls')),
                       url(r'^activity/',include('activity.urls')),
                       url(r'^browse/$','pk7lover.views.browse'),
                       url(r'^$','pk7lover.views.home',name='home'),                   
)

urlpatterns += patterns('',
                        (r'^comments/', include('django.contrib.comments.urls')),
                        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': settings.MEDIA_ROOT}))

