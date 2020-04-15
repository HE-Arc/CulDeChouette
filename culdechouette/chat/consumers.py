import json
from channels.generic.websocket import AsyncWebsocketConsumer
from random import randrange
from django.contrib.auth.models import User

class GameUser():
    def __init__(self, name, score):
        self.name = name
        self.score = score
    

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
                'message': json.dumps([user.name for user in ChatConsumer.users[self.room_name]]),
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


