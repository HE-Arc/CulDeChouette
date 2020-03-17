from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Game(models.Model):
    # id field is by default the primary key. no need to create it
    name = models.CharField(max_length=100)
    date = models.DateTimeField(null=True)
    isActive =  models.BooleanField(null=True)
    isFull = models.BooleanField(null=True)
    winner = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
