from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
# Create your views here.


# Dashboard views
def index(request):
    return render(request, 'dashboard/index.html')

def base(request):
    return render(request, 'dashboard/base.html')

def adresses(request):
    return render(request, 'dashboard/adresses.html')

def faq(request):
    return render(request, 'dashboard/faq.html')

def profile(request):
    return render(request, 'dashboard/profile.html')

def historique(request):    
    return render(request, 'dashboard/historique.html')

def parametre(request):
    return render(request, 'dashboard/parametre.html')


# No connection views
def acceuil(request):
    return render(request, 'acceuil.html')

def index(request):
    return render(request, 'index.html')

def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        motdepasse = request.POST.get('motdepasse')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=motdepasse)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                return render(request, 'connexion.html', {'error_message': "Identifiants invalides", 'email': email})
        except User.DoesNotExist:
            return render(request, 'connexion.html', {'error_message': "Aucun compte avec cet email", 'email': email})
    return render(request, 'connexion.html')


def inscription(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'inscription.html', {'error': "Nom d'utilisateur déjà pris"})
        if User.objects.filter(email=email).exists():
            return render(request, 'inscription.html', {'error': "Email déjà utilisé"})
        User.objects.create_user(username=username, email=email, password=password)
        return redirect('connexion')
    return render(request, 'inscription.html')



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
        # Envoi d'email (optionnel, nécessite configuration email dans settings.py)
        # send_mail(sujet, f"De: {nom} <{email}>\n\n{message}", settings.DEFAULT_FROM_EMAIL, ['support@lockcrypto.com'])
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

def achat(request):
    return render(request, 'achat.html')

def vente(request):
    return render(request, 'vente.html')


def profiles(request):
    return render(request, 'profile.html')

