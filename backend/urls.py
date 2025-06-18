from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [

    #Admin URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-cryptos/', views.cryptoadmin, name='cryptoadmin'),
    path('admin-transactions/', views.transactionadmin, name='transactionadmin'),
    path('admin-clients/', views.clientadmin, name='clientadmin'),
    path('admin-cryptos/ajouter/', views.ajouter_crypto, name='ajouter_crypto'),
    path('admin-cryptos/supprimer/<int:crypto_id>/', views.supprimer_crypto, name='supprimer_crypto'),
    path('admin-cryptos/modifier/<int:crypto_id>/', views.modifier_crypto, name='modifier_crypto'),
    path('admin-cryptos/supprimer/<int:crypto_id>/confirmer/', views.supprimer_crypto, name='confirmer_suppression_crypto'),

    #Dashboard URLs
    path('base', views.base, name='base'),
    path('home/', views.index, name='index'),
    path('faq/', views.faq, name='faq'),
    path('profile/', views.profile, name='profile'),
    path('adresses/', views.adresses, name='adresses'),
    path('historique/', views.historique, name='historique'),
    path('achat/<int:crypto_id>/', views.achat, name='achat'),
    path('vente/<int:crypto_id>/', views.vente, name='vente'),
    path('profiles/', views.profiles, name='profiles'),

    #No connection URLs
    path('', views.accueil, name='accueil'),
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
   
]