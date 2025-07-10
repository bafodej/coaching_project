"""Vues liées à l'authentification"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from ..forms import CustomUserCreationForm

def signup(request):
    """Formulaire d'inscription"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    """Déconnexion utilisateur"""
    logout(request)
    return redirect('accueil')