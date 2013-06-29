from django.db import models

# Create your models here.
import simplejson
import urllib
from django.contrib.auth.models import User

class FacebookSessionError(Exception):
    def __init__(self, error_type, message):
        self.message = message
        self.type = error_type
    def get_message(self):
        return self.message
    def get_type(self):
        return self.type
    def __unicode__(self):
        return u'%s: "%s"' % (self.type, self.message)

class FacebookSession(models.Model):

    access_token = models.CharField(max_length=255, unique=True)
    expires = models.IntegerField(null=True)

    user = models.ForeignKey(User, null=True)
    uid = models.BigIntegerField(unique=True, null=True)

    def picture_url(self):
        return "http://graph.facebook.com/" + str(self.uid) + "/picture"

    class Meta:
        unique_together = (('user', 'uid'), ('access_token', 'expires'))

    def query(self, object_id, connection_type=None, metadata=False):

        url = 'https://graph.facebook.com/%s' % (object_id)
        if connection_type:
            url += '/%s' % (connection_type)

        params = {'access_token': self.access_token}
        if metadata:
            params['metadata'] = 1

        url += '?' + urllib.urlencode(params)
        response = simplejson.load(urllib.urlopen(url))
        if 'error' in response:
            error = response['error']
            raise FacebookSessionError(error['type'], error['message'])
        return response

    def get_facebook_profile(self):
        fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % self.access_token)
        return simplejson.load(fb_profile)

    def get_friends(self):
        fb_friends = urllib.urlopen('https://graph.facebook.com/me/friends?access_token=%s' % self.access_token)
        return simplejson.load(fb_friends)