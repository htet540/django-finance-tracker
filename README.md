# Django Finance Tracker

Entities (Donors/Recipients), Transactions with attachments, Dashboard, Reports (CSV/XLSX/PDF), soft delete, roles (Admin/Manager/User), audit logs.

## Quick start (dev)

```bash
python3 -m venv venv && source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env  # or create .env
python manage.py migrate
python manage.py createsuperuser
python manage.py init_roles
python manage.py seed_currencies
python manage.py seed_purposes
python manage.py runserver