"""Vues spécifiques au coach"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Seance



@login_required
def dashboard_coach(request):
    """Tableau de bord coach avec statistiques et liste des clients"""
    # Statistiques générales
    nb_clients = User.objects.filter(is_superuser=False).count()
    nb_rdv_aujourd_hui = Seance.objects.filter(
        date=timezone.now().date()
    ).count()
    nb_rdv_semaine = Seance.objects.filter(
        date__gte=timezone.now().date(),
        date__lt=timezone.now().date() + timezone.timedelta(days=7)
    ).count()
    
    # Prochains rendez-vous
    prochains_rdv = Seance.objects.filter(
        date__gte=timezone.now().date()
    ).order_by('date', 'heure_debut')[:5]
    
    # Liste des clients (les 5 derniers inscrits)
    derniers_clients = User.objects.filter(
        is_superuser=False
    ).order_by('-date_joined')[:5]
    
    context = {
        'nb_clients': nb_clients,
        'nb_rdv_aujourd_hui': nb_rdv_aujourd_hui,
        'nb_rdv_semaine': nb_rdv_semaine,
        'prochains_rdv': prochains_rdv,
        'derniers_clients': derniers_clients,
    }
    return render(request, 'appointments/dashboard_coach.html', context)

@login_required
def gestion_clients(request):
    """Vue pour la gestion des clients (coach uniquement)"""
    if not request.user.is_superuser:
        return redirect('dashboard')

    clients_stats = _obtenir_statistiques_clients()
    
    return render(request, 'appointments/gestion_clients.html', {
        'clients_stats': clients_stats
    })

@login_required
def tous_les_rdv(request):
    """Vue pour voir tous les rendez-vous (coach uniquement)"""
    if not request.user.is_superuser:
        return redirect('dashboard')

    # Récupérer tous les RDV futurs
    rdv_futurs = Seance.objects.filter(
        date__gte=timezone.now().date()
    ).order_by('date', 'heure_debut')

    # Récupérer les RDV passés (optionnel)
    rdv_passes = Seance.objects.filter(
        date__lt=timezone.now().date()
    ).order_by('-date', '-heure_debut')[:10]  # Les 10 derniers

    return render(request, 'appointments/tous_les_rdv.html', {
        'rdv_futurs': rdv_futurs,
        'rdv_passes': rdv_passes
    })

def _obtenir_statistiques_clients():
    """Fonction utilitaire pour obtenir les statistiques des clients"""
    clients = User.objects.filter(is_superuser=False).order_by('username')
    clients_stats = []
    
    for client in clients:
        nb_seances = Seance.objects.filter(client=client).count()
        derniere_seance = Seance.objects.filter(
            client=client
        ).order_by('-date', '-heure_debut').first()
        
        clients_stats.append({
            'client': client,
            'nb_seances': nb_seances,
            'derniere_seance': derniere_seance
        })
    
    return clients_stats