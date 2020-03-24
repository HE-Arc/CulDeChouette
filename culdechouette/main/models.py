from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Game(models.Model):
    # id field is by default the primary key. no need to create it
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    isActive =  models.BooleanField()
    isFull = models.BooleanField()
    winner = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Play(models.Model):
    IDGame = models.ForeignKey(Game,on_delete=models.CASCADE)
    IDPlayer = models.ForeignKey(User,on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = (("IDGame", "IDPlayer"),)