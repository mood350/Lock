# chatbot/urls.py
# (Assurez-vous que ce fichier est bien dans le dossier de l'application 'chatbot')

from django.urls import path
from . import views

app_name = 'chatbot' # C'est le namespace de l'application

urlpatterns = [
    # Le chemin VIDE '' correspondra à /chatbot/
    path('', views.chatbot_view, name='chatbot_view'),

    # Le chemin 'api/chat/' correspondra à /chatbot/api/chat/
    path('api/chat/', views.chatbot_view, name='chat_api'),
]