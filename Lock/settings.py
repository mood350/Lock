import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
import dj_database_url

# Chargez les variables d'environnement
load_dotenv()

# Chemins de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Configuration de sécurité et des clés ---
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'lock-1-r3rz.onrender.com']
CSRF_TRUSTED_ORIGINS = ['https://lock-1-r3rz.onrender.com']

# --- Variables d'environnement pour vos clés d'API ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FEDAPAY_PUBLIC_KEY = os.getenv("FEDAPAY_PUBLIC_KEY")
FEDAPAY_SECRET_KEY = os.getenv("FEDAPAY_SECRET_KEY")
FEDAPAY_WEBHOOK_SECRET = os.getenv("FEDAPAY_WEBHOOK_SECRET")

# --- Définition des applications ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chatbot',
    'backend',
]

# --- Middlewares ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Essentiel pour la détection de la langue
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Lock.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Lock.wsgi.application'

# # --- Configuration de la base de données ---
# DATABASE_URL = os.getenv("DATABASE_URL")
# if DATABASE_URL:
#     DATABASES = {
#         'default': dj_database_url.config(
#             default=DATABASE_URL,
#             conn_max_age=600,
#             conn_health_checks=True,
#         )
#     }
# else:
#     # Mode développement local si la variable n'est pas définie
DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "Lock",
            "USER": "postgres",
            "PASSWORD": "Prince@#2006",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }

# --- Validation des mots de passe ---
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]

# --- Internationalisation (i18n) ---
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True

# La liste de langues qui sera utilisée pour le menu déroulant.
LANGUAGES = [
    ('fr', _('Français')),
    ('en', _('English')),
    ('es', _('Español')),
]

# Indique à Django où chercher les fichiers de traduction.
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

USE_TZ = True

# --- Fichiers statiques et médias ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# --- Configuration par défaut ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Configuration de l'e-mail ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER