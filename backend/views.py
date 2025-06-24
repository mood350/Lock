from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from multiprocessing.connection import Client
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.db import models
from .form import *
from django.utils import timezone
import os

# Create your views here.

# Admin views
@login_required
def admin(request):
    if not request.user.is_staff:
        return redirect('accueil')
    return render(request, 'admin/dashboard_admin.html')

@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('accueil')
    clients = Client.objects.all()
    cryptos = Crypto.objects.all()
    adresses = Adresse.objects.all()
    transactions = Transaction.objects.all()
    achats = Achat.objects.all()
    ventes = Vente.objects.all()
    context = {
        'clients': clients,
        'cryptos': cryptos,
        'adresses': adresses,
        'transactions': transactions,
        'achats': achats,
        'ventes': ventes
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('index')
    nb_clients = Client.objects.count()
    nb_cryptos = Crypto.objects.count()
    nb_transactions = Transaction.objects.count()
    nb_achats = Achat.objects.count()
    transactions = Transaction.objects.order_by('-date')[:10]
    return render(request, 'admin/dashboard_admin.html', {
        'nb_clients': nb_clients,
        'nb_cryptos': nb_cryptos,
        'nb_transactions': nb_transactions,
        'nb_achats': nb_achats,
        'transactions': transactions,
        'section': 'dashboard'
    })

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
def historique(request):    
    client = get_object_or_404(Client, user=request.user)
    transactions = Transaction.objects.filter(
        models.Q(achat__client=client) | models.Q(vente__client=client)
    ).order_by('-date')
    
    return render(request, 'dashboard/historique.html', {
        'transactions': transactions
    })

# No connection views
def accueil(request):
    return render(request, 'accueil.html')

def connexion(request):
    error_message = None
    email = ''
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        motdepasse = request.POST.get('motdepasse', '').strip()
        user = authenticate(request, username=email, password=motdepasse)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = "Nom d'utilisateur ou mot de passe incorrect."
    return render(request, 'connexion.html', {'error_message': error_message, 'email': email})

def inscription(request):
    if request.method == 'POST':
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
            nom = request.POST.get('nom')
            prenoms = request.POST.get('prenoms')
            date_naissance = request.POST.get('date_naissance')
            email = request.POST.get('email')
            telephone = request.POST.get('telephone')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirmPassword')
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

def politique_confidentialite(request):
    return render(request, 'politique_confidentialite.html')

def conditions_utilisation(request):
    return render(request, 'conditions_utilisation.html')

def support_contact(request):
    return render(request, 'support_contact.html')

@login_required
def achat(request, crypto_id):
    crypto = get_object_or_404(Crypto, id=crypto_id)
    client = get_object_or_404(Client, user=request.user)
    adresses = Adresse.objects.filter(client=client, crypto=crypto)
    error_message = None

    if request.method == 'POST':
        try:
            quantite_str = request.POST.get('quantite', '').strip().replace(',', '.')
            if not quantite_str:
                raise ValueError("La quantité est requise")
            
            quantite = float(quantite_str)
            if quantite <= 0:
                raise ValueError("La quantité doit être positive")

            adresse_existante = request.POST.get('adresse_existante')
            nouvelle_adresse = request.POST.get('nouvelle_adresse')
            adresse_val = adresse_existante if adresse_existante else nouvelle_adresse

            if not adresse_val:
                raise ValueError("Une adresse est requise")

            montant = quantite * crypto.prix_achat

            # Création de l'achat
            achat = Achat.objects.create(
                client=client,
                crypto=crypto,
                quantite=quantite,
                adresse=adresse_val
            )

            # Création de la transaction
            Transaction.objects.create(
                achat=achat,
                crypto=crypto,
                quantite=quantite,
                montant=montant,
                statut='en_attente'
            )

            return redirect('historique')

        except ValueError as e:
            error_message = str(e)
        except Exception as e:
            print(f"Erreur: {str(e)}")
            error_message = "Une erreur est survenue"

    return render(request, 'dashboard/achat.html', {
        'crypto': crypto,
        'adresses': adresses,
        'error_message': error_message
    })

@login_required
def vente(request, crypto_id):
    crypto = get_object_or_404(Crypto, id=crypto_id)
    client = get_object_or_404(Client, user=request.user)
    adresses = Adresse.objects.filter(client=client, crypto=crypto)
    error_message = None

    if request.method == 'POST':
        try:
            quantite_str = request.POST.get('quantite', '').strip().replace(',', '.')
            if not quantite_str:
                raise ValueError("La quantité est requise")
            quantite = float(quantite_str)
            if quantite <= 0:
                raise ValueError("La quantité doit être positive")

            adresse_existante = request.POST.get('adresse_existante')
            nouvelle_adresse = request.POST.get('nouvelle_adresse')
            adresse_val = adresse_existante if adresse_existante else nouvelle_adresse
            if not adresse_val:
                raise ValueError("Une adresse est requise")

            montant = quantite * crypto.prix_vente

            vente = Vente.objects.create(
                client=client,
                crypto=crypto,
                quantite=quantite,
                adresse=adresse_val
            )

            Transaction.objects.create(
                vente=vente,
                crypto=crypto,
                quantite=quantite,
                montant=montant,
                statut='en_attente'
            )

            return redirect('historique')

        except ValueError as e:
            error_message = str(e)
        except Exception as e:
            print(f"Erreur: {str(e)}")
            error_message = "Une erreur est survenue"

    return render(request, 'dashboard/vente.html', {
        'crypto': crypto,
        'adresses': adresses,
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

def cryptoadmin(request):
    if not request.user.is_staff:
        return redirect('index')
    cryptos = Crypto.objects.all()
    return render(request, 'admin/cryptoadmin.html', {
        'cryptos': cryptos,
        'section': 'cryptos'
    })

def transactionadmin(request):
    if not request.user.is_staff:
        return redirect('index')
    transactions = Transaction.objects.order_by('-date')
    return render(request, 'admin/transactionadmin.html', {
        'transactions': transactions,
        'section': 'transactions'
    })

@login_required
def clientadmin(request):
    if not request.user.is_staff:
        return redirect('index')

    # On ne récupère que les KYC en attente
    kycs = KYC.objects.filter(statut='en_attente').select_related('client')

    if request.method == 'POST':
        kyc_id = request.POST.get('kyc_id')
        action = request.POST.get('action')
        kyc = KYC.objects.filter(id=kyc_id).first()
        if kyc:
            if action == 'confirmer':
                kyc.statut = 'valide'
                kyc.date_validation = timezone.now()
            elif action == 'rejeter':
                kyc.statut = 'refuse'
                kyc.date_validation = timezone.now()
            kyc.save()
        return redirect('clientadmin')

    return render(request, 'admin/clientadmin.html', {
        'kycs': kycs,
        'section': 'clients'
    })

def ajouter_crypto(request):
    if not request.user.is_staff:
        return redirect('index')
    error_message = None
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        sigle = request.POST.get('sigle', '').strip()
        adresse = request.POST.get('adresse', '').strip()
        prix_achat = request.POST.get('prix_achat', '').strip()
        prix_vente = request.POST.get('prix_vente', '').strip()
        prix_achat_min = request.POST.get('prix_achat_min', '').strip()
        prix_vente_min = request.POST.get('prix_vente_min', '').strip()
        quantite = request.POST.get('quantite', '').strip()
        disponibilite = request.POST.get('disponibilite', '').strip()
        try:
            prix_achat = float(prix_achat)
            prix_vente = float(prix_vente)
            prix_achat_min = float(prix_achat_min)
            prix_vente_min = float(prix_vente_min)
            quantite = float(quantite)
        except ValueError:
            error_message = "Les prix et la quantité doivent être des nombres valides."
        else:
            if not all([nom, sigle, adresse, disponibilite]):
                error_message = "Tous les champs sont obligatoires."
            elif prix_achat <= 0 or prix_vente <= 0 or prix_achat_min <= 0 or prix_vente_min <= 0 or quantite <= 0:
                error_message = "Les prix et la quantité doivent être strictement supérieurs à 0."
            else:
                Crypto.objects.create(
                    nom=nom,
                    sigle=sigle,
                    adresse=adresse,
                    prix_achat=prix_achat,
                    prix_vente=prix_vente,
                    prix_achat_min=prix_achat_min,
                    prix_vente_min=prix_vente_min,
                    quantite=quantite,
                    disponibilite=disponibilite
                )
                return redirect('cryptoadmin')
    return render(request, 'admin/ajouter_crypto.html', {
        'error_message': error_message,
        'section': 'cryptos'
    })

def supprimer_crypto(request, crypto_id):
    if not request.user.is_staff:
        return redirect('index')
    crypto = Crypto.objects.filter(id=crypto_id).first()
    if request.method == 'POST' and crypto:
        crypto.delete()
    return redirect('cryptoadmin')

def modifier_crypto(request, crypto_id):
    if not request.user.is_staff:
        return redirect('index')
    crypto = Crypto.objects.filter(id=crypto_id).first()
    if not crypto:
        return redirect('cryptoadmin')
    error_message = None
    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        sigle = request.POST.get('sigle', '').strip()
        prix_achat = request.POST.get('prix_achat', '').strip()
        prix_vente = request.POST.get('prix_vente', '').strip()
        if nom and sigle and prix_achat and prix_vente:
            crypto.nom = nom
            crypto.sigle = sigle
            crypto.prix_achat = float(prix_achat)
            crypto.prix_vente = float(prix_vente)
            crypto.save()
            return redirect('cryptoadmin')
        else:
            error_message = "Tous les champs sont obligatoires."
    return render(request, 'admin/modifier_crypto.html', {
        'crypto': crypto,
        'error_message': error_message,
        'section': 'cryptos'
    })

def valider_transaction(request, transaction_id):
    if not request.user.is_staff:
        return redirect('index')
    transaction = Transaction.objects.filter(id=transaction_id).first()
    if transaction:
        transaction.statut = 'approuve'
        transaction.save()
    return redirect('transactionadmin')

def rejeter_transaction(request, transaction_id):
    if not request.user.is_staff:
        return redirect('index')
    transaction = Transaction.objects.filter(id=transaction_id).first()
    if transaction:
        transaction.statut = 'rejete'
        transaction.save()
    return redirect('transactionadmin')

@login_required
def kyc_form(request):
    client = Client.objects.get(user=request.user)
    kyc = KYC.objects.filter(client=client).first()

    # Permettre la resoumission si le KYC est refusé
    if kyc and kyc.statut == 'refuse':
        kyc.delete()
        kyc = None

    if request.method == 'POST':
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            kyc_obj = form.save(commit=False)
            kyc_obj.client = client
            kyc_obj.statut = 'en_attente'
            kyc_obj.date_validation = None
            kyc_obj.save()
            return redirect('profile')
    else:
        form = KYCForm(instance=kyc)

    return render(request, 'kyc.html', {
        'form': form,
        'kyc': KYC.objects.filter(client=client).first()
    })

@login_required
def kyc_verification(request, kyc_id):
    if not request.user.is_staff:
        return redirect('index')
    kyc = get_object_or_404(KYC, id=kyc_id)
    client = kyc.client

    # Vérifie si le document identité est une image supportée
    doc_is_image = False
    if kyc.document_identite and kyc.document_identite.url:
        ext = os.path.splitext(kyc.document_identite.url)[1].lower()
        doc_is_image = ext in [
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg', '.jfif', '.pjpeg', '.pjp', '.ico', '.heic', '.heif'
        ]

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'valider':
            kyc.statut = 'valide'
            kyc.date_validation = timezone.now()
            kyc.save()
        elif action == 'rejeter':
            kyc.statut = 'refuse'
            kyc.date_validation = timezone.now()
            kyc.save()
        return redirect('clientadmin')

    return render(request, 'admin/kyc_verification.html', {
        'client': client,
        'kyc': kyc,
        'doc_is_image': doc_is_image,
        'section': 'clients'
    })