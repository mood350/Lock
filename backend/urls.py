from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    #Chatbot URLs
    path('chatbot/', include('chatbot.urls')),  # Inclure les URLs de l'application chatbot

    #Admin URLs
    path('admin/', views.admin_dashboard, name='admin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-cryptos/', views.cryptoadmin, name='cryptoadmin'),
    path('admin-transactions/', views.transactionadmin, name='transactionadmin'),
    path('admin-clients/', views.clientadmin, name='clientadmin'),
    path('admin-cryptos/ajouter/', views.ajouter_crypto, name='ajouter_crypto'),
    path('admin-cryptos/supprimer/<int:crypto_id>/', views.supprimer_crypto, name='supprimer_crypto'),
    path('admin-cryptos/modifier/<int:crypto_id>/', views.modifier_crypto, name='modifier_crypto'),
    path('admin-cryptos/supprimer/<int:crypto_id>/confirmer/', views.supprimer_crypto, name='confirmer_suppression_crypto'),
    path('admin-transactions/valider/<int:transaction_id>/', views.valider_transaction, name='valider_transaction'),
    path('admin-transactions/rejeter/<int:transaction_id>/', views.rejeter_transaction, name='rejeter_transaction'),
    path('admin-kyc/<int:kyc_id>/', views.kyc_verification, name='kyc_verification'),
    path('admin/tutoriels/', views.tutoriels_admin, name='tutoriels_admin'),
    path('admin/tutoriels/ajouter/', views.ajouter_tutoriel, name='ajouter_tutoriel'),
    path('admin/tutoriels/modifier/<int:tutoriel_id>/', views.modifier_tutoriel, name='modifier_tutoriel'),
    path('admin/tutoriels/supprimer/<int:tutoriel_id>/', views.supprimer_tutoriel, name='supprimer_tutoriel'),


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
    path('kyc/', views.kyc_form, name='kyc_form'),
    path('tutoriels/', views.tutoriels, name='tutoriels'),
    path('supprimer_adresse/<int:adresse_id>/', views.supprimer_adresse, name='supprimer_adresse'),

    #No connection URLs
    path('', views.accueil, name='accueil'),
    path('propos/', views.propos, name='propos'),
    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription'),
    path('contact/', views.contact, name='contact'),
    path('politique_confidentialite/', views.politique_confidentialite, name='politique_confidentialite'),
    path('conditions_utilisation/', views.conditions_utilisation, name='conditions_utilisation'),
    path('support_contact/', views.support_contact, name='support_contact'),
    path('test/', views.test, name='test'),
    path('adresses/supprimer/<int:adresse_id>/', views.supprimer_adresse, name='supprimer_adresse'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)