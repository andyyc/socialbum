from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=64)
    users = models.ManyToManyField(User, through="Player")
    current_turn = models.OneToOneField('Turn', related_name="+", null=True)

class Turn(models.Model):
    STATUSES = (
        (0, 'Started'),
        (1, 'Voting'),
        (2, 'Ended'),
    )

    game = models.ForeignKey(Game)
    num = models.PositiveSmallIntegerField()
    judge = models.ForeignKey(User)
    black_card = models.OneToOneField('BlackCard', null=True)
    winner = models.OneToOneField('Submission', null=True, related_name='+')
    status = models.PositiveSmallIntegerField(default=0, choices=STATUSES)

# Create your models here.
class BlackCardTmpl(models.Model):
    text = models.TextField()

class WhiteCardTmpl(models.Model):
    text = models.TextField()

class BlackCard(models.Model):
    STATUSES = (
        ('N', 'Not Available'),
        ('A', 'Available'),
    )
    card = models.ForeignKey(BlackCardTmpl)
    game = models.ForeignKey('Game')
    status = models.CharField(max_length=1, choices=STATUSES, default='A')

class WhiteCard(models.Model):
    STATUSES = (
        ('P', 'Played'),
        ('D', 'Discarded'),
        ('U', 'Unused'),
    )
    card = models.ForeignKey(WhiteCardTmpl)
    game = models.ForeignKey('Game')
    user = models.ForeignKey(User, null=True)
    turn = models.ForeignKey(Turn, null=True)
    status = models.CharField(max_length=1, choices=STATUSES, default='U')

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
