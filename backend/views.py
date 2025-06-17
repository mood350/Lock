from http import client
from multiprocessing.connection import Client
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
<<<<<<< HEAD
from .models import Client, KYC
=======
from django.db import models

from .models import *
from .form import *
from backend import form

>>>>>>> 7e68f010ffd99cee7c63a4efce7e7c5fd99a60ca

# Create your views here.


# Dashboard views
@login_required
def index(request):
    cryptos = Crypto.objects.all()
    return render(request, 'dashboard/index.html', {'cryptos': cryptos})

@login_required
def base(request):
    return render(request, 'dashboard/base.html')

@login_required
def adresses(request):
    cryptos = Crypto.objects.all()
    adresses = []
    client = None
    if request.user.is_authenticated:
        try:
            client = Client.objects.get(user=request.user)
            adresses = Adresse.objects.filter(client=client)
        except Client.DoesNotExist:
            pass

    if request.method == 'POST' and client:
        nom = request.POST.get('nom')
        crypto_id = request.POST.get('crypto')
        adresse = request.POST.get('adresse')
        if all([nom, crypto_id, adresse]):
            crypto = Crypto.objects.get(id=crypto_id)
            Adresse.objects.create(
                client=client,
                crypto=crypto,
                nom=nom,
                adresse=adresse
            )
            return redirect('adresses')

    context = {
        'cryptos': cryptos,
        'adresses': adresses
    }
    return render(request, 'dashboard/adresses.html', context)

@login_required
def faq(request):
    return render(request, 'dashboard/faq.html')

@login_required
def profile(request):
    return render(request, 'dashboard/profil.html', {'user': request.user})

@login_required
def kyc(request):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        # Rediriger ou créer le client si nécessaire
        client = Client.objects.create(user=request.user)

    if request.method == 'POST':
        date_naissance = request.POST.get('date_naissance')
        adresse = request.POST.get('adresse')
        cni = request.POST.get('cni')

        kyc_obj, created = KYC.objects.get_or_create(client=client)
        kyc_obj.date_naissance = date_naissance
        kyc_obj.adresse = adresse
        kyc_obj.cni = cni
        kyc_obj.statut = 0  # En attente
        kyc_obj.save()

        return redirect('profile')

    return render(request, 'dashboard/kyc.html')

@login_required
def historique(request):    
    client = get_object_or_404(Client, user=request.user)
    transactions = Transaction.objects.filter(
        models.Q(achat__client=client) | models.Q(vente__client=client)
    ).order_by('-date')
    return render(request, 'dashboard/historique.html', {'transactions': transactions})


# No connection views
def accueil(request):
    return render(request, 'accueil.html')



def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('motdepasse')
        try:
<<<<<<< HEAD
            client = Client.objects.get(email=email)
            if client.password == password:  # (À remplacer par un hash en prod)
                # Connexion réussie, redirige vers l'accueil
                return redirect('accueil')
            # Récupérer l'utilisateur par email
=======
            # Récupérer l'utilisateur Django par email
>>>>>>> 7e68f010ffd99cee7c63a4efce7e7c5fd99a60ca
            user = User.objects.get(email=email)
            # Authentifier l'utilisateur
            user = authenticate(username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'connexion.html', {
                    'error_message': "Mot de passe incorrect",
                    'email': email
                })
        except User.DoesNotExist:
            return render(request, 'connexion.html', {
                'error_message': "Aucun compte trouvé avec cet email",
                'email': email
            })
    return render(request, 'connexion.html')

def inscription(request):
    if request.method == 'POST':
<<<<<<< HEAD
        nom = request.POST['nom']
        prenoms = request.POST['prenoms']
        date_naissance = request.POST['date_naissance']
        email = request.POST['email']
        telephone = request.POST['telephone']
        password = request.POST['password']  # À hasher en vrai projet !
        try:
            Client.objects.create(
                nom=nom,
                prenoms=prenoms,
                date_naissance=date_naissance,
                email=email,
                telephone=telephone,
                password=password
            )
            return redirect('connexion')
        except ValueError as e:
            # Affiche le message d’erreur dans le template
            nom = request.POST.get('nom')
            prenoms = request.POST.get('prenoms')
            email = request.POST.get('email')
            telephone = request.POST.get('telephone')
            password = request.POST.get('motdepasse')
            confirm_password = request.POST.get('confirm_motdepasse')
