from django import forms
from apps.common.models import Currency, Purpose

ENTITY_TYPE_CHOICES = [
    ("", "All"),
    ("donor", "Donor"),
    ("recipient", "Recipient"),
]

class DashboardFilterForm(forms.Form):
    # Existing text filters
    custom_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Exact entity ID (e.g., D0001)"})
    )
    entity_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Entity name contains..."})
    )

    # NEW: Entity autocomplete (stores entity id)
    entity = forms.CharField(
        required=False,
        widget=forms.Select(attrs={"class": "form-select", "id": "entity-select"})
    )

    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "placeholder": "DD/MM/YYYY"})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "placeholder": "DD/MM/YYYY"})
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Location contains..."})
    )
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.filter(is_active=True).order_by("code"),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    entity_type = forms.ChoiceField(
        choices=ENTITY_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select", "id": "entity-type"})
    )
    designated_purpose = forms.ModelChoiceField(
        queryset=Purpose.objects.filter(is_active=True).order_by("name"),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )