from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Seance
import datetime



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = "Obligatoire. 150 caractères maximum. Lettres, chiffres et @/./+/-/_ uniquement."
        self.fields['password1'].help_text = ""  # Supprime l'aide
        self.fields['password2'].help_text = "Saisissez le même mot de passe pour vérification."



class PriseRendezVousForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ['date', 'heure_debut', 'duree', 'objet']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-lime-500 focus:ring-lime-500 sm:text-sm',
                'min': datetime.date.today().strftime('%Y-%m-%d')
            }),
            'heure_debut': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-lime-500 focus:ring-lime-500 sm:text-sm',
                'step': '600'  # Pas de 10 minutes
            }),
            'duree': forms.Select(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-lime-500 focus:ring-lime-500 sm:text-sm'
            }),
            'objet': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-gray-300 shadow-sm focus:border-lime-500 focus:ring-lime-500 sm:text-sm',
                'placeholder': 'Ex: Gestion du stress, Confiance en soi...'
            })
        }
        labels = {
            'date': 'Date du rendez-vous',
            'heure_debut': 'Heure de début',
            'duree': 'Durée de la séance',
            'objet': 'Sujet de la séance'
        }
    
    def clean_date(self):
        """Valide que la date est dans le futur"""
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise ValidationError("Impossible de prendre un rendez-vous dans le passé.")
        return date
    
    def clean_heure_debut(self):
        """Valide les horaires autorisés"""
        heure = self.cleaned_data['heure_debut']
        
        # Horaires du coach : 9h-18h en semaine, 9h-12h le samedi
        if heure < datetime.time(9, 0) or heure > datetime.time(18, 0):
            raise ValidationError("Les rendez-vous sont possibles de 9h à 18h.")
        
        # Vérifier que l'heure est sur un créneau de 10 minutes
        if heure.minute % 10 != 0:
            raise ValidationError("Les rendez-vous doivent commencer sur un créneau de 10 minutes (ex: 9h00, 9h10, 9h20...).")
        
        return heure
    
    def clean(self):
        """Validations globales"""
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        heure_debut = cleaned_data.get('heure_debut')
        
        if date and heure_debut:
            # Vérifier les horaires selon le jour de la semaine
            if date.weekday() == 6:  # Dimanche
                raise ValidationError("Pas de rendez-vous le dimanche.")
            elif date.weekday() == 5:  # Samedi
                if heure_debut > datetime.time(12, 0):
                    raise ValidationError("Le samedi, les rendez-vous sont possibles jusqu'à 12h.")
        
        return cleaned_data