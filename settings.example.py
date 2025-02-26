"""Django settings for djmailer project."""
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'SecretExampleKey123!@#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1',]

ADMINS = MANAGERS = (("Admin", "admin@example.com"),)

EMAIL_HOST = 'mail.example.com'
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = SERVER_EMAIL = "djmailer@example.com"
EMAIL_SUBJECT_PREFIX = "[Django: " + ALLOWED_HOSTS[0] + "] "

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.CoreConfig',
    'apps.UsersConfig',
    'apps.MailerConfig',
    'apps.WidgetsConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

AUTH_USER_MODEL = "users.WidgetUser"
AUTHENTICATION_BACKENDS = ("apps.users.backends.WidgetUserAuthBackend",)

ROOT_URLCONF = 'urls'
WEBSITE_TITLE = 'Widgets'

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

WSGI_APPLICATION = 'wsgi.application'

X_FRAME_OPTIONS = "SAMEORIGIN"

# Database.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'exampledb',
        'USER': 'exampleuser',
        'PASSWORD': 'Secret123!',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

# Password validation.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization.
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images).
MEDIA_URL = 'media/'
MEDIA_ROOT = Path(BASE_DIR, MEDIA_URL)

SITE_ID = 1
STATIC_URL = 'static/'
STATIC_ROOT = Path(BASE_DIR, STATIC_URL)

# Default primary key field type.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
