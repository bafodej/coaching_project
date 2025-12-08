from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

class Seance(models.Model):
    DUREE_CHOICES = [
        (60, '1 heure'),
        (90, '1h30'),
        (120, '2 heures'),
    ]
    
    # Champs obligatoires selon le cahier des charges
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seances')
    date = models.DateField(verbose_name="Date du rendez-vous")
    heure_debut = models.TimeField(verbose_name="Heure de début")
    objet = models.CharField(max_length=200, verbose_name="Objet de la séance", 
                            help_text="Ex: Gestion du stress, Confiance en soi...")
    
    # Champs additionnels utiles
    duree = models.IntegerField(choices=DUREE_CHOICES, default=60, verbose_name="Durée")
    notes_coach = models.TextField(blank=True, null=True, verbose_name="Notes du coach",
                                help_text="Notes privées, non visibles par le client")
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'heure_debut']
        verbose_name = "Séance"
        verbose_name_plural = "Séances"
        # Contrainte : un client ne peut pas avoir 2 RDV au même moment
        unique_together = ['client', 'date', 'heure_debut']
    
    def __str__(self):
        return f"{self.client.username} - {self.date} à {self.heure_debut} ({self.objet})"
    
    @property
    def heure_fin(self):
        """Calcule l'heure de fin de la séance"""
        if self.date and self.heure_debut:  #  Vérification ajoutée
            debut = datetime.datetime.combine(self.date, self.heure_debut)
            fin = debut + datetime.timedelta(minutes=self.duree)
            return fin.time()
        return None
    
    def clean(self):
            """Validation des contraintes métier"""
            if self.date and self.heure_debut:
                # Empêcher les RDV dans le passé
                maintenant = timezone.now()
                seance_datetime = datetime.datetime.combine(self.date, self.heure_debut)
                if timezone.make_aware(seance_datetime) <= maintenant:
                    raise ValidationError("Impossible de prendre un rendez-vous dans le passé.")
