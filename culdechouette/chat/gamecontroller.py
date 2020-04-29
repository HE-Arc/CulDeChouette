

from main.models import Play
from main.models import Game
from django.contrib.auth.models import User

from channels.db import database_sync_to_async

class GameController():

    def evaluateThrow(diceList):

        diceList.sort()
        d1 = diceList[0]
        d2 = diceList[1]
        d3 = diceList[2]
        score =0
        diceSum = sum(diceList)

        flag = 0

        if d1 == d2 == d3:
            # Cul de chouette
            score = 40 + 10*d1
            flag = 1
        elif d1 == d2 or d1 == d3 or d2 == d3:
            
            if max(diceList)*2 == diceSum:
                # Chouette velute -> pas mou le caillou
                score = 2*d3*d3
                flag = 2
            else : 
                #chouette
                score = d2*d2
                flag = 3
        elif d1+1 == d2 and d1+2 == d3:
            # suite -> Grelote ça picote
            score = -10
            flag = 5
        elif d1 + d2 == d3:
            # velutte
            score = 2*d3*d3
            flag = 4
        else:
            flag = -1
        return score, flag

    @database_sync_to_async
    def endOfGame(self,winner,players,room_name):
        game = Game.objects.get(id=room_name)
        winner = User.objects.get(username=winner.name)
        game.winner = winner
        game.isActive = False
        game.save()
        for player in players:            
            p = Play(IDGame=game,IDPlayer=User.objects.get(username=player.name),score=player.score)
            p.save()

    @database_sync_to_async
    def getStatus(self, room_name):
        game = Game.objects.get(id=room_name)
        return game.isActive

