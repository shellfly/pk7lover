from django.conf.urls import patterns, include, url

urlpatterns = patterns('accounts.views', 
                       url(r'^profile/$','profile',name='7profile'),
                       url(r'^login/$','login'),
                       url(r'^logout/$','logout'),
                       url(r'^signup/$','signup'),
                       url(r'^confirm/$','confirm'),
                       url(r'^(?P<username>\w+)/$','people',name='7people'),
                       url(r'^eyeon/(?P<username>\w+)/$','eyeon',name="accounts_eyeon")
)
