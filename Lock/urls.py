from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admine/', admin.site.urls),
    path('', include('backend.urls')),
    path('chat/', include('chatbot.urls', namespace='chatbot')),  # Inclure les URLs de l'application chatbot
]

urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)