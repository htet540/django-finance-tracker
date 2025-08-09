from pathlib import Path
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

# ──────────────────────────────────────────────────────────────────────────────
# Paths & basics
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "insecure-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

# Render gives you the full external URL in RENDER_EXTERNAL_URL, e.g.
# https://django-finance-tracker.onrender.com
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "").strip()

# Helper to extract host from a URL (for ALLOWED_HOSTS)
def _host_from_url(url: str) -> str:
    try:
        return urlparse(url).hostname or ""
    except Exception:
        return ""

# Build ALLOWED_HOSTS
# - From env DJANGO_ALLOWED_HOSTS (comma-separated)
# - Always allow localhost
# - Add Render host if available
_env_hosts = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()]
_default_hosts = ["127.0.0.1", "localhost"]
_render_host = _host_from_url(RENDER_EXTERNAL_URL)
ALLOWED_HOSTS = list(dict.fromkeys(_env_hosts + _default_hosts + ([_render_host] if _render_host else [])))

# ──────────────────────────────────────────────────────────────────────────────
# Apps
# ──────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 3rd party
    "django_filters",
    "crispy_forms",
    "crispy_bootstrap5",

    # Local apps
    "apps.common",
    "apps.entities",
    "apps.transactions",
    "apps.dashboard",
    "apps.reports",
]

# ──────────────────────────────────────────────────────────────────────────────
# Middleware
# ──────────────────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # If you’re using Whitenoise in production, add:
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# When running behind Render’s proxy, ensure Django knows the original scheme
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ──────────────────────────────────────────────────────────────────────────────
# URLs / WSGI / ASGI
# ──────────────────────────────────────────────────────────────────────────────
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ──────────────────────────────────────────────────────────────────────────────
# Templates
# ──────────────────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# ──────────────────────────────────────────────────────────────────────────────
# Database (SQLite dev)
# ──────────────────────────────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ──────────────────────────────────────────────────────────────────────────────
# I18N / TZ
# ──────────────────────────────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Bangkok"
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────────────────────────────────────
# Static & Media
# ──────────────────────────────────────────────────────────────────────────────
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# ──────────────────────────────────────────────────────────────────────────────
# Crispy Forms
# ──────────────────────────────────────────────────────────────────────────────
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ──────────────────────────────────────────────────────────────────────────────
# Auth redirects
# ──────────────────────────────────────────────────────────────────────────────
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard:index"
LOGOUT_REDIRECT_URL = "login"

# ──────────────────────────────────────────────────────────────────────────────
# Date input formats
# ──────────────────────────────────────────────────────────────────────────────
from django.conf.locale.en import formats as en_formats
en_formats.DATE_INPUT_FORMATS = ["%d/%m/%Y", "%Y-%m-%d"]
en_formats.DATETIME_INPUT_FORMATS = ["%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M:%S"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ──────────────────────────────────────────────────────────────────────────────
# CSRF trusted origins (must include scheme)
# ──────────────────────────────────────────────────────────────────────────────
# Start with local dev:
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1",
    "http://localhost",
    "https://127.0.0.1",
    "https://localhost",
]

# Add Render external URL if present
if RENDER_EXTERNAL_URL:
    # e.g. https://django-finance-tracker.onrender.com
    CSRF_TRUSTED_ORIGINS.append(RENDER_EXTERNAL_URL)