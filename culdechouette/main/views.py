from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Game
from django.views import generic, View
import datetime
import json


# Create your views here.
class HomeView(generic.TemplateView):
    template_name = 'main/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = Game.objects.all()
        return context

class CreateView(CreateView):
    model = Game
    fields = ['name']

    def form_valid(self, form):
        model = form.save()
        model.date = datetime.datetime.now()
        model.isActive = True
        model.isFull = False
        model.save()
        return redirect('home')

class GameView(generic.TemplateView):
    template_name = 'main/game.html'

    def get_view(request, room_name): # TODO : make this standard ?
        user = serializers.serialize('json',[request.user,],fields=('id','username'))
        struct = json.loads(user)
        user = json.dumps(struct[0])
        return render(request, 'main/game.html', {
            'room_name': room_name,'user':user
        })
    