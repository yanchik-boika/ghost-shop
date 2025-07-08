from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm

def home(request):
    return render(request, 'ghost/home.html')


def nike_men(request):
    return render(request, 'nike-men.html')

def nike_women(request):
    return render(request, 'nike-women.html')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'ghost/register.html', {'form': form})


from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'ghost/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
