import os  # noqa
from datetime import timedelta
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))
env = environ.Env(
    DJANGO_SECRET_KEY=(
        str,
        "django-insecure-084#^2w=y+3@v-%ctg%q)4*$fyz4+uqmi80dw(2q_hjbpb0u%-",  # noqa: E501
    ),
    PG_DATABASE_NAME=(str, "mydatabase"),  # noqa: E501
    PG_DATABASE_USER=(str, "myuser"),  # noqa: E501
    PG_DATABASE_PASSWORD=(str, "mypassword"),  # noqa: E501
    PG_DATABASE_HOST=(str, "db"),
    PG_DATABASE_PORT=(int, 5432),
    EMAIL_HOST_USER=(str, ""),
    EMAIL_HOST_PASSWORD=(str, ""),
    DEFAULT_FROM_EMAIL=(str, ""),
    FRONTEND_URL=(str, ""),
)


SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = []

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_softdelete",
    "psycopg",
]

LOCAL_APPS = [
    "app",
    "authentication",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # noqa: F401
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

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

WSGI_APPLICATION = "app.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # noqa: F401
        "HOST": env("PG_DATABASE_HOST"),
        "NAME": env("PG_DATABASE_NAME"),
        "USER": env("PG_DATABASE_USER"),
        "PASSWORD": env("PG_DATABASE_PASSWORD"),
        "PORT": env("PG_DATABASE_PORT"),
        "ATOMIC_REQUESTS": True,
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # noqa: F401
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

SIMPLE_JWT = {
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",  # noqa
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "SIGNING_KEY": "tu_clave_secreta",
    "ALGORITHM": "HS256",
    "AUTH_COOKIE": "jwt-access-token",
    "AUTH_COOKIE_SECURE": False,
    "AUTH_COOKIE_HTTP_ONLY": True,
    "AUTH_COOKIE_PATH": "/",
    "AUTH_COOKIE_SAMESITE": "Lax",
    "USER_ID_FIELD": "uuid",
    "USER_ID_CLAIM": "user_uuid",
}

CSRF_COOKIE_NAME = "csrf_token"
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = True


CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_IGNORE_RESULT = True
CELERY_BROKER_URL = os.environ.get("CELERY_URL")
CELERYD_HIJACK_ROOT_LOGGER = False  # noqa: F401
REDIS_CHANNEL_URL = os.environ.get("REDIS_CHANNEL_URL")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
FRONTEND_URL = env("FRONTEND_URL")

AUTH_USER_MODEL = "authentication.User"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
