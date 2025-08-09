from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from .models import Transaction, TransactionAttachment
from apps.common.models import AuditLog
from apps.common.diff import model_changes
from apps.common.auth import is_admin, is_manager

class TransactionAttachmentInline(admin.TabularInline):
    model = TransactionAttachment
    extra = 0

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "entity", "currency", "amount", "exchange_rate", "converted_amount_mmk", "created_by", "is_deleted")
    list_filter = ("currency", "entity__type", "is_deleted", "date")
    search_fields = ("entity__custom_id", "entity__name")
    autocomplete_fields = ("entity",)
    inlines = [TransactionAttachmentInline]

    # Role gates
    def has_delete_permission(self, request, obj=None):
        return is_admin(request.user)
    def has_add_permission(self, request):
        return is_admin(request.user) or is_manager(request.user)
    def has_change_permission(self, request, obj=None):
        return is_admin(request.user) or is_manager(request.user)

    # Audit hooks
    def save_model(self, request, obj, form, change):
        if change:
            old = Transaction.objects.get(pk=obj.pk)
            super().save_model(request, obj, form, change)
            changed = model_changes(obj, old, ["date", "entity_id", "currency_id", "amount", "exchange_rate", "converted_amount_mmk", "designated_purpose_id", "notes", "is_deleted"])
            if changed:
                AuditLog.objects.create(
                    action=AuditLog.ACTION_UPDATE,
                    user=request.user,
                    content_type=ContentType.objects.get_for_model(Transaction),
                    object_id=str(obj.pk),
                    changes=changed,
                )
        else:
            if not obj.created_by:
                obj.created_by = request.user
            super().save_model(request, obj, form, change)
            AuditLog.objects.create(
                action=AuditLog.ACTION_CREATE,
                user=request.user,
                content_type=ContentType.objects.get_for_model(Transaction),
                object_id=str(obj.pk),
                changes={"created": True},
            )

    def delete_model(self, request, obj):
        pk = obj.pk
        super().delete_model(request, obj)
        AuditLog.objects.create(
            action=AuditLog.ACTION_DELETE,
            user=request.user,
            content_type=ContentType.objects.get_for_model(Transaction),
            object_id=str(pk),
            changes={"deleted": True},
        )

@admin.register(TransactionAttachment)
class TransactionAttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "transaction", "file", "created_at")