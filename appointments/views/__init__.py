"""Package des vues - Imports pour maintenir la compatibilité avec les URLs"""
from .auth_views import signup, logout_view
from .client_views import dashboard_client, prendre_rendez_vous
from .coach_views import dashboard_coach, gestion_clients, tous_les_rdv
from .public_views import accueil, index

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """Vue principale qui redirige selon le rôle utilisateur"""
    if request.user.is_superuser:
        return dashboard_coach(request)
    else:
        return dashboard_client(request)