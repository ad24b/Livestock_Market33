from django.shortcuts import render

# Create your views here.

# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm

def register_view(response):
    if response.method == 'POST':
        form = UserRegistrationForm(response.POST)
        if form.is_valid():
            #user = form.save()
            #login(request, user)
            form.save()
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(response,'users/register.html', {'form': form})

def login_view(response):
    if response.method == 'POST':
        form = UserLoginForm(data=response.POST)
        if form.is_valid():
            user = form.get_user()
            login(response, user)
            return redirect('/')
    else:
        form = UserLoginForm()
    return render(response, 'users/login.html', {'form': form})

def logout_view(response):
    logout(response)
    return redirect('login')


#@login_required
def home_view(response):
    return render(response,'users/home.html',)