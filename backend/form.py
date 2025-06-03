from django.shortcuts import render, redirect
from .models import Client, KYC
from django.contrib.auth.decorators import login_required

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
