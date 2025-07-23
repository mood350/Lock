from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admine/', admin.site.urls),
    path('', include('backend.urls')),
    path('', include('chatbot.urls')),  # Inclure les URLs de l'application chatbot
]