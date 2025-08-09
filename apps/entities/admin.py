from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from .models import Entity
from apps.common.models import AuditLog
from apps.common.diff import model_changes
from apps.common.auth import is_admin, is_manager

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('custom_id', 'name', 'type', 'location', 'is_deleted')
    list_filter = ('type', 'is_deleted', 'location')
    search_fields = ('custom_id', 'name')
    readonly_fields = ('custom_id', 'created_at', 'updated_at')

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
            old = Entity.objects.get(pk=obj.pk)
            super().save_model(request, obj, form, change)
            changed = model_changes(obj, old, ["name", "type", "location", "is_deleted"])
            if changed:
                AuditLog.objects.create(
                    action=AuditLog.ACTION_UPDATE,
                    user=request.user,
                    content_type=ContentType.objects.get_for_model(Entity),
                    object_id=str(obj.pk),
                    changes=changed,
                )
        else:
            super().save_model(request, obj, form, change)
            AuditLog.objects.create(
                action=AuditLog.ACTION_CREATE,
                user=request.user,
                content_type=ContentType.objects.get_for_model(Entity),
                object_id=str(obj.pk),
                changes={"created": True},
            )

    def delete_model(self, request, obj):
        pk = obj.pk
        super().delete_model(request, obj)
        AuditLog.objects.create(
            action=AuditLog.ACTION_DELETE,
            user=request.user,
            content_type=ContentType.objects.get_for_model(Entity),
            object_id=str(pk),
            changes={"deleted": True},
        )