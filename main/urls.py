from django.conf.urls import patterns, include, url

urlpatterns = patterns('main.views', 
                       url(r'^signup/$','signup'),
                       url(r'^signin/$','signin'),
                       url(r'^$','index'),
)
