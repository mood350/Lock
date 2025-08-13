import os
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from multiprocessing.connection import Client
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .form import *
from django.utils import timezone
from django.contrib import messages
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # pyright: ignore[reportMissingImports]
from rest_framework import status # type: ignore
from .serializers import BuyCryptoRequestSerializer,CryptoDetailSerializer, SellCryptoRequestSerializer, TransactionResultSerializer

logger = logging.getLogger(__name__)

def test(request):
    return render(request, 'test.html')

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
class CryptoDetailAPIView(APIView):
    def get(self, request, sigle, *args, **kwargs):
        crypto = get_object_or_404(Crypto, sigle__iexact=sigle)
        serializer = CryptoDetailSerializer(crypto)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BuyCryptoAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BuyCryptoRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount_fcfa = serializer.validated_data['amount_fcfa']
        crypto_sigle = serializer.validated_data['crypto_sigle'].upper()

        crypto = get_object_or_404(Crypto, sigle__iexact=crypto_sigle)

        if not crypto.is_active:
            return Response({"error": f"{crypto.nom} n'est pas active pour le trading."},
                            status=status.HTTP_400_BAD_REQUEST)

        if amount_fcfa < crypto.min_achat_fcfa or amount_fcfa > crypto.max_achat_fcfa:
            return Response({"error": f"Le montant FCFA doit être entre {crypto.min_achat_fcfa} et {crypto.max_achat_fcfa} pour {crypto.sigle}."},
                            status=status.HTTP_400_BAD_REQUEST)

        if crypto.valeur_sur_le_marche_fcfa <= Decimal('0.0'):
             return Response({"error": f"La valeur sur le marché de {crypto.sigle} n'est pas définie ou invalide."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        amount_crypto_to_receive = amount_fcfa / crypto.valeur_sur_le_marche_fcfa

        if amount_crypto_to_receive <= Decimal('0.0'):
            return Response({"error": "Le montant de crypto calculé est invalide."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if crypto.quantite_disponible < amount_crypto_to_receive:
            return Response({"error": f"Quantité insuffisante de {crypto.sigle} disponible pour l'achat."},
                            status=status.HTTP_400_BAD_REQUEST)

        transaction = ConversionTransaction.objects.create(
            crypto=crypto,
            transaction_type='BUY',
            amount_fcfa=amount_fcfa,
            amount_crypto=amount_crypto_to_receive,
        )
        
        crypto.quantite_disponible -= amount_crypto_to_receive
        crypto.save()

        response_serializer = TransactionResultSerializer(transaction)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

class SellCryptoAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SellCryptoRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount_crypto = serializer.validated_data['amount_crypto']
        crypto_sigle = serializer.validated_data['crypto_sigle'].upper()

        crypto = get_object_or_404(Crypto, sigle__iexact=crypto_sigle)

        if not crypto.is_active:
            return Response({"error": f"{crypto.nom} n'est pas active pour le trading."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if crypto.valeur_sur_le_marche_fcfa <= Decimal('0.0'):
             return Response({"error": f"La valeur sur le marché de {crypto.sigle} n'est pas définie ou invalide."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        amount_fcfa_to_receive = amount_crypto * crypto.valeur_sur_le_marche_fcfa

        if amount_fcfa_to_receive <= Decimal('0.0'):
            return Response({"error": "Le montant FCFA calculé est invalide."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if amount_fcfa_to_receive < crypto.min_vente_fcfa or amount_fcfa_to_receive > crypto.max_vente_fcfa:
            return Response({"error": f"Le montant FCFA résultant doit être entre {crypto.min_vente_fcfa} et {crypto.max_vente_fcfa} pour {crypto.sigle}."},
                            status=status.HTTP_400_BAD_REQUEST)

        transaction = ConversionTransaction.objects.create(
            crypto=crypto,
            transaction_type='SELL',
            amount_fcfa=amount_fcfa_to_receive,
            amount_crypto=amount_crypto,
        )

        crypto.quantite_disponible += amount_crypto
        crypto.save()

        response_serializer = TransactionResultSerializer(transaction)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

def index(request):
    cryptos = Crypto.objects.all().order_by('nom')

    context = {
        'cryptos': cryptos,
    }
    
    return render(request, 'dashboard/index.html', context)

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
    # La vue récupère simplement toutes les transactions de l'utilisateur
    transactions = ConversionTransaction.objects.filter(user=request.user).order_by('-timestamp')
    
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
        # Récupération des données du formulaire
        nom = request.POST.get('nom')
        prenoms = request.POST.get('prenoms')
        date_naissance = request.POST.get('date_naissance')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # 1. Vérification de la correspondance des mots de passe
        if password != confirm_password:
            return render(request, 'inscription.html', {
                'error_message': "Les mots de passe ne correspondent pas.",
                'nom': nom,
                'prenoms': prenoms,
                'email': email,
                'telephone': telephone,
            })
        
        # 2. Vérification de l'existence d'un utilisateur avec le même email
        if User.objects.filter(email=email).exists():
            return render(request, 'inscription.html', {
                'error_message': "Un utilisateur avec cet email existe déjà.",
                'nom': nom,
                'prenoms': prenoms,
                'email': email,
                'telephone': telephone,
            })

        # 3. Création de l'utilisateur Django et du client
        try:
            # Créer l'utilisateur Django
            user = User.objects.create_user(
                username=email, # L'email est souvent utilisé comme nom d'utilisateur
                email=email,
                password=password,
                first_name=prenoms,
                last_name=nom
            )
            
            # Créer le profil client associé (sans le champ password, car il est dans le modèle User)
            client = Client.objects.create(
                user=user,
                nom=nom,
                prenoms=prenoms,
                date_naissance=date_naissance,
                email=email,
                telephone=telephone
            )

            # 4. Connexion automatique de l'utilisateur
            user_auth = authenticate(request, username=email, password=password)
            if user_auth is not None:
                login(request, user_auth)
                return redirect('index') # Rediriger vers la page d'accueil après l'inscription
            else:
                return render(request, 'inscription.html', {
                    'error_message': "Erreur lors de la connexion automatique. Veuillez vous connecter manuellement.",
                    # Vous pouvez laisser les champs vides ici, car l'utilisateur est créé
                })

        except Exception as e:
            # Gérer les autres exceptions (ex: problème de base de données)
            return render(request, 'inscription.html', {
                'error_message': f"Une erreur est survenue lors de l'inscription: {e}",
                'nom': nom,
                'prenoms': prenoms,
                'email': email,
                'telephone': telephone,
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
        message_body = request.POST.get('message')

        full_message = f"Nom: {nom}\nEmail: {email}\n\nMessage:\n{message_body}"

        try:
            send_mail(
                subject=f"Demande de contact - {sujet}",
                message=full_message,
                from_email=settings.EMAIL_HOST_USER, # L'e-mail de votre serveur
                recipient_list=['princiuso350@gmail.com'], # L'e-mail où recevoir les messages
                fail_silently=False,
            )
            message_sent = True
        except Exception as e:
            # Gérer l'erreur si l'e-mail ne peut pas être envoyé
            print(f"Erreur lors de l'envoi de l'e-mail : {e}")
            message_sent = False
            
    return render(request, 'contact.html', {'message_sent': message_sent})

def politique_confidentialite(request):
    return render(request, 'politique_confidentialite.html')

def conditions_utilisation(request):
    return render(request, 'conditions_utilisation.html')

def support_contact(request):
    return render(request, 'support_contact.html')

def acheter_crypto_view(request, crypto_id):
    if not request.user.is_authenticated:
        messages.error(request, "Veuillez vous connecter pour effectuer un achat.")
        return redirect('login')

    try:
        current_client = request.user.client
    except Client.DoesNotExist:
        messages.error(request, "Votre compte client n'a pas été trouvé. Veuillez contacter le support.")
        return redirect('accueil_dashboard_ou_profil')

    crypto = get_object_or_404(Crypto, id=crypto_id)
    adresses_enregistrees = Adresse.objects.filter(client=current_client, crypto=crypto)

    initial_amount_fcfa = None
    initial_address = None
    initial_new_address = None

    if request.method == 'POST':
        amount_fcfa = request.POST.get('amount_fcfa')
        selected_address = request.POST.get('adresse_existante')
        new_address = request.POST.get('nouvelle_adresse')
        recipient_address = selected_address if selected_address else new_address.strip()

        try:
            amount_fcfa = float(amount_fcfa)
            if amount_fcfa <= 0:
                raise ValueError("Le montant doit être positif.")
            if amount_fcfa < float(crypto.min_achat_fcfa) or amount_fcfa > float(crypto.max_achat_fcfa):
                raise ValueError(f"Le montant doit être entre {crypto.min_achat_fcfa} et {crypto.max_achat_fcfa} FCFA.")
        except (ValueError, TypeError):
            messages.error(request, "Veuillez entrer un montant FCFA valide.")
            # ... (Logique de retour au template)
            # Votre code initial ici est correct

        if not recipient_address:
            messages.error(request, "Veuillez spécifier une adresse de réception.")
            # ... (Logique de retour au template)
            # Votre code initial ici est correct
        
        try:
            valeur_crypto_fcfa = float(crypto.valeur_sur_le_marche_fcfa)
            amount_crypto = amount_fcfa / valeur_crypto_fcfa
        except (TypeError, ValueError, ZeroDivisionError):
            messages.error(request, "Impossible de calculer la quantité de crypto. La valeur de la crypto est invalide.")
            # ... (Logique de retour au template)
            # Votre code initial ici est correct

        try:
            if not selected_address and new_address.strip():
                adresse_obj, created = Adresse.objects.get_or_create(
                    client=current_client,
                    crypto=crypto,
                    adresse=recipient_address,
                    defaults={'nom': f"Adresse {crypto.sigle} ({recipient_address[:10]}...)"}
                )
                if created:
                    messages.success(request, f"Nouvelle adresse {crypto.sigle} enregistrée : {recipient_address}.")

            # Création de la transaction en PENDING
            conversion_transaction = ConversionTransaction.objects.create(
                user=request.user,
                crypto=crypto,
                transaction_type='BUY',
                amount_fcfa=Decimal(str(amount_fcfa)),
                amount_crypto=Decimal(str(amount_crypto)),
                status='PENDING',
                user_receiving_address=recipient_address,
            )
            request.session['conversion_transaction_id'] = conversion_transaction.id

        except Exception as e:
            messages.error(request, f"Une erreur est survenue lors de la préparation de la transaction : {e}")
            # ... (Logique de retour au template)
            # Votre code initial ici est correct

        return redirect('confirmer_achat') # Utilisez le nom de l'URL, pas le nom de la fonction

    context = {
        'crypto': crypto,
        'adresses': adresses_enregistrees,
        'initial_amount_fcfa': initial_amount_fcfa,
        'initial_address': initial_address,
        'initial_new_address': initial_new_address,
    }
    return render(request, 'dashboard/achat.html', context)

def confirmer_achat_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "Veuillez vous connecter pour confirmer un achat.")
        return redirect('login')

    conversion_transaction_id = request.session.pop('conversion_transaction_id', None)

    if not conversion_transaction_id:
        messages.error(request, "Aucune transaction à confirmer. Veuillez recommencer.")
        # Rediriger vers la page d'achat d'une crypto existante (à adapter)
        return redirect('nom_de_votre_url_pour_acheter', crypto_id=1) 

    conversion_transaction = get_object_or_404(ConversionTransaction, id=conversion_transaction_id, user=request.user)

    if conversion_transaction.status != 'PENDING':
        messages.warning(request, f"Cette transaction est déjà {conversion_transaction.get_status_display()}.")
        return redirect('historique')

    transaction_data_for_fedapay = {
        'amount_fcfa': float(conversion_transaction.amount_fcfa),
        'crypto_id': conversion_transaction.crypto.id,
        'crypto_nom': conversion_transaction.crypto.nom,
        'crypto_sigle': conversion_transaction.crypto.sigle,
        'recipient_address': conversion_transaction.user_receiving_address,
        'user_email': request.user.email,
        'user_id': request.user.id,
        'callback_url': request.build_absolute_uri(reverse('fedapay_webhook')),
        # C'est la donnée cruciale que nous allons utiliser pour lier le webhook à notre transaction
        'internal_transaction_id': conversion_transaction.id, 
    }

    fedapay_public_key = settings.FEDAPAY_PUBLIC_KEY

    context = {
        'transaction_data': transaction_data_for_fedapay,
        'fedapay_public_key': fedapay_public_key,
    }
    return render(request, 'dashboard/confirmer_paiement.html', context)

@csrf_exempt
def fedapay_webhook(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Seules les requêtes POST sont autorisées.")

    try:
        body_unicode = request.body.decode('utf-8')
        if not body_unicode:
            return JsonResponse({'error': 'Empty body'}, status=400)
        data = json.loads(body_unicode)
    except Exception as e:
        logger.error(f'Invalid JSON: {str(e)}')
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Récupération des données du webhook
    event_type = data.get('event')
    transaction_data = data.get('data', {})
    
    # Récupération de l'ID de votre transaction depuis les méta-données
    custom_meta = transaction_data.get('custom_metadata', {})
    internal_transaction_id = custom_meta.get('internal_transaction_id')

    if not internal_transaction_id:
        logger.error("FedaPay webhook received without internal_transaction_id in meta data.")
        return JsonResponse({'error': 'Missing internal_transaction_id'}, status=400)

    try:
        # Tente de récupérer la transaction en utilisant son ID
        conversion_transaction = ConversionTransaction.objects.get(id=internal_transaction_id)

        # Logique de mise à jour du statut en fonction de l'événement
        if event_type == 'transaction.approved':
            conversion_transaction.status = 'APPROVED'
            # TODO: Implémentez la logique pour créditer la crypto à l'utilisateur ici.
            logger.info(f"Transaction {internal_transaction_id} APPROVED via FedaPay webhook.")
        elif event_type == 'transaction.canceled' or event_type == 'transaction.declined':
            conversion_transaction.status = 'CANCELLED' # Ou 'DECLINED' si vous avez ce statut
            logger.warning(f"Transaction {internal_transaction_id} CANCELLED via FedaPay webhook.")
        elif event_type == 'transaction.failed':
            conversion_transaction.status = 'FAILED'
            logger.error(f"Transaction {internal_transaction_id} FAILED via FedaPay webhook.")
        else:
            # Gérer d'autres événements si nécessaire
            logger.info(f"Webhook event not handled: {event_type} for transaction {internal_transaction_id}.")
            return JsonResponse({'success': True}) # Retourner success pour éviter les re-envois

        conversion_transaction.save()

    except ConversionTransaction.DoesNotExist:
        logger.error(f"Transaction with ID {internal_transaction_id} not found in database.")
        return JsonResponse({'error': 'Transaction not found'}, status=404)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

    return JsonResponse({'success': True})

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

@login_required
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

@login_required
def cryptoadmin(request):
    if not request.user.is_staff:
        return redirect('index')
    cryptos = Crypto.objects.all()
    return render(request, 'admin/cryptoadmin.html', {
        'cryptos': cryptos,
        'section': 'cryptos'
    })

@login_required
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

@login_required
def valider_transaction(request, transaction_id):
    if not request.user.is_staff:
        return redirect('index')
    transaction = Transaction.objects.filter(id=transaction_id).first()
    if transaction:
        transaction.statut = 'approuve'
        transaction.save()
    return redirect('transactionadmin')

@login_required
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
    #
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

@login_required
def tutoriels(request):
    tutoriels = Tutoriel.objects.all().order_by('-titre')
    tutoriel_list = []
    for tuto in tutoriels:
        ext = ''
        if tuto.media and hasattr(tuto.media, 'url'):
            ext = tuto.media.url.split('.')[-1].lower()
        media_type = 'image'
        if ext in ['mp4', 'webm', 'ogg']:
            media_type = 'video'
        elif ext == 'mp3':
            media_type = 'audio'
        tutoriel_list.append({
            'titre': tuto.titre,
            'description': tuto.description,
            'media_url': tuto.media.url if tuto.media else '',
            'media_type': media_type,
        })
    return render(request, 'dashboard/tutoriels.html', {
        'tutoriels': tutoriel_list
    })

@login_required
def tutoriels_admin(request):
    if not request.user.is_staff:
        return redirect('index')
    tutoriels = Tutoriel.objects.all().order_by('-id')
    return render(request, 'admin/tutoriels.html', {
        'tutoriels': tutoriels
    })

@login_required
def ajouter_tutoriel(request):
    if not request.user.is_staff:
        return redirect('index')

    error_message = None

    if request.method == 'POST':
        titre = request.POST.get('titre', '').strip()
        description = request.POST.get('description', '').strip()
        media = request.FILES.get('media')
        if titre and description and media:
            Tutoriel.objects.create(
                titre=titre,
                description=description,
                media=media
            )
            return redirect('tutoriels_admin')
        else:
            error_message = "Tous les champs sont obligatoires."

    return render(request, 'admin/ajouter_tutoriel.html', {
        'error_message': error_message
    })

@login_required
def modifier_tutoriel(request, tutoriel_id):
    if not request.user.is_staff:
        return redirect('index')
    tutoriel = get_object_or_404(Tutoriel, id=tutoriel_id)
    error_message = None

    if request.method == 'POST':
        titre = request.POST.get('titre', '').strip()
        description = request.POST.get('description', '').strip()
        media = request.FILES.get('media')
        if titre and description:
            tutoriel.titre = titre
            tutoriel.description = description
            if media:
                tutoriel.media = media
            tutoriel.save()
            return redirect('tutoriels_admin')
        else:
            error_message = "Tous les champs sont obligatoires."

    return render(request, 'admin/modifier_tutoriel.html', {
        'tutoriel': tutoriel,
        'error_message': error_message
    })

@login_required
def supprimer_tutoriel(request, tutoriel_id):
    if not request.user.is_staff:
        return redirect('index')
    tutoriel = get_object_or_404(Tutoriel, id=tutoriel_id)
    if request.method == 'POST':
        tutoriel.delete()
    return redirect('tutoriels_admin')

@login_required
def supprimer_adresse(request, adresse_id):
    client = Client.objects.get(user=request.user)
    adresse = get_object_or_404(Adresse, id=adresse_id, client=client)
    if request.method == 'POST':
        adresse.delete()
    return redirect('adresses')

class CryptoDetailAPIView(APIView):
    def get(self, request, sigle, *args, **kwargs):
        crypto = get_object_or_404(Crypto, sigle__iexact=sigle)
        serializer = CryptoDetailSerializer(crypto)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
