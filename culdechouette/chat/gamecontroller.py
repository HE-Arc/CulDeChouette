

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
            print("Cul de chouette")
            score = 40 + 10*d1
            flag = 1
        elif d1 == d2 or d1 == d3 or d2 == d3:
            
            if max(diceList)*2 == diceSum:
                # Chouette velute -> pas mou le caillou
                print("Chouette velute")
                score = 2*d3*d3
                flag = 2
            else : 
                #chouette
                print("chouette")
                score = d2*d2
                flag = 3
        elif d1 + d2 == d3:
            # velutte
            print("velutte")
            score = 2*d3*d3
            flag = 4
        elif d1+1 == d2 and d1+2 == d3:
            # suite -> Grelote ça picote
            print("suite")
            score = -10
            flag = 5
        else:
            print("néant")
            flag = -1
        return score, flag

    @database_sync_to_async
    def endOfGame(self,winner,players,room_name):
        for player in players:
            game = Game.objects.get(id=room_name)
            winner = User.objects.get(username=winner.name)
            game.winner = winner
            game.isActive = False
            game.save()
            p = Play(IDGame=game,IDPlayer=User.objects.get(username=player.name),score=player.score)
            p.save()