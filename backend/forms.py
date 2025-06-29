from .models import *
from django import forms

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

<<<<<<< HEAD:backend/forms.py

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



=======
class KYCForm(forms.ModelForm):
    class Meta:
        model = KYC
        fields = ['date_naissance', 'adresse', 'cni', 'document_identite', 'selfie']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'cni': forms.TextInput(attrs={'class': 'form-control'}),
            'document_identite': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'selfie': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
>>>>>>> 75bb34b5396952830af9d11de8dcd33f810e8de3:backend/form.py
