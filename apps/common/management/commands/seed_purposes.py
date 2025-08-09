from django.core.management.base import BaseCommand
from apps.common.models import Purpose

DEFAULTS = [
    "General Donation",
    "Medical Aid",
    "Education Support",
    "Emergency Relief",
]

class Command(BaseCommand):
    help = "Seed sample designated purposes."

    def handle(self, *args, **options):
        created, existing = 0, 0
        for name in DEFAULTS:
            obj, was_created = Purpose.objects.get_or_create(
                name=name, defaults={"is_active": True}
            )
            if was_created:
                created += 1
            else:
                existing += 1
                if not obj.is_active:
                    obj.is_active = True
                    obj.save()
        self.stdout.write(self.style.SUCCESS(f"Purposes seeded. created={created}, existing={existing}"))