from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^login/', 'facebook.views.login', name='login'),
    url(r'^logout/', 'facebook.views.logout_view', name='logout'),
)
