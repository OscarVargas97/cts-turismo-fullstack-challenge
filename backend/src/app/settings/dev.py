from .base import *  # noqa

DEV_APPS = [
    "debug_toolbar",
    "silk",
    "django_extensions",
]

MIDDLEWARE = MIDDLEWARE + [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "silk.middleware.SilkyMiddleware",
]

SIMPLE_JWT["AUTH_COOKIE_SECURE"] = True
CSRF_COOKIE_SECURE = False

INTERNAL_IPS = [
    "127.0.0.1",  # Añade la IP local para activar Debug Toolbar en desarrollo
]

INSTALLED_APPS = INSTALLED_APPS + DEV_APPS

DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True
