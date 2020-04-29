from django.shortcuts import render
from django.core import serializers
import json

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    user = serializers.serialize('json',[request.user,],fields=('id','username'))
    struct = json.loads(user)
    user = json.dumps(struct[0])
    #user = request.user
    return render(request, 'chat/room.html', {
        'room_name': room_name,'user':user
    })