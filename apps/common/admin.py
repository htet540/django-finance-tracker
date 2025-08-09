from django.contrib import admin
from .models import Currency, Purpose, AuditLog


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name")

@admin.register(Purpose)
class PurposeAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "action", "user", "content_type", "object_id")
    list_filter = ("action", "content_type")
    search_fields = ("object_id", "user__username")
    readonly_fields = ("created_at", "action", "user", "content_type", "object_id", "changes")