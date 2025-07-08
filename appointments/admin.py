from django.contrib import admin
from .models import Seance

@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
    list_display = ['client', 'date', 'heure_debut', 'duree', 'objet']
    list_filter = ['date', 'duree']
    search_fields = ['client__username', 'objet']
    ordering = ['date', 'heure_debut']
  