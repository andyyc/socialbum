from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(User)
