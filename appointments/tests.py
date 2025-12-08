from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, time, timedelta
from .models import Seance


class SeanceModelTest(TestCase):
    
    def setUp(self):
        """Créer un utilisateur de test"""
        self.user = User.objects.create_user(
            username='testclient',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_seance_creation(self):
        """Test de création d'une séance valide"""
        demain = date.today() + timedelta(days=1)
        seance = Seance.objects.create(
            client=self.user,
            date=demain,
            heure_debut=time(10, 0),
            objet="Gestion du stress",
            duree=60
        )
        self.assertEqual(seance.client, self.user)
        self.assertEqual(seance.objet, "Gestion du stress")
        self.assertEqual(seance.duree, 60)
    
    def test_seance_str_representation(self):
        """Test de la représentation string"""
        demain = date.today() + timedelta(days=1)
        seance = Seance.objects.create(
            client=self.user,
            date=demain,
            heure_debut=time(14, 30),
            objet="Confiance en soi",
            duree=90
        )
        expected = f"testclient - {demain} à 14:30:00 (Confiance en soi)"
        self.assertEqual(str(seance), expected)
    
    def test_heure_fin_calculation(self):
        """Test du calcul de l'heure de fin"""
        demain = date.today() + timedelta(days=1)
        seance = Seance.objects.create(
            client=self.user,
            date=demain,
            heure_debut=time(10, 0),
            objet="Test",
            duree=90  # 1h30
        )
        # 10h00 + 1h30 = 11h30
        self.assertEqual(seance.heure_fin, time(11, 30))
    
    def test_cannot_create_past_appointment(self):
        """Test qu'on ne peut pas créer un RDV dans le passé"""
        hier = date.today() - timedelta(days=1)
        seance = Seance(
            client=self.user,
            date=hier,
            heure_debut=time(10, 0),
            objet="Test passé",
            duree=60
        )
        with self.assertRaises(ValidationError):
            seance.full_clean()
    
    def test_unique_appointment_per_client(self):
        """Test qu'un client ne peut pas avoir 2 RDV au même moment"""
        demain = date.today() + timedelta(days=1)
        
        # Créer le premier RDV
        Seance.objects.create(
            client=self.user,
            date=demain,
            heure_debut=time(10, 0),
            objet="Premier RDV",
            duree=60
        )
        
        # Tenter de créer un second RDV au même moment
        with self.assertRaises(Exception):  # IntegrityError en pratique
            Seance.objects.create(
                client=self.user,
                date=demain,
                heure_debut=time(10, 0),
                objet="Doublon",
                duree=60
            )
    
    def test_default_duree(self):
        """Test de la durée par défaut (60 minutes)"""
        demain = date.today() + timedelta(days=1)
        seance = Seance.objects.create(
            client=self.user,
            date=demain,
            heure_debut=time(15, 0),
            objet="Test durée défaut"
        )
        self.assertEqual(seance.duree, 60)
