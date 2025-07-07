from django.shortcuts import render

def accueil(request):
    return render(request, 'appointments/accueil.html')

def index(request):
    return render(request, 'appointments/accueil.html')