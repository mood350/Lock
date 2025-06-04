from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
import os

from django.dispatch import receiver

STATUS = (
    ("Approuvé","Approuvé"),
    ("Rejeté","Rejeté"),
    ("En attente","En attente")
)

DISPONIBILITE = (
    ("Non","Non disponible"),
    ("Oui","Disponible")
)

class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=100)
    date_naissance = models 
    email = models.EmailField()
    telephone = models.IntegerField()
    password = models.CharField(max_length=100)

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        #Si un email existe déjà dans la base de données
        if Utilisateur.objects.filter(email=self.email).exists():
            raise ValueError("Un utilisateur avec cet email existe déjà.")
        #Si un téléphone existe déjà dans la base de données
        if Utilisateur.objects.filter(telephone=self.telephone).exists():
            raise ValueError("Un utilisateur avec ce numéro de téléphone existe déjà.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

class Admin(Utilisateur):
    niveau_acces = models.CharField(max_length=50, default='admin', editable=False)

class ServiceClient(Utilisateur):
    niveau_acces = models.CharField(max_length=50, default='service_client', editable=False)

class Client(Utilisateur):
    date_inscription = models.DateTimeField(auto_now_add=True)

class KYC(models.Model): 
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='kyc')
    date_naissance = models.DateField(null=True, blank=True)
    adresse = models.CharField(max_length=200, null=True, blank=True)
    cni = models.CharField(max_length=20, null=True, blank=True)
    statut = models.IntegerField(choices=STATUS, default=0)
    date_validation = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenoms} - {self.email}"

class Validateur(Utilisateur):
    niveau_acces = models.CharField(max_length=50, default='validateur', editable=False)

class Crypto(models.Model):
    nom = models.CharField(max_length=100)
    sigle = models.CharField(max_length=10)
    adresse = models.CharField(max_length=200)
    prix_achat = models.FloatField()
    prix_vente = models.FloatField()
    prix_achat_min = models.FloatField(null=True, blank=True)
    prix_vente_min = models.FloatField(null=True, blank=True)
    quantite = models.FloatField(null=True, blank=True)
    disponibilite = models.CharField(choices=DISPONIBILITE, default="Oui")

    def save(self, *args, **kwargs):
        if self.quantite == 0 :
            self.disponible = "Non"
        else:
            self.disponible = "Oui"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom}-({self.sigle})"

class Vente(models.Model):
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    quantite = models.FloatField()
    valeur = models.FloatField(editable=False)
    montant = models.FloatField(editable=False)
    adresse = models.CharField(max_length=200, null=True)
    statut = models.IntegerField(choices=STATUS, default="En attente")
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
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    quantite = models.FloatField()
    valeur = models.FloatField(editable=False)
    montant = models.FloatField(editable=False)
    adresse = models.CharField(max_length=200, null=True)
    statut = models.IntegerField(choices=STATUS, default="En attente")
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
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, null=True)
    achat = models.ForeignKey(Achat, on_delete=models.CASCADE, null=True)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    quantite = models.FloatField()
    montant = models.FloatField()
    statut = models.IntegerField(choices=STATUS, default="En attente")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.crypto.nom

    def save(self, *args, **kwargs):
        # 
        if self.vente:
            self.montant = self.vente.montant
            self.quantite = self.vente.quantite
            self.crypto = self.vente.crypto
            self.statut = self.vente.statut
        else:
            self.montant = self.achat.montant
            self.quantite = self.achat.quantite
            self.crypto = self.achat.crypto
            self.statut = self.achat.statut
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