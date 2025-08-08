from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
import os
from django.conf import settings
from django.dispatch import receiver
from django.shortcuts import redirect, render

STATUS = (
    ("Approuvé","Approuvé"),
    ("Rejeté","Rejeté"),
    ("En attente","En attente")
)

KYC_STATUS = (
    ("en_attente", "En attente"),
    ("valide", "Validée"),
    ("refuse", "Refusée"),
)

DISPONIBILITE = (
    ("Non","Non disponible"),
    ("Oui","Disponible")
)

def kyc_upload_path(instance, filename):
    return f"kyc/{instance.client.id}/{filename}"

class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    email = models.EmailField()
    telephone = models.IntegerField()
    password = models.CharField(max_length=100)

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if type(self).objects.filter(email=self.email).exclude(pk=self.pk).exists():
         raise ValueError("Un utilisateur avec cet email existe déjà.")
        if type(self).objects.filter(telephone=self.telephone).exclude(pk=self.pk).exists():
         raise ValueError("Un utilisateur avec ce numéro de téléphone existe déjà.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

class Admin(Utilisateur):
    niveau_acces = models.CharField(max_length=50, default='admin', editable=False)

class ServiceClient(Utilisateur):
    niveau_acces = models.CharField(max_length=50, default='service_client', editable=False)

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='client')
    nom = models.CharField(max_length=100, null=True, blank=True)
    prenoms = models.CharField(max_length=100, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.prenoms} {self.nom}"

class KYC(models.Model): 
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='kyc')
    date_naissance = models.DateField(null=True, blank=True)
    adresse = models.CharField(max_length=200, null=True, blank=True)
    cni = models.CharField(max_length=20, null=True, blank=True)
    document_identite = models.FileField(upload_to=kyc_upload_path, null=True, blank=True)
    selfie = models.ImageField(upload_to=kyc_upload_path, null=True, blank=True)
    statut = models.CharField(max_length=20, choices=KYC_STATUS, default="en_attente")
    date_validation = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"KYC {self.client.nom} {self.client.prenoms} - {self.get_statut_display()}"

class Validateur(Utilisateur):
    niveau_acces = models.CharField(max_length=50, default='validateur', editable=False)


class Crypto(models.Model):
    nom = models.CharField(max_length=100)
    sigle = models.CharField(max_length=10)
    valeur_sur_le_marche_fcfa = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    quantite_disponible = models.DecimalField(max_digits=20, decimal_places=10, default=0.00)
    min_achat_fcfa = models.DecimalField(max_digits=15, decimal_places=2, default=1000)
    max_achat_fcfa = models.DecimalField(max_digits=15, decimal_places=2, default=10000000)
    min_vente_fcfa = models.DecimalField(max_digits=15, decimal_places=2, default=1000)
    max_vente_fcfa = models.DecimalField(max_digits=15, decimal_places=2, default=10000000)
    image = models.ImageField(upload_to='crypto_images/', blank=True, null=True)
    deposit_address = models.CharField(max_length=255, blank=True, null=True, help_text="Adresse de dépôt pour cette crypto (pour les ventes)")

    def __str__(self):
        return f"{self.nom} ({self.sigle})"

class ConversionTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('BUY', 'Achat'),
        ('SELL', 'Vente'),
    ]
    TRANSACTION_STATUSES = [
        ('PENDING', 'En attente de paiement'), # Initial state for payment
        ('PAID', 'Payé (Attente confirmation crypto)'), # Payment received by FedaPay
        ('FAILED', 'Échoué'),
        ('CANCELLED', 'Annulé'),
        ('COMPLETED', 'Terminé (Crypto envoyée)'), # Crypto sent to user or FCFA sent
        ('REFUNDED', 'Remboursé'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True) # Lien vers l'utilisateur
    crypto = models.ForeignKey(Crypto, on_delete=models.PROTECT)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES, default='BUY')
    
    amount_fcfa = models.DecimalField(max_digits=15, decimal_places=2)
    amount_crypto = models.DecimalField(max_digits=20, decimal_places=10)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Nouveaux champs pour l'intégration de paiement
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUSES, default='PENDING')
    fedapay_transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True, help_text="ID de transaction FedaPay")
    user_receiving_address = models.CharField(max_length=200, blank=True, null=True, help_text="Adresse où l'utilisateur recevra la crypto (pour les achats)")
    user_paying_address = models.CharField(max_length=200, blank=True, null=True, help_text="Adresse d'où l'utilisateur envoie la crypto (pour les ventes)") # Pourrait être ses détails bancaires/mobile money pour la vente

    def __str__(self):
        return f"{self.transaction_type} {self.amount_crypto} {self.crypto.sigle} for {self.amount_fcfa} FCFA (Status: {self.status}) par {self.user.username if self.user else 'N/A'}"

