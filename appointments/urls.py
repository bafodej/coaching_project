from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"), 
    path("logout/", views.logout_view, name="logout"),
    path("prendre-rdv/", views.prendre_rendez_vous, name="prendre_rdv"),  
    path("gestion-clients/", views.gestion_clients, name="gestion_clients"),  
    path("tous-les-rdv/", views.tous_les_rdv, name="tous_les_rdv"), 
]