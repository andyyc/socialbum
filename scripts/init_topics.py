import sys
import os

sys.path.append(os.path.join('/vagrant/app'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'socialbum.settings'

from game.models import Topic

for i in xrange(0,20):
    Topic.objects.create(text="topic" + str(i))

