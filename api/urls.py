from django.conf.urls.defaults import patterns, include, url
from tastypie.api import Api
from api import GameResource, PlayerResource

v1_api = Api(api_name='v1')
v1_api.register(PlayerResource())
v1_api.register(GameResource())

urlpatterns = patterns('',
  (r'', include(v1_api.urls)),
)
