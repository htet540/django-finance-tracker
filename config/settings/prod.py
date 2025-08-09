from .base import *
import os

# --- Core prod flags ---
DEBUG = False

# Hosts (REQUIRED in prod)
ALLOWED_HOSTS = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()]

# --- Security (tweak as needed) ---
SECURE_SSL_REDIRECT = bool(int(os.getenv("DJANGO_SSL_REDIRECT", "1")))  # set 0 if your proxy terminates TLS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_HSTS_SECONDS", "31536000"))  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# If behind a proxy/load balancer
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# --- Static/Media ---
# In prod, collect static files here: python manage.py collectstatic
STATIC_ROOT = BASE_DIR / "staticfiles"
# MEDIA_ROOT already defined in base.py -> BASE_DIR / "media"

# --- Database ---
# If env DB_NAME exists, assume Postgres; else fallback to SQLite (not recommended in prod).
if os.getenv("DB_NAME"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
# else: keep DATABASES from base.py (SQLite) — OK for quick demos, not real prod.