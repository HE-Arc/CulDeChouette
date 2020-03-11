from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from .models import Game
from django.views import generic, View


# Create your views here.
class HomeView(generic.TemplateView):
    template_name = 'main/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = Game.objects.all()
        return context
