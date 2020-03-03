from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views import View



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
