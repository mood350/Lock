from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .gemini_integration import get_gemini_response # Importe notre fonction Gemini

# Pour stocker l'historique de conversation (pour un utilisateur unique ou par session)
# Pour un usage réel, utilisez une base de données ou les sessions Django.
# Ceci est un exemple simple en mémoire.
conversation_history = []

@csrf_exempt # Pour les requêtes POST sans jeton CSRF, attention en production !
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')

        if user_message:
            # Ajouter le message utilisateur à l'historique
            global conversation_history
            conversation_history.append({'role': 'user', 'parts': [user_message]})

            # Obtenir la réponse de Gemini en passant l'historique
            bot_response = get_gemini_response(user_message, history=conversation_history)

            # Ajouter la réponse du bot à l'historique
            conversation_history.append({'role': 'model', 'parts': [bot_response]})

            return JsonResponse({'response': bot_response})
        else:
            return JsonResponse({'error': 'Message vide'}, status=400)
    return render(request, 'chatbot_app/index.html')
