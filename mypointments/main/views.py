from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.views import View

from . import forms

# Create your views here.

def home(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'home.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return render(request, 'DafAdmin.html')
            elif user.get_user() == user.is_metupal:
                return render(request, 'DafMetupal')
            else:
                return render(request, 'Dafrofe')
    else:
        form = AuthenticationForm()
    return render(request, 'home.html', {'form': form})

def dafmetupal(request):
    return render(request, 'DafMetupal.html')

def dafadmin(request):
    return render(request, 'DafAdmin.html')

def signout(request):
    return render(request, 'login.html')
