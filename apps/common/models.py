from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()
    class Meta:
        abstract = True

# Flexible lists managed in admin
class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True)  # e.g., MMK, USD, SGD, THB
    name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ["code"]
    def __str__(self):
        return self.code

class Purpose(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ["name"]
    def __str__(self):
        return self.name

class AuditLog(models.Model):
    ACTION_CREATE = "create"
    ACTION_UPDATE = "update"
    ACTION_DELETE = "delete"
    ACTION_SOFT_DELETE = "soft_delete"

    action = models.CharField(max_length=20)
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=64)
    content_object = GenericForeignKey("content_type", "object_id")

    changes = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} {self.action} by {self.user} on {self.content_type}:{self.object_id}"    
