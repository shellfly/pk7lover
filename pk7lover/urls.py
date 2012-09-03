from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login,logout
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pk7lover.views.home', name='home'),
    # url(r'^pk7lover/', include('pk7lover.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
                           url(r'^gallery/',include('gallery.urls')), 
                       url(r'^administrato/', include(admin.site.urls)),
                       url(r'^accounts/',include('accounts.urls')),
                       url(r'^albums/',include('albums.urls')),
                       url(r'^$','pk7lover.views.home',name='home'),
)

urlpatterns += patterns('',
                        
                        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': settings.MEDIA_ROOT}))

