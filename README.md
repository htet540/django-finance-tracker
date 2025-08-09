# Django Finance Tracker

A Django app for tracking income/expenses with reports, filters, and exports.

## Quickstart
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
### 3) Add an `.env.example` (good practice for deployment later)
```bash
cat > .env.example << 'EOF'
# Example env vars
DJANGO_SECRET_KEY=replace-me
DJANGO_DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
