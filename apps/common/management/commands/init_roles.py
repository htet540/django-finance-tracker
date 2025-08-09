from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from apps.entities.models import Entity
from apps.transactions.models import Transaction, TransactionAttachment
from apps.common.models import Currency, Purpose, AuditLog
from apps.common.auth import ADMIN, MANAGER, USER

class Command(BaseCommand):
    help = "Initialize user roles (Admin, Manager, User) and assign permissions."

    def handle(self, *args, **options):
        # Ensure groups
        admin_g, _ = Group.objects.get_or_create(name=ADMIN)
        manager_g, _ = Group.objects.get_or_create(name=MANAGER)
        user_g, _ = Group.objects.get_or_create(name=USER)

        def perms_for(model, actions=("add", "change", "delete", "view")):
            ct = ContentType.objects.get_for_model(model)
            codes = [f"{a}_{model._meta.model_name}" for a in actions]
            return list(Permission.objects.filter(content_type=ct, codename__in=codes))

        # Collect permissions
        entity_perms_all = perms_for(Entity)
        entity_perms_nodel = perms_for(Entity, ("add", "change", "view"))

        tx_perms_all = perms_for(Transaction)
        tx_perms_nodel = perms_for(Transaction, ("add", "change", "view"))

        attach_perms_all = perms_for(TransactionAttachment)
        attach_perms_nodel = perms_for(TransactionAttachment, ("add", "change", "view"))

        currency_perms_view = perms_for(Currency, ("view",))
        purpose_perms_view = perms_for(Purpose, ("view",))
        audit_perms_view = perms_for(AuditLog, ("view",))

        # Admin: everything for these models
        admin_g.permissions.set(
            entity_perms_all + tx_perms_all + attach_perms_all +
            currency_perms_view + purpose_perms_view + audit_perms_view
        )

        # Manager: add/change/view; no delete
        manager_g.permissions.set(
            entity_perms_nodel + tx_perms_nodel + attach_perms_nodel +
            currency_perms_view + purpose_perms_view + audit_perms_view
        )

        # User: view only (including audit view for transparency)
        user_g.permissions.set(
            perms_for(Entity, ("view",)) +
            perms_for(Transaction, ("view",)) +
            perms_for(TransactionAttachment, ("view",)) +
            currency_perms_view + purpose_perms_view + audit_perms_view
        )

        self.stdout.write(self.style.SUCCESS("Roles initialized: Admin, Manager, User."))
        self.stdout.write(self.style.SUCCESS("Assign users to groups via /admin."))