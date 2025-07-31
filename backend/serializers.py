from rest_framework import serializers
from .models import Crypto, ConversionTransaction, Decimal

class CryptoDetailSerializer(serializers.ModelSerializer):
    disponibilite = serializers.CharField(read_only=True)

    class Meta:
        model = Crypto
        fields = [
            'id', 'nom', 'sigle', 'deposit_address', # Renommé ici
            'valeur_sur_le_marche_fcfa',
            'quantite_disponible', 'is_active',
            'min_achat_fcfa', 'max_achat_fcfa', 'min_vente_fcfa', 'max_vente_fcfa',
            'disponibilite',
        ]

class BuyCryptoRequestSerializer(serializers.Serializer):
    crypto_sigle = serializers.CharField(max_length=10)
    amount_fcfa = serializers.DecimalField(max_digits=15, decimal_places=2, min_value=Decimal('0.01'))

class SellCryptoRequestSerializer(serializers.Serializer):
    crypto_sigle = serializers.CharField(max_length=10)
    amount_crypto = serializers.DecimalField(max_digits=20, decimal_places=10, min_value=Decimal('0.00000001'))

class TransactionResultSerializer(serializers.ModelSerializer):
    crypto_sigle = serializers.CharField(source='crypto.sigle', read_only=True)

    class Meta:
        model = ConversionTransaction
        fields = [
            'id', 'crypto_sigle', 'transaction_type',
            'amount_fcfa', 'amount_crypto',
            'timestamp'
        ]