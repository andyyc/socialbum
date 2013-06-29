from socialbum import settings
import urllib2, urllib
import simplejson

class FbGraph:
    def __init__(self, access_token=None):
        self.access_token = access_token

    def get_url(self, path='', include_access_token=True, **params):
        api_base_url = settings.FACEBOOK_GRAPH_URI
        if self.access_token is not None and include_access_token:
            params['access_token'] = self.access_token
        url = '%s%s?%s' % (api_base_url, path, urllib.urlencode(params))
        return url

    def request(self, path='', post_data=None, include_access_token=True, **params):
        url = self.get_url(path, include_access_token=include_access_token, params=params)
        response = self._request(url, post_data)
        return response

    @classmethod
    def _request(cls, url, post_data=None):
        data = urllib2.urlopen(url)
        return simplejson.load(data)