from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=64)
    users = models.ManyToManyField(User, through="Player")
    current_turn = models.OneToOneField('Turn', related_name="+", null=True)
    completed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    winner = models.OneToOneField('Player', null=True, related_name='+')

class Turn(models.Model):
    STATUSES = (
        (0, 'Choose Topic'),
        (1, 'Waiting Submissions / Select Winner'),
        (2, 'Turn End'),
    )

    game = models.ForeignKey(Game)
    num = models.PositiveSmallIntegerField()
    judge = models.ForeignKey(User)
    game_topic = models.OneToOneField('GameTopic', null=True)
    winner = models.OneToOneField('Submission', null=True, related_name='+')
    status = models.PositiveSmallIntegerField(default=0, choices=STATUSES)

# Create your models here.
class Topic(models.Model):
    text = models.TextField()
    deleted = models.BooleanField(default=False)

class GameTopic(models.Model):
    topic = models.ForeignKey(Topic)
    game = models.ForeignKey('Game')
    used = models.BooleanField(default=False)

class Submission(models.Model):
    clickX = models.TextField()
    clickY = models.TextField()
    clickDrag = models.TextField()
    clickColor = models.TextField()
    clickSize = models.TextField()
    player = models.ForeignKey('Player')
    turn = models.ForeignKey(Turn)

class Player(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    points = models.PositiveSmallIntegerField()