class AdresseCrypto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=255)
    nom = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'crypto', 'adresse')

    def __str__(self):
        return f"{self.user.username}'s {self.crypto.sigle} address: {self.adresse}"

class Vente(models.Model):
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    quantite = models.FloatField()
    valeur = models.FloatField(editable=False)
    montant = models.FloatField(editable=False)
    adresse = models.CharField(max_length=200, null=True)
    statut = models.CharField(choices=STATUS, default="En attente")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.client.nom, self.crypto.nom)
    
    def save(self, *args, **kwargs):
        # Calcul du montant
        self.valeur = self.crypto.prix_vente
        self.montant = self.quantite * self.valeur
        # Vérification de la quantité
        if self.quantite > self.crypto.quantite:
            raise ValueError("La quantité demandée est supérieure à la quantité disponible")
        # Vérification du prix de vente
        if self.valeur < self.crypto.prix_vente_min:
            raise ValueError("La quantité est inférieure à la quantité minimum")
        # Vérification du prix d'achat
        if self.valeur < self.crypto.prix_achat_min:
            raise ValueError("La quantité est inférieure à la quantité minimum")

        super().save(*args, **kwargs)

class Achat(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    quantite = models.FloatField()
    adresse = models.CharField(max_length=255, null = True)  # <-- ce champ doit exister
    statut = models.CharField(choices=STATUS, default="En attente")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.client.nom, self.crypto.nom)
    
    def save(self, *args, **kwargs):
        # Calcul du montant
        self.valeur = self.crypto.prix_achat
        self.montant = self.quantite * self.valeur
        # Vérification de la quantité
        if self.quantite > self.crypto.quantite:
            raise ValueError("La quantité demandée est supérieure à la quantité disponible")
        # Vérification du prix d'achat
        if self.valeur < self.crypto.prix_achat_min:
            raise ValueError("La quantité est inférieure à la quantité minimum")
        super().save(*args, **kwargs)

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('approuve', 'Approuvé'),
        ('rejete', 'Rejeté')
    ]
    achat = models.ForeignKey('Achat', on_delete=models.CASCADE, null=True, blank=True)
    vente = models.ForeignKey('Vente', on_delete=models.CASCADE, null=True, blank=True)
    crypto = models.ForeignKey('Crypto', on_delete=models.CASCADE)
    quantite = models.FloatField()
    montant = models.FloatField()
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction de {self.quantite} {self.crypto.sigle} - Statut: {self.get_statut_display()}"

    def save(self, *args, **kwargs):
        # 
        if self.achat:
            self.montant = self.achat.quantite * self.achat.crypto.prix_achat
        elif self.vente:
            self.montant = self.vente.quantite * self.vente.crypto.prix_vente
        super().save(*args, **kwargs)

class Tutoriel(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    media = models.FileField(upload_to='tutoriels/')

    def __str__(self):
        return self.titre
   
@receiver(pre_delete, sender=Tutoriel)
def delete_post_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

class Adresse(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='adresses')
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE, related_name='adresses_crypto')
    adresse = models.CharField(max_length=200)
    nom = models.CharField(max_length=100, help_text='Nom pour identifier cette adresse')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['client', 'nom']
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.nom} - {self.crypto.nom}"

