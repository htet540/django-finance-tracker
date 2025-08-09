from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone

from apps.common.models import TimeStampedModel, SoftDeleteModel, Currency, Purpose
from apps.entities.models import Entity

class Transaction(TimeStampedModel, SoftDeleteModel):
    entity = models.ForeignKey(Entity, on_delete=models.PROTECT, related_name="transactions")
    date = models.DateField(default=timezone.now)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    exchange_rate = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal("1.0000"))
    converted_amount_mmk = models.DecimalField(max_digits=14, decimal_places=2, editable=False)

    designated_purpose = models.ForeignKey(
        Purpose, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions"
    )
    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_transactions"
    )

    class Meta:
        ordering = ["-date", "-id"]

    def save(self, *args, **kwargs):
        # always keep converted_amount_mmk in sync
        rate = self.exchange_rate or Decimal("1")
        amt = self.amount or Decimal("0")
        self.converted_amount_mmk = (amt * rate).quantize(Decimal("1.00"))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} · {self.entity.custom_id} · {self.currency.code} {self.amount}"

def attachment_upload_to(instance, filename):
    return f"transactions/{instance.transaction_id}/{filename}"

class TransactionAttachment(TimeStampedModel):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to=attachment_upload_to)
    def __str__(self):
        return f"Attachment #{self.id} for Tx {self.transaction_id}"