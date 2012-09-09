from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_change,password_reset, password_reset_confirm

urlpatterns = patterns('accounts.views', 
                       url(r'^profile/$','profile',name='7profile'),          
                       url(r'^login/$','login'),
                       url(r'^logout/$','logout'),
                       url(r'^signup/$','signup'),
                       url(r'^update/$',password_change,
                           {'template_name':'accounts/password_change_form.html',
                            'post_change_redirect':'/accounts/profile/',
                            'current_app':'accounts',},
                           name="7passwd_change"),
                       url(r'^reset/$',password_reset,
                           {'template_name':'accounts/password_reset_form.html',
                           'post_reset_redirect':'/accounts/profile/',
                           'current_app':'accounts'},
                           name="7reset"),
                       url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                           password_reset_confirm,
                           {'template_name':'accounts/password_reset_email.html'},
                           name='password_reset_confirm'),
                       url(r'^confirm/$','confirm'),
                       url(r'^(?P<username>\w+)/$','people',name='7people'),
                       url(r'^eyeon/(?P<username>\w+)/$','eyeon',name="accounts_eyeon")
)
