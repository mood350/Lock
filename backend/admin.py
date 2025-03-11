from django.contrib import admin
from .models import *

class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenoms', 'email', 'telephone')
    search_fields = ('nom', 'prenoms', 'email', 'telephone')
    list_filter = ('nom', 'prenoms', 'email', 'telephone')
    ordering = ('nom',)
admin.site.register(Client, ClientAdmin)

class AdminAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenoms', 'email', 'telephone')
    search_fields = ('nom', 'prenoms', 'email', 'telephone')
    list_filter = ('nom', 'prenoms', 'email', 'telephone')
    ordering = ('nom',)
admin.site.register(Admin, AdminAdmin)

class ServiceclientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenoms', 'email', 'telephone')
    search_fields = ('nom', 'prenoms', 'email', 'telephone')
    list_filter = ('nom', 'prenoms', 'email', 'telephone')
    ordering = ('nom',)
admin.site.register(ServiceClient, ServiceclientAdmin)

class ValidateurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenoms', 'email', 'telephone')
    search_fields = ('nom', 'prenoms', 'email', 'telephone')
    list_filter = ('nom', 'prenoms', 'email', 'telephone')
    ordering = ('nom',)
admin.site.register(Validateur, ValidateurAdmin)

class CryptoAdmin(admin.ModelAdmin):
    list_display = ('nom', 'sigle', 'adresse', 'prix_achat', 'prix_vente', 'prix_achat_min', 'prix_vente_min', 'quantite', 'disponibilite')
    search_fields = ('nom', 'sigle', 'adresse', 'prix_achat', 'prix_vente', 'prix_achat_min', 'prix_vente_min', 'quantite', 'disponibilite')
    list_filter = ('nom', 'sigle', 'adresse', 'prix_achat', 'prix_vente', 'disponibilite')
    ordering = ('nom',)
admin.site.register(Crypto, CryptoAdmin)

class VenteAdmin(admin.ModelAdmin):
    list_display = ('crypto', 'client', 'quantite', 'valeur', 'montant', 'adresse', 'statut', 'date')
    search_fields = ('crypto', 'client', 'quantite', 'valeur', 'montant', 'adresse', 'statut', 'date')
    list_filter = ('crypto', 'client', 'quantite', 'valeur', 'montant', 'adresse','statut', 'date')
    ordering = ('date',)
admin.site.register(Vente, VenteAdmin)

class AchatAdmin(admin.ModelAdmin):
    list_display = ('crypto', 'client', 'quantite', 'valeur', 'montant', 'adresse', 'statut', 'date')
    search_fields = ('crypto', 'client', 'quantite', 'valeur', 'montant', 'adresse', 'statut', 'date')
    list_filter = ('crypto', 'client', 'quantite', 'valeur', 'montant', 'adresse', 'statut', 'date')
    ordering = ('date',)
admin.site.register(Achat, AchatAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('crypto', 'quantite', 'quantite', 'montant', 'statut', 'date')
    search_fields = ('crypto', 'quantite', 'quantite', 'montant', 'statut', 'date')
    list_filter = ('crypto', 'quantite', 'quantite', 'montant', 'statut', 'date')
    ordering = ('date',)
admin.site.register(Transaction, TransactionAdmin)


