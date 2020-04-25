from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User

from main.models import Play
from main.models import Game


class Register(View):
    def post(self,request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account successfuly created ! ')
            return redirect('login')
        return render(request,'users/register.html',{'form':form})


    def get(self,request):
        form = UserCreationForm()
        return render(request,'users/register.html',{'form':form})

class ProfileView(View):
    def get(self,request):
        current_user = request.user
        plays = Play.objects.select_related('IDGame').filter(IDPlayer=current_user)
        return render(request,'users/profile.html',{'user':current_user,'plays':plays})