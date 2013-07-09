from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^create/', 'game.views.create', name='create_game'),
    url(r'^(?P<game_id>\d+)/$', 'game.views.game', name='game'),
    url(r'^$', 'game.views.games', name='games'),
    url(r'^(?P<game_id>\d+)/turn/(?P<turn_id>\d+)/$', 'game.views.turn', name='turn'),
)
