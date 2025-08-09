from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Case, When, DecimalField, Value
from django.shortcuts import render

from apps.transactions.models import Transaction
from apps.dashboard.forms import DashboardFilterForm

@login_required
def index(request):
    form = DashboardFilterForm(request.GET or None)

    qs = (
        Transaction.objects
        .filter(is_deleted=False, entity__is_deleted=False)
        .select_related("entity", "currency", "designated_purpose")
    )

    if form.is_valid():
        cd = form.cleaned_data

        # NEW: entity autocomplete (by id)
        if cd.get("entity"):
            try:
                qs = qs.filter(entity_id=int(cd["entity"]))
            except (TypeError, ValueError):
                pass

        # Existing: exact custom_id + name contains
        if cd.get("custom_id"):
            qs = qs.filter(entity__custom_id__iexact=cd["custom_id"].strip())

        if cd.get("entity_name"):
            qs = qs.filter(entity__name__icontains=cd["entity_name"])

        # Existing filters
        if cd.get("date_from"):
            qs = qs.filter(date__gte=cd["date_from"])
        if cd.get("date_to"):
            qs = qs.filter(date__lte=cd["date_to"])

        if cd.get("location"):
            qs = qs.filter(entity__location__icontains=cd["location"])

        if cd.get("currency"):
            qs = qs.filter(currency=cd["currency"])

        if cd.get("entity_type"):
            et = cd["entity_type"]
            if et in ("donor", "recipient"):
                qs = qs.filter(entity__type=et)

        if cd.get("designated_purpose"):
            qs = qs.filter(designated_purpose=cd["designated_purpose"])

    # Totals
    totals = qs.aggregate(
        total_donated=Sum(
            Case(
                When(entity__type="donor", then="converted_amount_mmk"),
                default=Value(0),
                output_field=DecimalField(max_digits=14, decimal_places=2),
            )
        ),
        total_distributed=Sum(
            Case(
                When(entity__type="recipient", then="converted_amount_mmk"),
                default=Value(0),
                output_field=DecimalField(max_digits=14, decimal_places=2),
            )
        ),
    )
    total_donated = totals["total_donated"] or Decimal("0")
    total_distributed = totals["total_distributed"] or Decimal("0")
    remaining = total_donated - total_distributed

    # Per-currency summary
    per_currency = (
        qs.values("currency__code")
        .annotate(
            donated=Sum(
                Case(
                    When(entity__type="donor", then="converted_amount_mmk"),
                    default=Value(0),
                    output_field=DecimalField(max_digits=14, decimal_places=2),
                )
            ),
            distributed=Sum(
                Case(
                    When(entity__type="recipient", then="converted_amount_mmk"),
                    default=Value(0),
                    output_field=DecimalField(max_digits=14, decimal_places=2),
                )
            ),
        )
        .order_by("currency__code")
    )
    summary_by_currency = []
    for row in per_currency:
        donated = row["donated"] or Decimal("0")
        distributed = row["distributed"] or Decimal("0")
        summary_by_currency.append({
            "currency": row["currency__code"] or "-",
            "donated": donated,
            "distributed": distributed,
            "remaining": donated - distributed,
        })

    context = {
        "form": form,
        "total_donated": total_donated,
        "total_distributed": total_distributed,
        "remaining": remaining,
        "summary_by_currency": summary_by_currency,
        "recent": qs.order_by("-date", "-id")[:10],
    }
    return render(request, "dashboard/index.html", context)