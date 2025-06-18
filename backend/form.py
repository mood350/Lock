from django.shortcuts import render, redirect
from .models import Client, KYC
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Client, Achat, Vente, Transaction, Adresse

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenoms', 'date_naissance', 'telephone', 'email']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenoms': forms.TextInput(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['quantite']  # Remove 'crypto' and 'adresse' as they're handled in the view
        widgets = {
            'quantite': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Ex: 0.001'
            }),
        }

class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['quantite']  # Remove 'crypto' and 'adresse' as they're handled in the view
        widgets = {
            'quantite': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 'any',
                'placeholder': 'Ex: 0.001'
            }),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['crypto', 'quantite', 'montant', 'statut']
        widgets = {
            'crypto': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }

class AdresseForm(forms.ModelForm):
    class Meta:
        model = Adresse
        fields = ['nom', 'crypto', 'adresse']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'crypto': forms.Select(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
        }


@login_required
def kyc_form(request):
    client = Client.objects.get(user=request.user)

    if request.method == 'POST':
        date_naissance = request.POST.get('date_naissance')
        adresse = request.POST.get('adresse')
        cni = request.POST.get('cni')

        # Créer ou mettre à jour l'entrée KYC liée au client
        kyc, created = KYC.objects.get_or_create(client=client)
        kyc.date_naissance = date_naissance
        kyc.adresse = adresse
        kyc.cni = cni
        kyc.statut = 0  # En attente
        kyc.save()

        return redirect('profile')  # à adapter à ton URL de profil

    return render(request, 'dashboard/kyc.html')

