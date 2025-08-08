from datetime import timezone
from django.contrib import admin, messages
from django.contrib import admin
import requests
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

@admin.register(Crypto)
class CryptoAdmin(admin.ModelAdmin):
    list_display = ('nom', 'sigle', 'valeur_sur_le_marche_fcfa', 'quantite_disponible', 'min_achat_fcfa', 'max_achat_fcfa', 'deposit_address')
    search_fields = ('nom', 'sigle')
    list_filter = ('nom',)

@admin.register(ConversionTransaction)
class ConversionTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'crypto', 'transaction_type', 'amount_fcfa', 'amount_crypto',
        'status', 'fedapay_transaction_id', 'timestamp'
    )
    list_filter = ('status', 'transaction_type', 'crypto', 'timestamp', 'user')
    search_fields = ('crypto__sigle', 'fedapay_transaction_id', 'user__username')
    readonly_fields = ('timestamp',)
    fieldsets = (
        (None, {
            'fields': ('user', 'crypto', 'transaction_type', 'status')
        }),
        ('Montants', {
            'fields': ('amount_fcfa', 'amount_crypto')
        }),
        ('Détails FedaPay', {
            'fields': ('fedapay_transaction_id',)
        }),
        ('Adresses', {
            'fields': ('user_receiving_address', 'user_paying_address')
        }),
        ('Date', {
            'fields': ('timestamp',)
        }),
    )

@admin.register(AdresseCrypto)
class AdresseCryptoAdmin(admin.ModelAdmin):
    list_display = ('user', 'crypto', 'adresse', 'nom')
    search_fields = ('user__username', 'crypto__sigle', 'adresse')
    list_filter = ('crypto',)