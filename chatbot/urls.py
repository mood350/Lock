# chatbot/urls.py
from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chatbot_view, name='chatbot_view'),
    path('api/', views.chatbot_view, name='chat_api'),
    path('admin/support/<str:session_key>/', views.support_admin_view, name='support_admin'),
]