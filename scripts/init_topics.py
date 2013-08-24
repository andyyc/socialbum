import sys
import os

sys.path.append(os.path.join('/vagrant/app'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'socialbum.settings'

from game.models import Topic

#for i in xrange(0,20):
#    Topic.objects.create(text="topic" + str(i))

f = open('topics.txt', 'r')

for topic in f:
    Topic.objects.create(text=topic.strip())


"""
Topic.objects.create(text="Why can't I sleep at night?")
Topic.objects.create(text="What's that smell?")
Topic.objects.create(text="I got 99 problems but ___ ain't one")
Topic.objects.create(text="What's the next happy meal toy?")
Topic.objects.create(text="What ended my last relationship?")
Topic.objects.create(text="I drink to forget ___")
Topic.objects.create(text="What is batman's guilty pleasure?")
Topic.objects.create(text="What's a girl's best friend?")
Topic.objects.create(text="What does dick cheney prefer?")
Topic.objects.create(text="White people like ___")
Topic.objects.create(text="During sex, I like to think about ___")
Topic.objects.create(text="What are my parents hiding from me?")
Topic.objects.create(text="What will always get you laid?")
Topic.objects.create(text="What did I bring back from mexico?")
Topic.objects.create(text="What don't you want to find in your chinese food?")
Topic.objects.create(text="What will I bring back in time to convince everybody I am a wizard?")
Topic.objects.create(text="What's my secret power?")
Topic.objects.create(text="What gives me uncontrollable gas?")
Topic.objects.create(text="What do old people smell like?")
Topic.objects.create(text="Why am I sticky?")
Topic.objects.create(text="What gets better with age?")
Topic.objects.create(text="What am I giving up for lent?")
Topic.objects.create(text="Why do I hurt all over?")
Topic.objects.create(text="What never fails to liven up the party?")
Topic.objects.create(text="Instead of coal, Santa now gives bad children ___")
Topic.objects.create(text="Friends who eat all the snacks")
Topic.objects.create(text="Crystal meth")
Topic.objects.create(text="College")
Topic.objects.create(text="Flying sex snakes")
Topic.objects.create(text="Being a motherfucking sorcerer")
"""