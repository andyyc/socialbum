from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from game.models import Game, Player
from django.contrib.auth.models import User

class PlayerResource(ModelResource):
    class Meta:
        queryset = Player.objects.all()
        resource_name = 'player'

class GameResource(ModelResource):
    winner = fields.ForeignKey(PlayerResource, 'winner')

    class Meta:
        queryset = Game.objects.all()
        resource_name = 'game'
        authorization= Authorization()
