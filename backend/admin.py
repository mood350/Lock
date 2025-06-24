from datetime import timezone
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
    list_display = ['client', 'crypto', 'quantite', 'adresse', 'get_montant']

    def get_montant(self, obj):
        # Remplace par ton calcul réel
        return obj.quantite * obj.crypto.prix_achat
    get_montant.short_description = 'Montant'

admin.site.register(Achat, AchatAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('crypto', 'quantite', 'quantite', 'montant', 'statut', 'date')
    search_fields = ('crypto', 'quantite', 'quantite', 'montant', 'statut', 'date')
    list_filter = ('crypto', 'quantite', 'quantite', 'montant', 'statut', 'date')
    ordering = ('date',)
admin.site.register(Transaction, TransactionAdmin)


@admin.register(KYC)
class KYCAdmin(admin.ModelAdmin):
    list_display = ('client', 'statut', 'date_validation')
    list_filter = ('statut',)
    search_fields = ('client__nom', 'client__prenoms', 'client__email')
    actions = ['valider_kyc', 'refuser_kyc']

    def valider_kyc(self, request, queryset):
        queryset.update(statut='valide', date_validation=timezone.now())
    valider_kyc.short_description = "Valider la sélection"

    def refuser_kyc(self, request, queryset):
        queryset.update(statut='refuse', date_validation=timezone.now())
    refuser_kyc.short_description = "Refuser la sélection"


