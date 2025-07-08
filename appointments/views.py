from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, PriseRendezVousForm
from django.contrib.auth.decorators import login_required
from .models import Seance

def accueil(request):
    return render(request, 'appointments/accueil.html')

def index(request):
    return render(request, 'appointments/accueil.html')



def signup(request):
    """ formulaire """
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
    logout(request)
    return redirect('accueil')

@login_required
def dashboard(request):
    if request.user.is_superuser:
        # Coach dashboard
        return render(request, 'appointments/dashboard_coach.html')
    else:
        # Client dashboard  
        return render(request, 'appointments/dashboard_client.html')
    

@login_required
def prendre_rendez_vous(request):
    """Vue pour la prise de rendez-vous"""
    if request.method == 'POST':
        form = PriseRendezVousForm(request.POST)
        if form.is_valid():
            # Vérifier les conflits d'horaires avant de sauvegarder
            date = form.cleaned_data['date']
            heure_debut = form.cleaned_data['heure_debut']
            duree = form.cleaned_data['duree']
            
            # Calculer l'heure de fin
            import datetime
            debut_datetime = datetime.datetime.combine(date, heure_debut)
            fin_datetime = debut_datetime + datetime.timedelta(minutes=duree)
            heure_fin = fin_datetime.time()
            
            # Vérifier les chevauchements avec d'autres RDV
            conflits = Seance.objects.filter(
                date=date,
                heure_debut__lt=heure_fin,
                heure_fin__gt=heure_debut
            ).exclude(pk=form.instance.pk if form.instance.pk else None)
            
            if conflits.exists():
                messages.error(request, "Ce créneau n'est pas disponible. Veuillez choisir un autre horaire.")
            else:
                # Sauvegarder le rendez-vous
                seance = form.save(commit=False)
                seance.client = request.user
                seance.save()
                
                messages.success(request, f"Votre rendez-vous du {date.strftime('%d/%m/%Y')} à {heure_debut.strftime('%H:%M')} a été confirmé !")
                return redirect('dashboard')
    else:
        form = PriseRendezVousForm()
    
    # Récupérer les rendez-vous existants pour affichage (optionnel)
    rendez_vous_existants = Seance.objects.filter(
        date__gte=datetime.date.today()
    ).order_by('date', 'heure_debut')
    
    context = {
        'form': form,
        'rendez_vous_existants': rendez_vous_existants
    }
    return render(request, 'appointments/prise_rdv.html', context)