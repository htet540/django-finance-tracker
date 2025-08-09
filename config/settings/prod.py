# config/settings/prod.py
from .base import *  # noqa
import os

# --- Core ---
DEBUG = False
# Reuse base SECRET_KEY unless an env override is provided
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", SECRET_KEY)

# --- Hosts / CSRF ---
# Prefer explicit list via env; otherwise fall back to Render hostname if present
_allowed = os.getenv("DJANGO_ALLOWED_HOSTS")
if _allowed:
    ALLOWED_HOSTS = [h.strip() for h in _allowed.split(",") if h.strip()]
else:
    render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    if render_host:
        ALLOWED_HOSTS = [render_host, ".onrender.com"]
    else:
        ALLOWED_HOSTS = [".onrender.com", "127.0.0.1", "localhost"]

# CSRF trusted origins: allow explicit env or derive from ALLOWED_HOSTS
_csrf = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS")
if _csrf:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf.split(",") if o.strip()]
else:
    # Build https://<host> entries (skip wildcard-only hosts here)
    CSRF_TRUSTED_ORIGINS = [
        f"https://{h}"
        for h in ALLOWED_HOSTS
        if h and not h.startswith(".") and h != "localhost" and not h.startswith("127.")
    ]
    # Always include Render wildcard
    CSRF_TRUSTED_ORIGINS += ["https://*.onrender.com"]

# --- Static files (WhiteNoise) ---
# Insert WhiteNoise right after SecurityMiddleware if not already present
if "whitenoise.middleware.WhiteNoiseMiddleware" not in MIDDLEWARE:
    try:
        i = MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1
    except ValueError:
        i = 0
    MIDDLEWARE = (
        MIDDLEWARE[:i]
        + ["whitenoise.middleware.WhiteNoiseMiddleware"]
        + MIDDLEWARE[i:]
    )

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- Security ---
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# --- Logging ---
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": os.getenv("DJANGO_LOG_LEVEL", "INFO")},
}