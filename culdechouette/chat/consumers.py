import json
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

        diceSum = sum(diceList)
        if d1 == d2 == d3:
            # Cul de chouette
            print("Cul de chouette")
        elif d1 == d2 or d1 == d3 or d2 == d3:
            
            if max(diceList)*2 == diceSum:
                # Chouette velute
                print("Chouette velute")
            else : 
                #chouette
                print("chouette")
        elif d1 + d2 == d3:
            # velutte
            print("velutte")
        elif d1+1 == d2 and d1+2 == d3:
            # suite
            print("suite")


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


        if self.room_name not in ChatConsumer.active_player:
            ChatConsumer.active_player[self.room_name] = 0

        if self.room_name not in ChatConsumer.users:
            ChatConsumer.users[self.room_name] = []

        if self.room_name not in ChatConsumer.dices:
            ChatConsumer.dices[self.room_name] = []    

        ChatConsumer.users[self.room_name].append(str(self.scope['user']))

        await self.update()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        ChatConsumer.users[self.room_name].remove(str(self.scope['user']))

        await self.update()

    async def update(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'config_message',
                'message': json.dumps(ChatConsumer.users[self.room_name]),
                'active_player': ChatConsumer.users[self.room_name][ChatConsumer.active_player[self.room_name]]
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
        if type == "game_message" :
            ChatConsumer.dices[self.room_name] = []
            ChatConsumer.active_player[self.room_name] = (ChatConsumer.active_player[self.room_name] + 1) % len(ChatConsumer.users[self.room_name])
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

        if ChatConsumer.dices[self.room_name] == []:
            ChatConsumer.dices[self.room_name] = [randrange(1,6), randrange(1,6), randrange(1,6)]
            GameController.evaluateThrow(ChatConsumer.dices[self.room_name])

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type' : "game_message",
            'message': "throw_dices",
            'dices': ChatConsumer.dices[self.room_name]
        }))
        
  
    async def config_message(self, event):
        message = event['message']
        active_player = event['active_player']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type' : "config_message",
            'message': message,
            'active_player': active_player
        }))

