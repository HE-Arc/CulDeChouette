import json
from json import JSONEncoder
from channels.generic.websocket import AsyncWebsocketConsumer
from random import randrange
from django.contrib.auth.models import User
#from gamecontroller import GameController

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


class GameUser():
    def __init__(self, name, score):
        self.name = name
        self.score = score

class GameUserEncoder(JSONEncoder):
    def default(self,o):
        return o.__dict__
    

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        if not hasattr(ChatConsumer, 'users'):
            ChatConsumer.users = {}
        if not hasattr(ChatConsumer, 'active_player'):
            ChatConsumer.active_player = {}
        if not hasattr(ChatConsumer, 'dices'):
            ChatConsumer.dices = {}
        if not hasattr(ChatConsumer, 'caillou'):
            ChatConsumer.caillou = {}
        if not hasattr(ChatConsumer, 'grelotte'):
            ChatConsumer.grelotte = {}
        if not hasattr(ChatConsumer, 'change'):
            ChatConsumer.change = {}


        if self.room_name not in ChatConsumer.active_player:
            ChatConsumer.active_player[self.room_name] = 0

        if self.room_name not in ChatConsumer.users:
            ChatConsumer.users[self.room_name] = []

        if self.room_name not in ChatConsumer.dices:
            ChatConsumer.dices[self.room_name] = []    

        if self.room_name not in ChatConsumer.caillou:
            ChatConsumer.caillou[self.room_name] = 0    

        if self.room_name not in ChatConsumer.change:
            ChatConsumer.change[self.room_name] = True    

        ChatConsumer.users[self.room_name].append(GameUser(str(self.scope['user']), 0))

        await self.update()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        users = ChatConsumer.users[self.room_name]

        [users.pop(i) for i in range(len(users)) if users[i].name == str(self.scope['user'])]

        ChatConsumer.active_player[self.room_name] = (ChatConsumer.active_player[self.room_name] + 1) % len(ChatConsumer.users[self.room_name])
        
        await self.update()

    async def update(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'config_message',
                'message': json.dumps(ChatConsumer.users[self.room_name], cls=GameUserEncoder),
                'active_player': ChatConsumer.users[self.room_name][ChatConsumer.active_player[self.room_name]].name
            }
        )   

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        type = text_data_json['type']


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': type,
                'message': message
            }
        )

        if ChatConsumer.change[self.room_name]: ChatConsumer.active_player[self.room_name] = (ChatConsumer.active_player[self.room_name] + 1) % len(ChatConsumer.users[self.room_name])

        ChatConsumer.dices[self.room_name] = []

        print(ChatConsumer.change[self.room_name])    
        await self.update()

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type' : "chat_message",
            'message': message
        }))

    # Receive message from room group
    async def game_message(self, event):
        message = event['message']
        if message == "throw_dices" and ChatConsumer.change[self.room_name]:
            if ChatConsumer.dices[self.room_name] == []:
                ChatConsumer.dices[self.room_name] =  [2,2,4]#[randrange(1,6), randrange(1,6), randrange(1,6)]
                
                score, flag = GameController.evaluateThrow(ChatConsumer.dices[self.room_name])
                if flag != 2 and flag != 5:                    
                    ChatConsumer.users[self.room_name][ChatConsumer.active_player[self.room_name]].score += score
                elif flag == 2:
                    ChatConsumer.change[self.room_name] = False
                    ChatConsumer.caillou[self.room_name] = score
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'type' : "game_message",
                'message': "throw_dices",
                'dices': ChatConsumer.dices[self.room_name]
            }))
        else:
            if message == "caillou":
                if ChatConsumer.caillou[self.room_name] > 0:
                    for user in ChatConsumer.users[self.room_name]:
                        if user.name == str(self.scope['user']):
                            user.score += ChatConsumer.caillou[self.room_name]
                    ChatConsumer.caillou[self.room_name] = 0
                    ChatConsumer.change[self.room_name] = True
            if message == "grelotte":
                pass


  
    async def config_message(self, event):
        message = event['message']
        active_player = event['active_player']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type' : "config_message",
            'message': message,
            'active_player': active_player
        }))


