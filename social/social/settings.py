import os
import sentry_sdk
from pathlib import Path
from envparse import env
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = env.bool("DEBUG")
SERVER_IP = env.str("SERVER_IP")
SECRET_KEY = env.str("SECRET_KEY")
BACKEND_URL = env.str("BACKEND_URL")
ALLOWED_HOSTS = [env.str("ALLOWED_HOSTS")]
BASE_DIR = Path(__file__).resolve().parent.parent

LOCAL = "local"
PRODUCTION = "production"
ENVIRONMENT = env.str("ENVIRONMENT", default="local")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "network",
    "telegram",
    "linkedin",
    "twitter",
    "notification",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "social.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "social.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "social_db",
        "NAME": "postgres",
        "PORT": 5432,
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


STATIC_URL = "/static/"
if DEBUG:
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Celery
BROKER_URL = "redis://social_redis:6379"
CELERY_RESULT_BACKEND = "redis://social_redis:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Tehran"


TELEGRAM_API_ID = env.str("TELEGRAM_API_ID")
TELEGRAM_API_HASH = env.str("TELEGRAM_API_HASH")
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGIN_REGEXES = ["*"]

if (dsn := env.str("SENTRY_DSN", default=None)) is not None:
    sentry_sdk.init(
        dsn=dsn,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        environment="ras-soc",
    )

LINKEDIN_EMAIL = env.str("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = env.str("LINKEDIN_PASSWORD")
