from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.acceuil, name='acceuil'),
    path('base', views.base, name='base'),
    path('index_base/', views.index_base, name='index_base'),
    path('faq_base/', views.faq_base, name='faq_base'),
    path('profile_base/', views.profile_base, name='profile_base'),
    path('adresses_base/', views.adresses_base, name='adresses_base'),
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