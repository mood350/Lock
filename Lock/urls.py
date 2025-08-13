from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path('admine/', admin.site.urls),
    path('', include('backend.urls')),
    path('chat/', include('chatbot.urls', namespace='chatbot')),  # Inclure les URLs de l'application chatbot
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)