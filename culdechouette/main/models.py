from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid


class Game(models.Model):
    # id field is by default the primary key. no need to create it
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(null=True)
    isActive =  models.BooleanField(null=True)
    isFull = models.BooleanField(null=True)
    winner = models.ForeignKey(User,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Play(models.Model):
    IDGame = models.ForeignKey(Game,on_delete=models.CASCADE)
    IDPlayer = models.ForeignKey(User,on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = (("IDGame", "IDPlayer"),)
