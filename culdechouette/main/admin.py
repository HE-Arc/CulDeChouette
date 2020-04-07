from django.contrib import admin
from .models import Game
from .models import Play


# Register your models here.
admin.site.register(Game)
admin.site.register(Play)