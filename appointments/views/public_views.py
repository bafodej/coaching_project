"""Vues publiques accessibles à tous"""
from django.shortcuts import render

def accueil(request):
    """Page d'accueil du site"""
    return render(request, 'appointments/accueil.html')

def index(request):
    """Vue index (alias de accueil)"""
    return render(request, 'appointments/accueil.html')