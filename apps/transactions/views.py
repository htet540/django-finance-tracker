from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db import transaction as db_transaction
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator

from .models import Transaction
from .forms import TransactionForm, AttachmentFormSet
from apps.common.auth import is_admin, is_manager
from apps.common.models import AuditLog

@login_required
def transaction_list(request):
    qs = Transaction.objects.filter(is_deleted=False).select_related("entity", "currency", "designated_purpose")
    paginator = Paginator(qs.order_by('-date', '-id'), 25)
    page_obj = paginator.get_page(request.GET.get('page') or 1)
    return render(request, "transactions/transaction_list.html", {"page_obj": page_obj})

@login_required
@db_transaction.atomic
def transaction_create(request):
    if not (is_admin(request.user) or is_manager(request.user)):
        return HttpResponseForbidden("You do not have permission to create transactions.")
    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            tx = form.save(commit=False)
            tx.created_by = request.user
            tx.save()
            formset = AttachmentFormSet(request.POST, request.FILES, instance=tx)
            if formset.is_valid():
                formset.save()
                AuditLog.objects.create(
                    action=AuditLog.ACTION_CREATE,
                    user=request.user,
                    content_type=ContentType.objects.get_for_model(Transaction),
                    object_id=str(tx.pk),
                    changes={"created": True},
                )
                messages.success(request, "Transaction created.")
                return redirect("transactions:index")
        else:
            formset = AttachmentFormSet(request.POST, request.FILES)
    else:
        form = TransactionForm()
        formset = AttachmentFormSet()
    return render(request, "transactions/transaction_form.html", {"form": form, "formset": formset, "title": "Add Transaction"})

@login_required
@db_transaction.atomic
def transaction_edit(request, pk):
    if not (is_admin(request.user) or is_manager(request.user)):
        return HttpResponseForbidden("You do not have permission to edit transactions.")
    tx = get_object_or_404(Transaction, pk=pk, is_deleted=False)
    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES, instance=tx)
        form.fields.pop("entity_type", None)  # not a model field
        if form.is_valid():
            tx = form.save()
            formset = AttachmentFormSet(request.POST, request.FILES, instance=tx)
            if formset.is_valid():
                formset.save()
                AuditLog.objects.create(
                    action=AuditLog.ACTION_UPDATE,
                    user=request.user,
                    content_type=ContentType.objects.get_for_model(Transaction),
                    object_id=str(tx.pk),
                    changes={"updated": True},
                )
                messages.success(request, "Transaction updated.")
                return redirect("transactions:index")
        else:
            formset = AttachmentFormSet(request.POST, request.FILES, instance=tx)
    else:
        form = TransactionForm(instance=tx, initial={"entity_type": tx.entity.type})
        formset = AttachmentFormSet(instance=tx)
    return render(request, "transactions/transaction_form.html", {"form": form, "formset": formset, "title": "Edit Transaction"})

@login_required
def transaction_delete(request, pk):
    if not is_admin(request.user):
        return HttpResponseForbidden("Only Admin can delete transactions.")
    tx = get_object_or_404(Transaction, pk=pk, is_deleted=False)
    tx.is_deleted = True
    tx.save()
    AuditLog.objects.create(
        action=AuditLog.ACTION_SOFT_DELETE,
        user=request.user,
        content_type=ContentType.objects.get_for_model(Transaction),
        object_id=str(tx.pk),
        changes={"is_deleted": True},
    )
    messages.info(request, "Transaction deleted (soft).")
    return redirect("transactions:index")