from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',views.HomeView.as_view(), name='home'),
    path('create/',views.CreateView.as_view(),name='create'),
    path('game/<str:room_name>/', login_required(views.GameView.get_view), name='game')

]