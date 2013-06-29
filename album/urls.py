from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^create/', 'album.views.create_album', name='create_album'),
)