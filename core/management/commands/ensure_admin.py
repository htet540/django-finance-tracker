# core/management/commands/ensure_admin.py
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

class Command(BaseCommand):
    help = "Ensure a Django superuser exists using env vars (idempotent)."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.getenv("adminpass")

        if not password:
            self.stdout.write(self.style.WARNING(
                "DJANGO_SUPERUSER_PASSWORD not set; skipping superuser creation."
            ))
            return

        with transaction.atomic():
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email, "is_staff": True, "is_superuser": True},
            )

            # If it already exists, make sure it's actually a superuser/staff and email is correct
            changed = False
            if not created:
                if user.email != email:
                    user.email = email
                    changed = True
                if not user.is_staff:
                    user.is_staff = True
                    changed = True
                if not user.is_superuser:
                    user.is_superuser = True
                    changed = True

            # Always (re)set the password to match env (so you can change it from Render)
            user.set_password(password)
            changed = True or changed

            if changed:
                user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' ensured/updated."))