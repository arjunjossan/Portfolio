import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SECRET_KEY = "django-insecure-change-me-before-production"

def env(key, default=None, cast=str):
    value = os.getenv(key, default)
    if value is None:
        return None
    if cast is bool:
        return str(value).lower() in {"1", "true", "yes", "on"}
    if cast is list:
        return [item.strip() for item in str(value).split(",") if item.strip()]
    return cast(value)


SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    DEFAULT_SECRET_KEY,
)
DEBUG = env("DJANGO_DEBUG", True, bool)
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost", list)
CSRF_TRUSTED_ORIGINS = env("DJANGO_CSRF_TRUSTED_ORIGINS", "", list)

if not DEBUG and SECRET_KEY == DEFAULT_SECRET_KEY:
    raise ValueError("Set DJANGO_SECRET_KEY in production when DJANGO_DEBUG is False.")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'portfolio_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'portfolio_app.context_processors.site_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio_project.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': env('DB_NAME', str(BASE_DIR / 'db.sqlite3')),
        'USER': env('DB_USER', ''),
        'PASSWORD': env('DB_PASSWORD', ''),
        'HOST': env('DB_HOST', ''),
        'PORT': env('DB_PORT', ''),
    }
}


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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = env('DJANGO_TIME_ZONE', 'Asia/Kolkata')

USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

EMAIL_BACKEND = env(
    'DJANGO_EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend',
)
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', 'portfolio@example.com')
CONTACT_NOTIFICATION_EMAIL = env('CONTACT_NOTIFICATION_EMAIL', DEFAULT_FROM_EMAIL)

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT', not DEBUG, bool)
CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE', False, bool)
SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE', False, bool)
CSRF_COOKIE_HTTPONLY = env('CSRF_COOKIE_HTTPONLY', False, bool)
SECURE_HSTS_SECONDS = env('SECURE_HSTS_SECONDS', 0, int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env('SECURE_HSTS_INCLUDE_SUBDOMAINS', False, bool)
SECURE_HSTS_PRELOAD = env('SECURE_HSTS_PRELOAD', False, bool)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
