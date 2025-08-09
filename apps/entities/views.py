from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator

from .models import Entity
from .forms import EntityForm
from apps.common.auth import is_admin, is_manager
from apps.common.models import AuditLog

@login_required
def entity_list(request):
    qs = Entity.objects.filter(is_deleted=False).order_by('custom_id')
    paginator = Paginator(qs, 25)
    page_obj = paginator.get_page(request.GET.get('page') or 1)
    return render(request, 'entities/entity_list.html', {'page_obj': page_obj})

@login_required
def entity_create(request):
    if not (is_admin(request.user) or is_manager(request.user)):
        return HttpResponseForbidden("You do not have permission to create entities.")
    if request.method == 'POST':
        form = EntityForm(request.POST)
        if form.is_valid():
            obj = form.save()
            AuditLog.objects.create(
                action=AuditLog.ACTION_CREATE,
                user=request.user,
                content_type=ContentType.objects.get_for_model(Entity),
                object_id=str(obj.pk),
                changes={"created": True},
            )
            return redirect('entities:index')
    else:
        form = EntityForm()
    return render(request, 'entities/entity_form.html', {'form': form, 'title': 'Add Entity'})

@login_required
def entity_edit(request, pk):
    if not (is_admin(request.user) or is_manager(request.user)):
        return HttpResponseForbidden("You do not have permission to edit entities.")
    entity = get_object_or_404(Entity, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = EntityForm(request.POST, instance=entity)
        if form.is_valid():
            form.save()
            AuditLog.objects.create(
                action=AuditLog.ACTION_UPDATE,
                user=request.user,
                content_type=ContentType.objects.get_for_model(Entity),
                object_id=str(entity.pk),
                changes={"updated": True},
            )
            return redirect('entities:index')
    else:
        form = EntityForm(instance=entity)
    return render(request, 'entities/entity_form.html', {'form': form, 'title': 'Edit Entity'})

@login_required
def entity_delete(request, pk):
    if not is_admin(request.user):
        return HttpResponseForbidden("Only Admin can delete entities.")
    entity = get_object_or_404(Entity, pk=pk, is_deleted=False)
    entity.is_deleted = True
    entity.save()
    AuditLog.objects.create(
        action=AuditLog.ACTION_SOFT_DELETE,
        user=request.user,
        content_type=ContentType.objects.get_for_model(Entity),
        object_id=str(entity.pk),
        changes={"is_deleted": True},
    )
    return redirect('entities:index')

@login_required
def entity_autocomplete(request):
    q = request.GET.get('q', '')
    entity_type = request.GET.get('type')
    qs = Entity.objects.filter(is_deleted=False)
    if entity_type in ['donor', 'recipient']:
        qs = qs.filter(type=entity_type)
    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(custom_id__icontains=q)
    results = [
        {'id': e.id, 'text': f"{e.custom_id} · {e.name} · {e.get_type_display()}"}
        for e in qs.order_by('custom_id')[:20]
    ]
    return JsonResponse({'results': results})