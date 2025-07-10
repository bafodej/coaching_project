"""Vues spécifiques aux clients"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from ..models import Seance
from ..forms import PriseRendezVousForm
import datetime

@login_required
def dashboard_client(request):
    """Tableau de bord client avec ses rendez-vous"""
    # Récupérer les RDV futurs du client
    mes_rdv_futurs = Seance.objects.filter(
        client=request.user,
        date__gte=timezone.now().date()
    ).order_by('date', 'heure_debut')
    
    # Récupérer l'historique des séances passées
    historique = Seance.objects.filter(
        client=request.user,
        date__lt=timezone.now().date()
    ).order_by('-date', '-heure_debut')[:5]
    
    context = {
        'mes_rdv_futurs': mes_rdv_futurs,
        'historique': historique
    }
    return render(request, 'appointments/dashboard_client.html', context)

@login_required
def prendre_rendez_vous(request):
    """Vue pour la prise de rendez-vous"""
    if request.method == 'POST':
        form = PriseRendezVousForm(request.POST)
        if form.is_valid():
            if _verifier_disponibilite_creneau(form.cleaned_data):
                # Sauvegarder le rendez-vous
                seance = form.save(commit=False)
                seance.client = request.user
                seance.save()

                date = form.cleaned_data['date']
                heure_debut = form.cleaned_data['heure_debut']
                messages.success(
                    request, 
                    f"Votre rendez-vous du {date.strftime('%d/%m/%Y')} "
                    f"à {heure_debut.strftime('%H:%M')} a été confirmé !"
                )
                return redirect('dashboard')
            else:
                messages.error(
                    request, 
                    "Ce créneau n'est pas disponible. Veuillez choisir un autre horaire."
                )
    else:
        form = PriseRendezVousForm()

    # Récupérer les rendez-vous existants pour affichage
    rendez_vous_existants = Seance.objects.filter(
        date__gte=timezone.now().date()
    ).order_by('date', 'heure_debut')

    context = {
        'form': form,
        'rendez_vous_existants': rendez_vous_existants
    }
    return render(request, 'appointments/prise_rdv.html', context)

def _verifier_disponibilite_creneau(cleaned_data):
    """Fonction utilitaire pour vérifier la disponibilité d'un créneau"""
    date = cleaned_data['date']
    heure_debut = cleaned_data['heure_debut']
    duree = cleaned_data['duree']

    # Calculer l'heure de fin du nouveau RDV
    debut_datetime = datetime.datetime.combine(date, heure_debut)
    fin_datetime = debut_datetime + datetime.timedelta(minutes=duree)

    # Vérifier les conflits existants
    seances_meme_jour = Seance.objects.filter(date=date)
    
    for seance_existante in seances_meme_jour:
        # Calculer l'heure de fin de la séance existante
        debut_existant = datetime.datetime.combine(
            seance_existante.date, 
            seance_existante.heure_debut
        )
        fin_existant = debut_existant + datetime.timedelta(
            minutes=seance_existante.duree
        )

        # Vérifier le chevauchement
        if (debut_datetime < fin_existant and fin_datetime > debut_existant):
            return False
    
    return True