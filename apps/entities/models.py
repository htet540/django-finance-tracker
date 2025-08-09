from django.db import models
from apps.common.models import TimeStampedModel, SoftDeleteModel

class Entity(TimeStampedModel, SoftDeleteModel):
    ENTITY_TYPE_CHOICES = [
        ('donor', 'Donor'),
        ('recipient', 'Recipient'),
    ]

    custom_id = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=ENTITY_TYPE_CHOICES, default='donor')
    location = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.custom_id:
            prefix = 'D' if self.type == 'donor' else 'R'
            last_entity = Entity.objects.filter(type=self.type).order_by('-id').first()
            next_number = 1
            if last_entity and last_entity.custom_id:
                try:
                    next_number = int(last_entity.custom_id[1:]) + 1
                except ValueError:
                    pass
            self.custom_id = f"{prefix}{next_number:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.custom_id} · {self.name} · {self.get_type_display()}"