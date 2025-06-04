from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [

    #Dashboard URLs
    path('base', views.base, name='base'),
    path('home/', views.index, name='index'),
    path('faq/', views.faq, name='faq'),
    path('profile/', views.profile, name='profile'),
    path('adresses/', views.adresses, name='adresses'),
    path('historique/', views.historique, name='historique'),
    path('parametre/', views.parametre, name='parametre'),

    #No connection URLs
    path('', views.acceuil, name='acceuil'),
    path('service/', views.service, name='service'),
    path('partenaire/', views.partenaire, name='partenaire'),
    path('propos/', views.propos, name='propos'),
    path('faq/', views.faq, name='faq'),
    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('contact/', views.contact, name='contact'),
    path('auth/', views.auth, name='auth'),
    path('politique_confidentialite/', views.politique_confidentialite, name='politique_confidentialite'),
    path('conditions_utilisation/', views.conditions_utilisation, name='conditions_utilisation'),
    path('support_contact/', views.support_contact, name='support_contact'),

    path('achat/', views.achat, name='achat'),
    path('vente/', views.vente, name='vente'),
    path('profiles/', views.profiles, name='profiles')
   
    
]