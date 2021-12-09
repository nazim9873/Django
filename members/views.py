from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegisterUserForm


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.success(request, ("Username or password is incorrect"))
            return render(request, 'members/login.html')
    return render(request, 'members/login.html')

    # Create your views here.


def logout_user(request):
    logout(request)
    messages.success(request, ("Logged out successfully"))
    return redirect('/members/login_user')


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Username or password is incorrect"))
            return redirect('/')
    else:
        form = RegisterUserForm()
    return render(request, 'members/register.html', {'form': form})
