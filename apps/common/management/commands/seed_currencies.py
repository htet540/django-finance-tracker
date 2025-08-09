from django.core.management.base import BaseCommand
from apps.common.models import Currency

DEFAULTS = [
    ("MMK", "Myanmar Kyat"),
    ("USD", "US Dollar"),
    ("SGD", "Singapore Dollar"),
    ("THB", "Thai Baht"),
]

class Command(BaseCommand):
    help = "Seed default currencies (MMK, USD, SGD, THB)."

    def handle(self, *args, **options):
        created, existing = 0, 0
        for code, name in DEFAULTS:
            obj, was_created = Currency.objects.get_or_create(
                code=code, defaults={"name": name, "is_active": True}
            )
            if was_created:
                created += 1
            else:
                existing += 1
                if obj.name != name or not obj.is_active:
                    obj.name = name
                    obj.is_active = True
                    obj.save()
        self.stdout.write(self.style.SUCCESS(f"Currencies seeded. created={created}, existing={existing}"))