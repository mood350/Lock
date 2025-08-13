import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url  # type: ignore

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#Key configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FEDAPAY_PUBLIC_KEY = os.getenv("FEDAPAY_PUBLIC_KEY")
FEDAPAY_SECRET_KEY = os.getenv("FEDAPAY_SECRET_KEY")
FEDAPAY_WEBHOOK_SECRET = os.getenv("FEDAPAY_WEBHOOK_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG")  # Temporairement True pour le débogage

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'lock-1-r3rz.onrender.com',]
CSRF_TRUSTED_ORIGINS = ['https://lock-1-r3rz.onrender.com']

# Application definition
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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Middleware pour servir les fichiers statiques
    'django.contrib.sessions.middleware.SessionMiddleware',
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
# DATABASE_URL = os.getenv("DATABASE_URL")
# # Database
# if DATABASE_URL:
#     # Si DATABASE_URL est définie, utilisez-la (mode production)
#     DATABASES = {
#         'default': dj_database_url.config(
#             default=DATABASE_URL,
#             conn_max_age=600,
#             conn_health_checks=True,
#         )
#     }
#     # Assurez-vous que DEBUG est désactivé en production
#     DEBUG = True
# else:
#     # Sinon, utilisez la configuration locale (mode développement)
#     # Assurez-vous que le .env est chargé pour cette configuration
#     from dotenv import load_dotenv
#     load_dotenv()
    
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
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Ajout pour collectstatic
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER