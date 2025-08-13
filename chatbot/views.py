# chatbot/views.py

import json
import logging
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .gemini_integration import get_gemini_response
from django.http import HttpResponseNotFound, HttpResponse, JsonResponse
from django.contrib.sessions.backends.db import SessionStore

# Configuration d'un logger pour le débogage
logger = logging.getLogger(__name__)

# Message de passage de relais
HANDOFF_MESSAGE = "Je vois que vous avez un problème. J'ai notifié un agent de support qui va prendre en charge votre demande. Veuillez patienter un instant."


def notify_support_team(user_message, conversation_history, session_key):
    """
    Fonction utilitaire pour envoyer un email d'alerte avec le lien et l'historique.
    """
    # Formatte l'historique de la conversation pour l'email
    history_text = "\n".join([f"{msg['role'].title()}: {msg['parts'][0]}" for msg in conversation_history])

    subject = "ALERTE CHATBOT: Problème client détecté !"
    message = (f"Un utilisateur a signalé un problème.\n"
               f"Dernier message : '{user_message}'\n\n"
               f"Pour répondre, suivez ce lien :\n"
               f"http://127.0.0.1:8000/chat/admin/support/{session_key}/\n\n"
               f"Historique de la conversation :\n"
               f"--------------------------------\n{history_text}")
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['princiuso350@gmail.com', 'tpemedia1@gmail.com', 'princetanankouboussi@gmail.com']

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        logger.info("Email d'alerte envoyé avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email d'alerte : {e}")

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')

            if user_message:
                conversation_history = request.session.get('conversation_history', [])
                
                problem_keywords = ['bloqué', 'erreur', 'problème', 'urgent', 'inquiet', 'panne']
                is_problem_detected = any(keyword in user_message.lower() for keyword in problem_keywords)
                
                if is_problem_detected:
                    conversation_history.append({'role': 'user', 'parts': [user_message]})
                    
                    session_key = request.session.session_key
                    
                    notify_support_team(user_message, conversation_history, session_key)
                    
                    conversation_history.append({'role': 'model', 'parts': [HANDOFF_MESSAGE]})
                    
                    request.session['conversation_history'] = conversation_history
                    request.session.modified = True
                    
                    return JsonResponse({'response': HANDOFF_MESSAGE})
                else:
                    # Comportement normal du chatbot si aucun problème n'est détecté
                    conversation_history.append({'role': 'user', 'parts': [user_message]})
                    
                    # --- NOUVELLE LIGNE ---
                    # On ne transmet à Gemini que les messages dont le rôle est 'user' ou 'model'
                    filtered_history = [
                        msg for msg in conversation_history 
                        if msg['role'] in ['user', 'model']
                    ]
                    # --- FIN DE LA NOUVELLE LIGNE ---
                    
                    # On envoie l'historique filtré à Gemini
                    bot_response = get_gemini_response(user_message, history=filtered_history)
                    conversation_history.append({'role': 'model', 'parts': [bot_response]})

                    request.session['conversation_history'] = conversation_history
                    request.session.modified = True

                    return JsonResponse({'response': bot_response})
            else:
                return JsonResponse({'error': 'Message vide'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON invalide'}, status=400)
        except Exception as e:
            logger.error(f"Erreur dans la vue chatbot : {e}")
            return JsonResponse({'error': 'Erreur interne du serveur'}, status=500)

    # La vue GET pour afficher la page de chat
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
        # Initialiser l'historique avec un message de bienvenue
        initial_history = [{'role': 'model', 'parts': ["Bonjour ! Comment puis-je vous aider ?"]}]
        request.session['conversation_history'] = initial_history
    
    conversation_history = request.session.get('conversation_history', [])
    
    context = {
        'conversation_history': conversation_history,
        'session_key': session_key,
    }
    return render(request, 'chatbot_app/index.html', context)

@csrf_exempt
def support_admin_view(request, session_key):
    # Charge la session de l'utilisateur concerné
    s = SessionStore(session_key=session_key)
    
    if not s.exists(session_key) or 'conversation_history' not in s:
        return HttpResponseNotFound("Session de l'utilisateur introuvable.")

    conversation_history = s.get('conversation_history', [])

    if request.method == 'POST':
        agent_message = request.POST.get('message')
        if agent_message:
            conversation_history.append({'role': 'agent', 'parts': [agent_message]})
            s['conversation_history'] = conversation_history
            s.save()
            return HttpResponse("Message envoyé avec succès.")
        else:
            return HttpResponse("Message vide.", status=400)
    
    context = {
        'conversation_history': conversation_history,
        'session_key': session_key,
    }
    return render(request, 'chatbot_app/support_admin.html', context)