=======
        nom = request.POST.get('nom')
        prenoms = request.POST.get('prenoms')
        date_naissance = request.POST.get('date_naissance')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
>>>>>>> 7e68f010ffd99cee7c63a4efce7e7c5fd99a60ca

        if password != confirm_password:
            return render(request, 'inscription.html', {
                'error_message': "Les mots de passe ne correspondent pas",
                'nom': nom,
                'prenoms': prenoms,
                'email': email,
                'telephone': telephone
            })

        try:
            # Créer l'utilisateur Django
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=prenoms,
                last_name=nom
            )

            # Créer le profil client associé (sans password)
            client = Client.objects.create(
                user=user,
                nom=nom,
                prenoms=prenoms,
                date_naissance=date_naissance,
                email=email,
                telephone=telephone
            )

            # Authentifier et connecter l'utilisateur
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'inscription.html', {
                    'error_message': "Erreur lors de la connexion automatique.",
                    'nom': nom,
                    'prenoms': prenoms,
                    'email': email,
                    'telephone': telephone
                })

        except Exception as e:
            return render(request, 'inscription.html', {
                'error_message': "Une erreur est survenue lors de l'inscription",
                'nom': nom,
                'prenoms': prenoms,
                'email': email,
                'telephone': telephone
            })

    return render(request, 'inscription.html')

@login_required
def profile(request):
    try:
        client = Client.objects.get(user=request.user)
        kyc = KYC.objects.filter(client=client).first()
    except Client.DoesNotExist:
        client = None
        kyc = None

    context = {
        'client': client,  # On passe client au lieu de user
        'kyc': kyc
    }
    return render(request, 'dashboard/profil.html', context)

def service(request):
    return render(request, 'service.html')

def partenaire(request):
    return render(request, 'partenaire.html')

def propos(request):
    return render(request, 'Apropos.html')


def contact(request):
    message_sent = False
    if request.method == 'POST':
        nom = request.POST.get('name')
        email = request.POST.get('email')
        sujet = request.POST.get('subject')
        message = request.POST.get('message')

        message_sent = True
    return render(request, 'contact.html', {'message_sent': message_sent})

def auth(request):
    return render(request, 'auth.html')

def politique_confidentialite(request):
    return render(request, 'politique_confidentialite.html')

def conditions_utilisation(request):
    return render(request, 'conditions_utilisation.html')

def support_contact(request):
    return render(request, 'support_contact.html')

def achat(request, crypto_id):
    crypto = get_object_or_404(Crypto, id=crypto_id)
    client = get_object_or_404(Client, user=request.user)
    adresses = Adresse.objects.filter(client=client, crypto=crypto)

    if request.method == 'POST':
        form = AchatForm(request.POST)
        if form.is_valid():
            achat = form.save(commit=False)
            achat.client = client
            achat.crypto = crypto
            achat.save()
            # Crée la transaction ici si besoin
            return redirect('historique')
    else:
        form = AchatForm()

    return render(request, 'dashboard/achat.html', {
        'form': form,
        'crypto': crypto,
        'adresses': adresses,
    })

from .form import VenteForm
from .models import Client, Crypto

@login_required
def vente(request, crypto_id):
    crypto = get_object_or_404(Crypto, id=crypto_id)
    client = get_object_or_404(Client, user=request.user)
    error_message = None

    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            vente = form.save(commit=False)
            vente.client = client
            vente.crypto = crypto
            vente.save()
            # Crée la transaction ici si besoin
            return redirect('historique')
        else:
            error_message = "Un champ est invalide"
    else:
        form = VenteForm()

    return render(request, 'dashboard/vente.html', {
        'form': form,
        'crypto': crypto,
        'error_message': error_message
    })


def profiles(request):
    return render(request, 'profile.html', status=404)

def error_404_view(request, exception):
    return render(request, '404.html', status=404)

def ajouter_adresse(request):
    client = Client.objects.get(user=request.user)
    error_message = None

    if request.method == 'POST':
        form = AdresseForm(request.POST)
        if form.is_valid():
            adresse = form.save(commit=False)
            adresse.client = client
            adresse.save()
            return redirect('adresses')  # Redirige vers la liste des adresses
        else:
            error_message = "Un champ est invalide"
    else:
        form = AdresseForm()

    return render(request, 'dashboard/formulaire.html', {
        'form': form,
        'titre': "Ajouter une adresse",
        'bouton': "Ajouter",
        'error_message': error_message
    })