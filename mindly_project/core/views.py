from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@login_required(login_url='login')
def home(request):
    return render(request, 'core/home.html')

@login_required(login_url='login')
def registo_humor(request):
    return render(request, 'core/registo_humor.html')

@login_required(login_url='login')
def diario_digital(request):
    return render(request, 'core/diario_digital.html')

@login_required(login_url='login')
def exercicios(request):
    return render(request, 'core/exercicios.html')

@login_required(login_url='login')
def album(request):
    return render(request, 'core/album.html')

@login_required(login_url='login')
def feeling(request):
    return render(request, 'core/feeling.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})
