from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def accueil(request):
    return render(request, 'appointments/accueil.html')

def index(request):
    return render(request, 'appointments/accueil.html')



def signup(request):
    """
    Formulaire d'inscription de la page singin,
    renvoi vers le dashboard ou vers un nouveau formuaire 
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):  # ← Ajoutez cette fonction
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