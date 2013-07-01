from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^create/', 'game.views.create', name='create_game'),
)
