from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def acceuil(request):
    return render(request, 'acceuil.html')

def index(request):
    return render(request, 'index.html')

def connexion(request):
    return render(request, 'connexion.html')

def inscription(request):
    return render(request, 'inscription.html')

def service(request):
    return render(request, 'service.html')

def partenaire(request):
    return render(request, 'partenaire.html')

def propos(request):
    return render(request, 'propos.html')

def faq(request):
    return render(request, 'faq.html')

def contact(request):
    return render(request, 'contact.html')

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


def profile(request):
    return render(request, 'profile.html')

